"""
Common utilities for Fina Files processing.
"""
from typing import List
from typing import Optional
from typing import Union
import logging
import datetime as dt
import numpy as np
from emon_tools.emon_fina.fina_models import OutputAverageEnum
from emon_tools.emon_fina.fina_models import OutputType
from emon_tools.emon_fina.fina_models import FinaByDateParamsModel
from emon_tools.emon_fina.fina_models import FinaByTimeParamsModel
from emon_tools.emon_fina.fina_services import FinaOutputData
from emon_tools.emon_fina.fina_utils import Utils as Ut
from emon_tools.emon_fina.fina_reader import FinaReader

logging.basicConfig()
et_logger = logging.getLogger(__name__)


class FinaData:
    """
    A class to handle data retrieval and processing from a Fina data file.
    """
    def __init__(self, file_name: str, data_dir: str):
        """
        Initialize the FinaData object with a FinaReader instance.

        Parameters:
            file_name (str): Fina File Name
            data_dir (str): Directory path to the Fina data files.
        """
        self.reader = FinaReader(file_name=file_name, data_dir=data_dir)
        self.meta = self.reader.read_meta()
        self.length = self.meta.npoints * self.meta.interval
        self.lines: int = 0
        self.start: Optional[int] = None
        self.end: Optional[int] = None
        self.step: Optional[int] = None

    def _read_direct_values(
        self,
        props: FinaByTimeParamsModel
    ) -> np.ndarray:
        """
        Read raw values when the step interval is less than or equal
        to the metadata interval.

        This method retrieves data points directly from the file,
        filling the result array
        sequentially up to the required number of points (`npts`).

        Parameters:
            start (int): Start time in seconds from the feed's start time.
            step (int): Step interval in seconds for the data retrieval.
            npts (int): Number of data points to read.
            interval (int): Metadata interval in seconds.
            window (int): Total time window in seconds.
            set_pos (bool):
                If True, updates the reader's position after reading.

        Returns:
            np.ndarray: A NumPy array containing the retrieved values,
            with NaNs for missing data.

        Notes:
            - This method assumes the `step` interval
              is small enough for direct reading.
            - Values are read in chunks determined
              by `calculate_optimal_chunk_size`.
        """
        if props.output_type in (
            OutputType.VALUES_MIN_MAX,
            OutputType.TIME_SERIES_MIN_MAX
        ):
            raise ValueError(
                "Invalid output type, only 'VALUES' and 'TIME_SERIES' "
                "can be selected when interval is same as meta interval."
            )
        # initialise reader props
        self.reader.initialise_reader(
            meta=self.meta,
            props=props,
            auto_pos=True
        )

        # Initialize result storage and day boundaries
        nb_filled, result = self._initialize_result()
        for _, values in self.reader.read_file():
            available = values.shape[0]
            remaining = self.reader.props.remaining_points

            if remaining <= 0:
                break

            to_copy = min(available, remaining)
            result[nb_filled:nb_filled + to_copy] = values[:to_copy].reshape(
                (-1, 1))
            nb_filled += to_copy
        self.start = (
            self.reader.props.start_search
            * self.reader.props.search.time_interval
        ) + self.meta.start_time
        self.step = self.reader.props.search.time_interval
        self.lines = result.size
        if props.output_type == OutputType.TIME_SERIES:
            result = np.column_stack((self.timestamps(), result))
        return result

    def _process_chunk(
        self,
        values: np.ndarray,
        current_step_start: int,
        min_value: Optional[Union[int, float]],
        max_value: Optional[Union[int, float]],
        output_type: OutputType = OutputType.VALUES
    ) -> np.ndarray:
        """
        Process data for a single step by filtering and computing statistics.

        Parameters:
            values (np.ndarray): Array of data values for the current step.
            current_step_start (int): Start time of the current step.
            min_value (Optional[Union[int, float]]):
                Minimum valid value for filtering.
            max_value (Optional[Union[int, float]]):
                Maximum valid value for filtering.
            output_type (OutputType):
                Type of statistics to compute. Defaults to OutputType.VALUES.

        Returns:
            np.ndarray: Computed statistics for the current step.
        """
        filtered_values = Ut.filter_values_by_range(
            values.copy(), min_value, max_value)

        if output_type == OutputType.VALUES_MIN_MAX:
            return FinaOutputData.get_values_stats(
                values=filtered_values,
                day_start=current_step_start,
                with_stats=True,
                with_time=False
            )

        if output_type == OutputType.TIME_SERIES:
            return FinaOutputData.get_values_stats(
                values=filtered_values,
                day_start=current_step_start,
                with_stats=False
            )

        if output_type == OutputType.TIME_SERIES_MIN_MAX:
            return FinaOutputData.get_values_stats(
                values=filtered_values,
                day_start=current_step_start,
                with_stats=True
            )

        if output_type == OutputType.INTEGRITY:
            return FinaOutputData.get_integrity_stats(
                values=filtered_values,
                day_start=current_step_start
            )
        # By default return OutputType.VALUES
        return FinaOutputData.get_values_stats(
            values=filtered_values,
            day_start=current_step_start,
            with_stats=False,
            with_time=False
        )

    def _trim_results(self, result):
        """
        Trim the result array to include only processed data.

        Parameters:
            result (np.ndarray):
                Array of computed results with potential NaN entries.

        Returns:
            List[List[Union[float, int]]]:
                Trimmed result array as a list of lists.
        """
        finite_mask = np.isfinite(result[:, 0])
        if not finite_mask.any():
            return result

        last_valid_index = len(result) - np.argmax(finite_mask[::-1]) - 1
        return result[:last_valid_index + 1]

    def _round_results(
        self,
        result: np.ndarray,
        n_decimals: Optional[int] = 3
    ):
        """
        Round the result array to the specified number of decimal places.

        Parameters:
            result (np.ndarray): Array of computed results to be rounded.
            n_decimals (Optional[int]): Number of decimal places to round to.
            Defaults to 3.

        Returns:
            np.ndarray: Rounded result array.
        """
        if n_decimals is not None:
            # Apply rounding/flooring only to the data columns
            if n_decimals == 0:
                result[:] = np.floor(result[:]).astype(int)
            elif n_decimals > 0:
                result[:] = np.around(result[:], decimals=n_decimals)
        return result

    def _initialize_result(
        self
    ):
        """
        Initialize the result array and calculate points per step.

        Parameters:
            window_search (int): Number of selected points to process.

        Returns:
            A numpy array initialized with NaN values to store results.
        """
        output_type = self.reader.props.search.output_type
        window_max = self.reader.props.window_max
        block_size = self.reader.props.block_size
        # npts_total = math.ceil(window_max / block_size)
        npts_total = window_max // block_size
        steps = self.reader.props.get_initial_output_step()
        if steps > 0:
            npts_total += steps
        array = FinaOutputData.init_stats(
            output_type=output_type,
            block_size=block_size
        )
        nb_cols = 1
        if block_size > 1:
            nb_cols = len(array)
        result = np.full((npts_total, nb_cols), array)

        if steps > 0 and block_size > 1:
            for i in range(steps):
                result[i, 0] = self.reader.props.current_start
                self.reader.props.update_step_boundaries()
        return steps, result

    @staticmethod
    def rechape_by_rows(
        values: np.array,
        block_size: int,
        current_size: int,
        output_average: OutputAverageEnum,
        rest_array: np.array
    ):
        """
        Reshape a 1D numpy array into a 2D array with a specified number
        of columns, and return the remaining elements as a separate 1D array.

        If the provided rest_array is non-empty, it is concatenated
        with a copy of the values array before reshaping.
        This ensures that the original input array remains unchanged.

        Parameters:
            values (np.array): The input 1D numpy array to be reshaped.
            N (int): The number of columns for the reshaped 2D array.
            rest_array (np.array):
                An array containing leftover elements
                from a previous operation.

        Returns:
            tuple:
                A tuple containing the reshaped 2D numpy array
                and the remaining 1D numpy array.
        """
        # Work on a copy to avoid modifying the original array.
        values_copy = values.copy()

        # If rest_array is non-empty, concatenate it with the copied values.
        if rest_array is not None and rest_array.size > 0:
            combined = np.concatenate((rest_array, values_copy))
        else:
            combined = values_copy

        if block_size != current_size:
            if output_average == OutputAverageEnum.COMPLETE:
                return np.array([]), combined[current_size:]
            if output_average in (
                OutputAverageEnum.PARTIAL,
                OutputAverageEnum.AS_IS
            ):
                diff = block_size - current_size
                tmp = np.full((1, block_size), np.nan)
                # Only assign as many elements as are available.
                n = min(current_size, combined.size)
                tmp[:, diff:diff+n] = combined[:n].reshape(1, -1)
                return tmp, combined[n:]
        # Determine the number of complete rows that can be formed.
        num_full_rows = len(combined) // block_size

        # Create the 2D array from the first num_full_rows * N elements.
        array_2d = combined[:num_full_rows * block_size].reshape(
            num_full_rows, block_size)

        # Extract the remaining elements as the new rest_array.
        new_rest_array = combined[num_full_rows * block_size:]

        return array_2d, new_rest_array

    def _get_averaged_values(
        self,
        props: FinaByTimeParamsModel
    ) -> List[List[Union[float, int]]]:
        """
        Compute daily statistics from PhpFina file data.

        props Parameters:
            start_time (Optional[int]):
                Start time in seconds from the beginning of the file.
                Defaults to 0.
            steps_window (int):
                Number of steps to process. Use -1 to process all data.
                Defaults to -1.
            max_size (int):
                Maximum number of data points to process in one call.
                Defaults to 5,000,000.
            min_value (Optional[Union[int, float]]):
                Minimum valid value for filtering.
            max_value (Optional[Union[int, float]]):
                Maximum valid value for filtering.
            output_type (OutputType):
                Type of statistics to compute. Defaults to OutputType.VALUES.

        Returns:
            List[List[Union[float, int]]]:
                A list of daily statistics where each entry contains:
                - OutputType.VALUES:
                    [
                        day_start, min_value, mean_value, max_value
                    ].
                - OutputType.INTEGRITY:
                    [
                        day_start, finite_count, total_count
                    ].
        """
        # initialise reader props
        self.reader.initialise_reader(
            meta=self.meta,
            props=props,
            auto_pos=False
        )
        # Initialize result storage and day boundaries
        steps, result = self._initialize_result()
        nb_result = result.shape[0]
        # ToDo: init start nan's if any
        # Process data in chunks
        rest_array = None
        for _, values in self.reader.read_file():

            if values.shape[0] <= 0:
                break
            current_steps, rest_array = self.rechape_by_rows(
                values=values,
                block_size=self.reader.props.block_size,
                current_size=self.reader.props.current_window,
                output_average=self.reader.props.search.output_average,
                rest_array=rest_array
            )
            if current_steps is not None\
                    and current_steps.shape[0] > 0:
                for i in range(current_steps.shape[0]):
                    if steps >= nb_result:
                        break
                    result[steps] = self._process_chunk(
                        values=current_steps[i],
                        current_step_start=self.reader.props.current_start,
                        min_value=props.min_value,
                        max_value=props.max_value,
                        output_type=props.output_type
                    )

                    # Update step boundaries for next iteration
                    steps += 1
                    # update reader params
                    self.reader.props.update_step_boundaries()
            else:
                self.reader.props.update_step_boundaries()
            # else:
                # update reader params
            #    self.reader.props.iter_update_after()
            self.reader.props.get_chunk_size(
                bypass_min=False
            )
            self.reader.props.iter_update_after()

        if rest_array is not None\
                and rest_array.shape[0] > 0:
            current_steps, rest_array = self.rechape_by_rows(
                values=rest_array,
                block_size=self.reader.props.block_size,
                current_size=self.reader.props.current_window,
                output_average=self.reader.props.search.output_average,
                rest_array=None
            )
            for i in range(current_steps.shape[0]):
                if steps >= nb_result:
                    break
                result[steps] = self._process_chunk(
                    values=current_steps[i],
                    current_step_start=self.reader.props.current_start,
                    min_value=props.min_value,
                    max_value=props.max_value,
                    output_type=props.output_type
                )

                # Update step boundaries for next iteration
                steps += 1
                # update reader params
                self.reader.props.update_step_boundaries()
        # Trim and return results
        return self._trim_results(result)

    def reset(self):
        """
        Reset the object's state to its default values.

        This method reinitializes the core properties of the object,
        ensuring that it is in a clean and consistent state for reuse.
        Useful for scenarios where the object's attributes need to
        be cleared and set to their default states.

        Attributes Reset:
            - `lines` (int):
                Resets to 0, representing no data points processed.
            - `start` (Optional[int]):
                Resets to None, indicating no defined start time.
            - `end` (Optional[int]):
                Resets to None, indicating no defined end time.
            - `step` (Optional[int]):
                Resets to None, indicating no defined step interval.

        Usage:
            Call this method whenever you need to clear the object's state,
            typically before reusing it for new operations.
        """
        self.lines: int = 0
        self.start: Optional[int] = None
        self.end: Optional[int] = None
        self.step: Optional[int] = None
        self.reader.props = None

    def timescale(self) -> np.ndarray:
        """
        Generate a time scale for the feed as a NumPy array.

        This method creates an evenly spaced array of time values in seconds,
        based on the configured step size and number of lines. It represents
        the time intervals associated with the data feed.

        Returns:
            np.ndarray: A 1D array of time values in seconds, starting at 0 and
                        incrementing by `self.step` for `self.lines` intervals.

        Raises:
            ValueError: If `step` is not set or `lines` is zero, indicating
                        that the necessary properties for generating a time
                        scale are not properly initialized.

        Example:
            If `step` is 10 and `lines` is 5, this method returns:
            `[0, 10, 20, 30, 40]`
        """
        if self.step is None or self.lines == 0:
            raise ValueError(
                "Step size and line count must be set "
                "before generating a timescale."
            )
        return np.arange(0, self.step * self.lines, self.step)

    def timestamps(self) -> np.ndarray:
        """
        Generate an array of timestamps for the feed as a NumPy array.

        This method calculates the timestamps by adding the `start` time to the
        generated time scale, providing absolute time values
        in seconds for eachinterval of the feed.

        Returns:
            np.ndarray: A 1D array of absolute time values in seconds, starting
                        from `self.start` and incrementing by `self.step` for
                        `self.lines` intervals.

        Raises:
            ValueError: If `self.start` is invalid or not properly initialized.
                        Validation is performed by `Ut.validate_timestamp`.

        Example:
            If `self.start` is 1700000000
            and the time scale is `[0, 10, 20, 30]`,
            this method returns:
            `[1700000000, 1700000010, 1700000020, 1700000030]`
        """
        Ut.validate_timestamp(self.start, 'win_start')
        return self.timescale() + self.start

    def read_fina_values(
        self,
        props: FinaByTimeParamsModel
    ) -> np.ndarray:
        """
        Read values from the Fina data file, either directly or averaged,
        based on the step interval.

        This method retrieves values from the Fina data file
        for a specified time range and step interval.
        If the `step` is less than or equal to the metadata interval,
        values are read directly.
        Otherwise, values within each `step` interval are averaged.

        Parameters:
            start (int): Start time in seconds from the feed's start time.
            step (int): Step interval in seconds for the data retrieval.
            window (int): Total time window to read in seconds.
            set_pos (bool):
                If True, updates the reader's position after reading.

        Returns:
            np.ndarray:
                A NumPy array containing either the raw values
                or averaged values.
                Missing data is represented by NaNs.

        Raises:
            ValueError: If the `start` time exceeds the feed's end time.

        Notes:
            - This method adapts its approach based on the relation
              between `step` and the feed's metadata interval.
            - For large `step` values,
              averaging within step intervals is performed
              for efficiency and clarity.
        """
        if props.start_time >= self.meta.end_time:
            raise ValueError(
                "Invalid start value. "
                "Start must be less than the feed's end time "
                "defined by start_time + (npoints * interval) from metadata."
            )
        interval = self.meta.interval
        # window = min(window, self.length)
        step = max(props.time_interval, interval)
        # npts = window // step
        if step <= interval:
            return self._read_direct_values(
                props=props
            )

        return self._get_averaged_values(
            props=props)

    def get_fina_values(
        self,
        props: FinaByTimeParamsModel
    ) -> np.ndarray:
        """
        Retrieve data values from the Fina data file
        for a specified time window.

        This method accesses the Fina data file to extract values
        within a given time window, starting from a specific time point
        and using a defined step interval.
        The method delegates the actual data reading to `read_fina_values`.

        Parameters:
            start (int):
                Start time in seconds, relative to the feed's start time.
            step (int): Step interval in seconds for sampling the data.
            window (int): Total time window in seconds to retrieve data.

        Returns:
            np.ndarray: A 1D NumPy array containing the retrieved values.
                        Missing data points are represented by NaNs.

        Notes:
            - The method ensures that the requested time window
            and step size are handled appropriately, including averaging
            if the step size exceeds the feed's interval.
            - It is essential to validate the `start`, `step`,
            and `window` parameters against the metadata to avoid errors.
            - The data extraction aligns with the metadata's time configuration
            (e.g., interval and start time).

        Raises:
            ValueError:
            If the `start` time is invalid or exceeds the feed's end time.
        """
        result = self.read_fina_values(
            props=props
        )
        # if n_decimals is not None:
        #    # Apply rounding/flooring only to the data columns
        #    if n_decimals == 0:
        #        result[:] = np.floor(result[:]).astype(int)
        #    elif n_decimals > 0:
        #        result[:] = np.around(result[:], decimals=n_decimals)

        return result

    def get_data_by_date(
        self,
        props: FinaByDateParamsModel
    ) -> np.ndarray:
        """
        Retrieve values from the Fina data file
        based on a specified date range.

        This method converts the given date range into a time window
        and retrieves the corresponding values from the data file.

        Parameters:
            start_date (str): Start date in string format.
            end_date (str): End date in string format.
            step (int): Step interval in seconds for data retrieval.
            date_format (str):
            Format of the input date strings. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            np.ndarray:
                A 1D NumPy array containing the retrieved values,
                with NaNs for missing data.

        Notes:
            - The `Ut.get_window_by_dates` method is used
              to compute the time range.
            - This method is useful for aligning data retrieval
              with specific time periods.
        """
        start_dt = Ut.get_utc_datetime_from_string(
            dt_value=props.start_date,
            date_format=props.date_format,
            timezone=dt.timezone.utc
        )

        return self.get_fina_values(
            props=FinaByTimeParamsModel(
                start_time=int(start_dt.timestamp()),
                time_window=props.time_window,
                time_interval=props.time_interval
            )
        )

    def get_data_by_date_range(
        self,
        props: FinaByDateParamsModel
    ) -> np.ndarray:
        """
        Retrieve a 2D time series array of timestamps
        and values for a specific date range.

        This method combines timestamps and corresponding values
        within the specified date range
        into a 2D array where each row represents a [timestamp, value] pair.

        Parameters:
            start_date (str): Start date in string format.
            end_date (str): End date in string format.
            step (int): Step interval in seconds for data retrieval.
            date_format (str):
                Format of the input date strings.
                Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            np.ndarray: A 2D NumPy array with shape (n, 2),
                        where the first column contains timestamps
                        and the second contains corresponding values.

        Notes:
            - Combines `get_fina_values_by_date`
              and `timestamps` to create the time series.
            - Useful for generating aligned time series data
              for specific date ranges.
        """
        start, window = Ut.get_window_by_dates(
            start_date=props.start_date,
            end_date=props.end_date,
            interval=self.meta.interval,
            date_format=props.date_format,
        )

        return self.read_fina_values(
            props=FinaByTimeParamsModel(
                start_time=start,
                time_window=window,
                time_interval=props.time_interval
            )
        )
