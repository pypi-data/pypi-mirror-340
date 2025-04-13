import pandas as pd
import numpy as np
import time


def distance_to_segment(point, p1, p2, mode="perpendicular"):
    """
    Compute the distance of a point from a line segment.

    Parameters:
    - point: A tuple (x, high, low) representing the coordinates of the point.
    - p1: A tuple (x1, y1) representing the start of the line segment.
    - p2: A tuple (x2, y2) representing the end of the line segment.
    - mode: Either "perpendicular" or "vertical", indicating the type of distance to compute.

    Returns:
    - distance: The calculated distance from the point to the segment.
    - LenChange: The change in segment length if the point is added to the segment.
    - coord: The coordinate of the point on the segment (either high or low).
    """
    x, high, low = point  # Coordinates of the data point
    x1, y1 = p1  # Start of the segment
    x2, y2 = p2  # End of the segment

    # Calculate the vector for the segment and its squared length
    dx, dy = (x2 - x1), (y2 - y1)
    seg_len2 = dx**2 + dy**2  # Squared length of the segment

    # Handle zero-length segment case (p1 and p2 must be distinct)
    if seg_len2 == 0:
        raise ValueError(
            "The segment length is equal to zero. p1 and p2 must be distinct."
        )

    # Vectors connecting the point to the segment endpoints and their squared lengths
    dx_left, dy_left_hi, dy_left_lo = (x - x1), (high - y1), (low - y1)
    left_len_hi2 = dx_left**2 + dy_left_hi**2  # Length squared to high value
    left_len_lo2 = dx_left**2 + dy_left_lo**2  # Length squared to low value

    if mode == "perpendicular":
        # Perpendicular squared distances from high/low to the segment
        pp_dist_hi2 = left_len_hi2 - (dx_left * dx + dy_left_hi * dy) ** 2 / seg_len2
        pp_dist_lo2 = left_len_lo2 - (dx_left * dx + dy_left_lo * dy) ** 2 / seg_len2
        dist_hi = np.sqrt(np.abs(pp_dist_hi2))
        dist_lo = np.sqrt(np.abs(pp_dist_lo2))

    elif mode == "vertical":
        # Vertical distances (absolute difference from projected y)
        alpha = dy / dx
        beta = y1 - alpha * x1
        y_interp = alpha * x + beta
        dist_hi = np.abs(high - y_interp)
        dist_lo = np.abs(low - y_interp)

    else:
        raise ValueError("Invalid mode. Use 'perpendicular' or 'vertical'.")

    # Determine which value (high or low) has the greater distance
    if dist_hi > dist_lo:  # High value dominates
        dx_right, dy_right_hi = (x2 - x), (y2 - high)
        right_len_hi2 = dx_right**2 + dy_right_hi**2

        distance = dist_hi
        LenChange = (np.sqrt(left_len_hi2) + np.sqrt(right_len_hi2)) - np.sqrt(seg_len2)

        # Flag for high value
        y = high
        hilo = 1.0

    else:  # Low value dominates
        dx_right, dy_right_lo = (x2 - x), (y2 - low)
        right_len_lo2 = dx_right**2 + dy_right_lo**2

        distance = dist_lo
        LenChange = (np.sqrt(left_len_lo2) + np.sqrt(right_len_lo2)) - np.sqrt(seg_len2)

        # Flag for low value
        y = low
        hilo = 0.0

    coord = np.array([x, y])  # Coordinate of the point on the segment

    # Return the distance, length change, and the point's coordinates (high or low)
    return distance, LenChange, coord, hilo


class FastPip:
    def __init__(
        self,
        market_data: pd.DataFrame,
        dist_method: str = "perpendicular",
        num_points=None,
    ):
        """
        Initialize the FastPip class to detect perceptually important points (pips) in a price series.

        Parameters:
        - market_data: A pandas dataframe object containing 'Open', 'High', 'Low', 'Close' columns.
        - dist_method: Either "perpendicular" or "vertical", indicating the type of distance to compute.
        - num_points: Number of perceptually important points to detect. If None, defaults to all data points.
        """
        # Validate market_data
        required_columns = ["Open", "High", "Low", "Close"]
        if not set(required_columns).issubset(market_data.columns):
            missing_columns = set(required_columns) - set(market_data.columns)
            raise ValueError(
                f"Market data is missing required columns: {missing_columns}"
            )

        # Number of data points
        num_data = len(market_data)
        if num_data < 2:
            raise ValueError("Market data must contain at least 2 data points.")

        # Handle the case when num_points is provided or set to default
        if num_points is None:
            num_points = num_data
        elif num_points < 2 or num_points > num_data:
            raise ValueError(
                f"Number of points must be between 2 and {num_data}, inclusive."
            )

        # validate distance method
        if dist_method not in {"perpendicular", "vertical"}:
            raise ValueError(
                f"dist_method must be 'perpendicular' or 'vertical', got '{dist_method}'"
            )

        # Input data
        self.market_data = market_data
        self.num_data = num_data
        self.num_points = num_points
        self.dist_method = dist_method

        # Extracted data for fast access
        numpy_data = market_data.loc[:, required_columns].values
        self.op, self.hi, self.lo, self.cl = (
            numpy_data[:, 0],
            numpy_data[:, 1],
            numpy_data[:, 2],
            numpy_data[:, 3],
        )

        # Set x-axis values: use 'X' column if it exists, otherwise default to linspace between 0 and 1
        if "X" in market_data.columns:
            self.x = market_data["X"].to_numpy()
        else:
            self.x = np.linspace(0, 1, num_data)

        # Global variable for polyline length and iteration counter
        self.poly_line_len = None
        self.iterator = 0

        # Per-point information storage
        self.pip = {
            "is": np.full(num_data, False, dtype=bool),  # Whether point is a "pip"
            "iter": np.full(num_data, 0, dtype=int),  # pip point's found iteration
            "dist": np.full(num_data, 0.0),  # point's distance to segment
            "coordX": np.full(num_data, np.nan),  # pip point's x coordiante
            "coordY": np.full(num_data, np.nan),  # pip point's y coordiante
            "lenChng": np.full(num_data, 0.0),  # chenge in pip polyline
            "growth": np.full(num_data, 0.0),  # percentage of pip polyline growth
            "totLen": np.full(num_data, np.nan),  # pip polyline's length
            "hilo": np.full(num_data, 0.0),  # pip is high(1) or low(0)
        }

    def initialize(self):
        """Initialize the first and last points and compute distances for the initial segment."""

        # First point of the initial segment (x[0], Open[0])
        p1 = np.array([self.x[0], self.op[0]])  # (x[0], Open[0])
        self.pip["is"][0] = True  # Mark the first point as a pip
        self.pip["coordX"][0], self.pip["coordY"][0] = p1  # Store coordinates

        # Second point of the initial segment (x[-1], Close[-1])
        p2 = np.array([self.x[-1], self.cl[-1]])  # (x[-1], Close[-1])
        self.pip["is"][-1] = True  # Mark the last point as a pip
        self.pip["coordX"][-1], self.pip["coordY"][-1] = p2  # Store coordinates

        # Calculate the distance for each point relative to the initial segment
        for i in range(1, self.num_data - 1):
            point = (
                self.x[i],
                self.hi[i],
                self.lo[i],
            )  # Use high and low for comparison
            # Get distance, length change, and new coordinates for each point
            (
                self.pip["dist"][i],
                self.pip["lenChng"][i],
                (self.pip["coordX"][i], self.pip["coordY"][i]),
                self.pip["hilo"][i],
            ) = distance_to_segment(point, p1, p2, mode=self.dist_method)

        # Initialize length of pip polyline (distance between the first and last points)
        seg_len = np.linalg.norm(p2 - p1)
        self.poly_line_len = seg_len  # Store the initial polyline length

        # Initialize first and last point of the segment with their lengths and growth
        # The change in length at the first and last point
        self.pip["lenChng"][[0, -1]] = seg_len
        # Total length of the polyline up to these points
        self.pip["totLen"][[0, -1]] = seg_len
        # Growth percentage at the first and last point
        self.pip["growth"][[0, -1]] = 100.0
        # High-LOw flag at the first and last point
        self.pip["hilo"][[0, -1]] = 0.5

    def next_pip(self):
        """
        Find the next pip point by selecting the maximum distance point.

        Returns:
            float: Mean distance of non-PIP points to the PIP polyline. Useful for threshold-based stopping.
        """

        # Get the index of the point with the maximum distance from the segment but is not pip point
        index = np.argmax(self.pip["dist"] - 1e9 * self.pip["is"])
        self.pip["is"][index] = True  # Mark this point as a pip

        # Compute growth percentage
        self.pip["growth"][index] = (
            100.0 * self.pip["lenChng"][index] / self.poly_line_len
        )

        # Update the polyline length to the total length at the selected point
        self.poly_line_len += self.pip["lenChng"][index]
        self.iterator += 1  # Increment the iteration counter

        # Record the iteration number for this pip point
        self.pip["iter"][index] = self.iterator
        self.pip["totLen"][index] = self.poly_line_len

        # Get the indices of all pips
        pip_indices = np.where(self.pip["is"])[0]

        # Get the closest pip point to the left of the current pip
        if not np.any(pip_indices < index):
            raise IndexError(f"There is no pip point to the left of index {index}.")
        closest_left = pip_indices[pip_indices < index][-1]

        # Recompute distances between the closest left pip and the selected pip if there are intermediate points
        if (index - closest_left) > 1:
            p1 = (self.pip["coordX"][closest_left], self.pip["coordY"][closest_left])
            p2 = (self.pip["coordX"][index], self.pip["coordY"][index])
            for i in range(closest_left + 1, index):
                point = (self.x[i], self.hi[i], self.lo[i])  # Using high and low values
                (
                    self.pip["dist"][i],
                    self.pip["lenChng"][i],
                    (self.pip["coordX"][i], self.pip["coordY"][i]),
                    self.pip["hilo"][i],
                ) = distance_to_segment(point, p1, p2, mode=self.dist_method)

        # Get the closest pip point to the right of the current pip
        if not np.any(pip_indices > index):
            raise IndexError(f"There is no pip point to the right of index {index}.")
        closest_right = pip_indices[pip_indices > index][0]

        # Recompute distances between the selected pip and the closest right pip if there are intermediate points
        if (closest_right - index) > 1:
            p1 = (self.pip["coordX"][index], self.pip["coordY"][index])
            p2 = (self.pip["coordX"][closest_right], self.pip["coordY"][closest_right])
            for i in range(index + 1, closest_right):
                point = (self.x[i], self.hi[i], self.lo[i])  # Using high and low values
                (
                    self.pip["dist"][i],
                    self.pip["lenChng"][i],
                    (self.pip["coordX"][i], self.pip["coordY"][i]),
                    self.pip["hilo"][i],
                ) = distance_to_segment(point, p1, p2, mode=self.dist_method)

        # return distance between pip polyline and current choosed pip point
        return self.pip["dist"][index]

    def find_pips(
        self, time_it: bool = False, dtype: str = "df", threshold: float = None
    ):
        """
        This method identifies perceptually important points (PIPs) and normalizes related features.

        Args:
            time_it (bool): If True, prints the time taken to find the PIPs.
            dtype (str): Specifies the format of the exported data. Default is "df" (DataFrame).
            threshold (float): Minimum mean distance threshold for stopping PIP selection.
                               Default is None, which disables the threshold check.

        Returns:
            DataFrame or other type: The data in the format specified by `dtype`.
        """

        # Default threshold to -inf if not provided, ensuring no stopping based on distance
        threshold = -np.inf if threshold is None else threshold

        # Record the start time for performance measurement
        start_time = time.perf_counter()

        # Initialize PIP operator: sets up data structures and variables needed for PIP calculation
        self.initialize()

        # Iteratively find PIPs until the desired number of points is selected or threshold is reached
        while np.count_nonzero(self.pip["is"]) < self.num_points:
            # Find the next PIP and retrieve the mean distance
            thr = self.next_pip()

            # Check if the mean distance is below the threshold; if so, stop adding PIPs
            if thr < threshold:
                break

        # Record the end time for performance measurement
        end_time = time.perf_counter()

        # If timing is enabled, print the time taken for the PIP process
        if time_it:
            elapsed_time = end_time - start_time
            print(f"PIP Time taken: {elapsed_time:.4f} seconds")

        # Export the results in the specified format (e.g., DataFrame, dictionary)
        return self.export_data(dtype=dtype)

    def export_data(self, dtype: str = "dict"):
        """
        Exports data in different formats based on the specified dtype.

        Args:
            dtype (str): The format in which to export the data. Options are:
                - 'dict': Returns the data as a dictionary of numpy arrays.
                - 'data': Returns the market data object with the additional pip data.
                - 'df': Returns the data as a pandas DataFrame.

        Returns:
            Depending on dtype:
                - dict: A dictionary containing 'pip' data as numpy arrays.
                - data: The market data object with pip data added.
                - df: A pandas DataFrame with the market data and pip data.

        Raises:
            ValueError: If an unsupported dtype is provided.
        """

        dtype = dtype.lower()  # Convert dtype to lowercase to handle case insensitivity

        # Prepare the data to be exported by adding extra pip data
        for key, val in self.pip.items():
            self.market_data[key] = val

        if dtype == "dict":
            # Return the data as a dictionary of numpy arrays
            return self.pip

        elif dtype == "data":
            # Return the market data with the extra pip data
            return self.market_data.to_numpy()

        elif dtype == "df":
            # Return the data as a pandas DataFrame
            return self.market_data

        else:
            raise ValueError(
                f"Unsupported dtype: '{dtype}'. Choose from 'dict', 'data', or 'df'."
            )
