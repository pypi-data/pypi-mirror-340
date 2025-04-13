from .pip import FastPip
from .utils import tight_box_normalize_df
from chartDL.utils import csv as csv_utils
from chartDL.dataset import SingleDataset
import numpy as np
from pathlib import Path
from tqdm import tqdm
import pickle


def create_single_dataset(csv_path: str, seq_len: int = 128):
    """
    Create a single dataset object to retrieve OHLCV data from a source CSV file.

    Args:
        csv_path (str): The path to the CSV file containing OHLCV market data.
        seq_len (int): The length of the sequence for each data sample. Default is 128.

    Returns:
        SingleDataset: A dataset object containing OHLCV data.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """
    # Convert csv_path to a Path object if it is not already one
    csv_path = Path(csv_path)

    # Check if the file exists
    if not csv_path.exists():
        raise FileNotFoundError(f"File not found: {csv_path}")

    # Import OHLCV data from the CSV file
    df_source = csv_utils.import_ohlcv_from_csv(
        csv_path, header=True, datetime_format="%Y-%m-%d %H:%M:%S"
    )

    # Create and return the dataset object
    dataset = SingleDataset(df_source, seq_len)
    return dataset, df_source


def generate_pip(
    csv_path: str,
    pip_info_to_save: list[str],
    seq_len: int = 128,
    inc_index: int = 20,  # Increment step for selecting samples
    dist_method: str = "perpendicular",
    norm_width: float = 1.62,
    norm_height: float = 1.0,
    save_path: str = "pip_data.pkl",
):
    """
    Generate perceptually important points (PIP) for a dataset,
    and save the results to a file for efficient later use.

    Args:
        csv_path (str): Path to the CSV file containing OHLCV data.
        pip_info_to_save (list[str]): list of pip information dict's feilds to save.
        seq_len (int): Sequence length for each sample in the dataset. Default is 128.
        inc_index (int): Increment step for selecting samples from the dataset. Default is 20.
        dist_method (str): Distance calculation method for PIP detection. Default is 'perpendicular'.
        norm_width (float): Normalized width for scaling data during normalization. Default is 1.62.
        norm_height (float): Normalized height for scaling data during normalization. Default is 1.0.
        save_path (str): File path to save the packed results (must be .pkl file). Default is "pip_data.pkl".

    Returns:
        dict: A dictionary containing the packed data.
    """

    # Create the dataset
    dataset, df_source = create_single_dataset(csv_path, seq_len)

    # check save_path to be pickle file
    if save_path is not None and save_path.suffix != ".pkl":
        raise ValueError("The save_path must have a '.pkl' file extension.")

    # Generate indices for samples based on the increment step
    sample_index = range(0, len(dataset), inc_index)

    # initialize memory for storing results
    sz = (len(pip_info_to_save), seq_len, len(sample_index))
    pip_results = np.full(sz, np.nan, dtype=np.float32)

    # Use tqdm to track progress through the loop
    for i, idx in enumerate(
        tqdm(sample_index, desc="Generating PIP scores", unit="sample")
    ):
        # Retrieve the data sample from the dataset
        data = dataset[idx]

        # Normalize the data and convert into dataframe
        normalized_data = tight_box_normalize_df(
            data, width=norm_width, height=norm_height
        )

        # Initialize FastPip for detecting PIPs
        fast_pip = FastPip(normalized_data, dist_method=dist_method)

        # Find PIP points and retrieve their associated data
        pip_data = fast_pip.find_pips(time_it=False, dtype="df")

        # store results
        for ii, key in enumerate(pip_info_to_save):
            pip_results[ii, :, i] = pip_data[key].to_numpy()

    # Pack the results into a dictionary
    packed_data = {
        "df_source": df_source,
        "pip_results": pip_results,
        "seq_len": seq_len,
        "norm_width": norm_width,
        "norm_height": norm_height,
        "indexes": list(sample_index),  # Convert range to list for serialization
        "pip_info_to_save": pip_info_to_save,
    }

    # save data
    save_path = Path(save_path)
    with open(save_path, "wb") as file:
        pickle.dump(packed_data, file)

    print(f"Packed data saved to {save_path}")
