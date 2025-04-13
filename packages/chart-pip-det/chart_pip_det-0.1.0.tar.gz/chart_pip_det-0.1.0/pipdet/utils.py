from chartDL.utils.visual import plot_candlestick_chart
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def tight_box_normalize_df(
    df: pd.DataFrame, width: float = 1.62, height: float = 1.0
) -> pd.DataFrame:
    """
    Normalize the OHLC data in a DataFrame to fit within a tight box defined by width and height.

    Args:
        df (pd.DataFrame): DataFrame containing OHLC data.
        width (float): Width of the tight box. Default is 1.62.
        height (float): Height of the tight box. Default is 1.0.

    Returns:
        pd.DataFrame: A new DataFrame with normalized OHLC data and an added 'X' column.
    """

    ohlc_cols = ["Open", "High", "Low", "Close"]

    # Copy to avoid modifying original
    df_norm = df.copy()

    # Normalize Y-axis (OHLC)
    maximum = df_norm["High"].max()
    minimum = df_norm["Low"].min()

    df_norm[ohlc_cols] = height * (df_norm[ohlc_cols] - minimum) / (maximum - minimum)

    # Normalize X-axis
    df_norm["X"] = np.linspace(0, width, len(df_norm))

    return df_norm


def plot_pip_on_chart(
    df,
    color: str = "blue",
    title: str = None,
    ax=None,
    linewidth=1,
    marker="o",
    markersize=5,
):
    """
    Plot perceptually important points (PIP) on a candlestick chart.

    Args:
        df (pd.DataFrame): DataFrame containing market data and PIP information, with columns:
                           ['X', 'Open', 'High', 'Low', 'Close', 'is', 'coordX', 'coordY'].
        color (str): Color for the PIP points. Default is 'blue'.
        title (str): Title for the plot. Default is 'PIP Points on Chart'.
        ax (matplotlib.axes.Axes, optional): Axes object to plot on. If None, a new plot will be created.
        linewidth (float): Line width for the PIP line. Default is 1.
        marker (str): Marker style for PIP points. Default is 'o'.
        markersize (int): Size of the markers for PIP points. Default is 5.

    Returns:
        ax (matplotlib.axes.Axes): The axes object with the plot, for further customization or saving.
    """
    # Validate required columns in the DataFrame
    required_columns = {"X", "Open", "High", "Low", "Close", "is", "coordX", "coordY"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"The DataFrame is missing required columns: {missing_columns}"
        )

    # Create a new figure if no axes are provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Plot candlestick chart (ensure that plot_candlestick_chart is available in your environment)
    ax = plot_candlestick_chart(
        df, color="black", ax=ax, linewidth=linewidth, x_as_axis=True
    )

    # Extract PIP points from DataFrame
    mask = df["is"].astype(bool)
    pip_points = df.loc[mask, ["coordX", "coordY"]]

    # Plot the PIP points as a line or scatter
    ax.plot(
        pip_points["coordX"],
        pip_points["coordY"],
        color=color,
        linewidth=linewidth,
        label="PIP Points",
        marker=marker,
        markersize=markersize,
    )

    # Add title if specified
    if title is not None:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Set axis to be tight for better visualization
    ax.axis("tight")

    # Add legend for clarity
    ax.legend()

    return ax  # Return the axes object for further customization


def plot_pip_score(
    df,
    color: str = "blue",
    title: str = None,
    ax=None,
    linewidth=1,
    marker="o",
    max_markersize=30,
):
    """
    Visualize PIP points on a candlestick chart with distance from segment as scores represented by marker size.

    Args:
        df (pd.DataFrame): DataFrame containing columns ["X", "Open", "High", "Low", "Close", "dist", "hilo"].
        color (str): Line color for candlestick chart.
        title (str): Title for the chart.
        ax (matplotlib.axes.Axes): Pre-existing axes for the plot. If None, creates a new one.
        linewidth (float): Width of the candlestick lines.
        marker (str): Marker style for PIP points.
        max_markersize (int): Maximum size for markers, scaled by score.

    Returns:
        matplotlib.axes.Axes: The axes object containing the plot.
    """

    # Validate required columns in the DataFrame
    required_columns = {"X", "Open", "High", "Low", "Close", "dist", "hilo"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"The DataFrame is missing required columns: {missing_columns}"
        )

    # Create a new figure if no axes are provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Plot candlestick chart (ensure that plot_candlestick_chart is available in your environment)
    ax = plot_candlestick_chart(
        df, color="black", ax=ax, linewidth=linewidth, x_as_axis=True
    )

    # Extract points data for visualization
    x_data = df["X"].to_numpy()
    hi = df["High"].to_numpy()
    lo = df["Low"].to_numpy()
    hilo = df["hilo"].to_numpy()
    score = df["dist"].to_numpy()

    # Calculate y_data by selecting values from "High" or "Low" based on the "hilo" flag
    # If hilo > 0.5, use "High" values, otherwise use "Low" values.
    y_data = (hilo > 0.5) * hi + (hilo <= 0.5) * lo

    # Define marker sizes based on the normalized scores
    sizes = max_markersize * score / score.max()

    # Scatter plot for PIP points
    ax.scatter(
        x_data, y_data, s=sizes, c="red", alpha=0.7, edgecolors="none", marker=marker
    )

    # Add title if specified
    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")

    # Set axis to be tight for better visualization
    ax.axis("tight")

    return ax  # Return the axes object for further customization
