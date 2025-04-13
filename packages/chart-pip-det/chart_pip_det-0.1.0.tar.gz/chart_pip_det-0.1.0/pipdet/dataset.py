from chartDL.dataset import SingleDataset
from .utils import tight_box_normalize_df
from pathlib import Path
import pickle
import numpy as np


class PipDataset:
    def __init__(self, pkl_path: str):
        """
        This class loads a PIP dataset from a pickled file, reconstructs the dataset, and prepares necessary
        fields for training or evaluation.

        Args:
            pkl_path (str): The file path to the pickled dataset.
            transforms (list): A list of transformation functions to apply to the data (default is an empty list).
            return_type(str): define type of return data that could be {"data" -> Data, "dict" -> dict, "tuple" -> tuple, "train" -> tuple}
        """

        # Ensure the provided file exists
        if not Path(pkl_path).exists():
            raise FileNotFoundError(f"The pickle file at {pkl_path} was not found.")

        # Load the pickled data from the file
        try:
            with open(pkl_path, "rb") as f:
                loaded_data = pickle.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load or unpickle data from {pkl_path}: {e}")

        # Check if necessary keys are present in the loaded data
        expected_keys = [
            "df_source",
            "seq_len",
            "norm_width",
            "norm_height",
            "indexes",
            "pip_info_to_save",
        ]
        for key in expected_keys:
            if key not in loaded_data:
                raise KeyError(f"Missing key in the loaded pickle file: {key}")

        # Recreate the dataset using the loaded data
        self.dataset = SingleDataset(loaded_data["df_source"], loaded_data["seq_len"])
        self.seq_len = loaded_data["seq_len"]

        # Load sample data indexes and pip informations that are saved
        self.indexes = loaded_data["indexes"]
        self.pip_results = loaded_data["pip_results"]
        self.pip_results_rows = loaded_data["pip_info_to_save"]

        # Create normalizer function using provided normalization parameters
        self.norm_fun = lambda x: tight_box_normalize_df(
            x, width=loaded_data["norm_width"], height=loaded_data["norm_height"]
        )
        self.norm_width = loaded_data["norm_width"]
        self.norm_height = loaded_data["norm_height"]

    def __getitem__(self, idx):
        """
        Retrieve the data at a specific index. This method returns the normalized data and the corresponding score.

        Args:
            idx (int): The index of the data point to retrieve.

        Returns:
            tuple: A tuple containing the transformed data and the corresponding score.
        """
        # Check if idx is within valid range
        if idx < 0 or idx >= len(self.indexes):
            raise IndexError(f"Index {idx} is out of bounds.")

        # Retrieve the raw data from the dataset using the index
        data = self.dataset[self.indexes[idx]]

        # Normalize the data using the normalization function
        normalized_data = self.norm_fun(data)

        # attached pip information into data
        for i, key in enumerate(self.pip_results_rows):
            normalized_data[key] = self.pip_results[i, :, idx]

        return normalized_data

    def __len__(self):
        """
        Return the number of samples in the dataset (based on the number of indexes).

        Returns:
            int: The number of samples in the dataset.
        """
        return len(self.indexes)

    def split(self, train_ratio: float, val_ratio: float):
        """
        Split the dataset into train, validation, and test sets.

        Args:
            train_ratio (float): Proportion of the dataset to use for training.
            val_ratio (float): Proportion of the dataset to use for validation.

        Returns:
            tuple: Three new PipDataset instances for train, validation, and test sets.
        """

        if not (0 <= train_ratio <= 1 and 0 <= val_ratio <= 1):
            raise ValueError("train_ratio and val_ratio must be between 0 and 1.")
        if train_ratio + val_ratio > 1:
            raise ValueError("train_ratio + val_ratio cannot exceed 1.")

        # Calculate sizes
        total_len = len(self)
        train_len = int(total_len * train_ratio)
        val_len = int(total_len * val_ratio)

        # Shuffle indices
        indices = np.random.permutation(total_len)

        # Split indices
        train_indices = indices[:train_len]
        val_indices = indices[train_len : train_len + val_len]
        test_indices = indices[train_len + val_len :]

        # Create new datasets
        train_dataset = PipDatasetSubset(self, train_indices)
        val_dataset = PipDatasetSubset(self, val_indices)
        test_dataset = PipDatasetSubset(self, test_indices)

        return train_dataset, val_dataset, test_dataset


class PipDatasetSubset(PipDataset):
    """
    A subset of a PipDataset defined by specific indices.

    This class allows creating a smaller dataset from a larger PipDataset by
    selecting only a specific subset of indices. The subset behaves like a
    full PipDataset but contains data only for the provided indices.

    Attributes:
        dataset (SingleDataset): The original dataset containing the raw OHLCV data.
        indexes (list[int]): A list of indices corresponding to the subset of the parent dataset.
        scores (np.ndarray): The PIP distance scores for the subset.
        norm_fun (function): A normalization function inherited from the parent dataset.
    """

    def __init__(self, parent_dataset: PipDataset, indices: np.ndarray):
        """
        Initialize a PipDatasetSubset instance.

        Args:
            parent_dataset (PipDataset): The original PipDataset from which the subset is derived.
            indices (np.ndarray): A list or array of indices specifying the subset.
        """
        # Use the dataset object from the parent PipDataset, so raw OHLCV data is not duplicated
        self.dataset = parent_dataset.dataset

        # Filter the parent indexes to only include those specified in `indices`
        self.indexes = [parent_dataset.indexes[i] for i in indices]

        # Extract the PIP information
        self.pip_results = parent_dataset.pip_results[:, :, indices]
        self.pip_results_rows = parent_dataset.pip_results_rows

        # Inherit the normalization function from the parent dataset
        self.norm_fun = parent_dataset.norm_fun


class CombinedDataset:
    """
    A class for combining multiple PipDataset instances into a single unified dataset.

    Args:
        datasets (list[PipDataset]): A list of PipDataset instances to combine.

    Attributes:
        datasets (list[PipDataset]): The combined list of datasets.
        dataset_offsets (list[int]): Precomputed cumulative lengths of the datasets
                                     to allow efficient index mapping.
    """

    def __init__(self, datasets: list[PipDataset]):

        if not datasets:
            raise ValueError("The list of datasets cannot be empty.")

        # Ensure all items in the list are instances of PipDataset
        if not all(isinstance(ds, PipDataset) for ds in datasets):
            raise TypeError(
                "All elements in the datasets list must be instances of PipDataset."
            )

        self.datasets = datasets

        # Precompute dataset offsets for efficient index mapping
        self.dataset_offsets = [0]
        for ds in datasets:
            self.dataset_offsets.append(self.dataset_offsets[-1] + len(ds))

    def __getitem__(self, idx):
        """
        Retrieve a data sample from the combined datasets based on a global index.

        Args:
            idx (int): The global index of the sample to retrieve.

        Returns:
            tuple: A tuple containing the normalized data and the corresponding score.

        Raises:
            IndexError: If the provided index is out of range.
        """
        if idx < 0 or idx >= len(self):
            raise IndexError(
                f"Index {idx} is out of range for CombinedDataset with length {len(self)}."
            )

        # Identify which dataset the index belongs to
        for i, offset in enumerate(self.dataset_offsets[:-1]):
            if idx < self.dataset_offsets[i + 1]:
                dataset_idx = idx - offset
                return self.datasets[i][dataset_idx]

    def __len__(self):
        """
        Return the total number of samples in the combined datasets.

        Returns:
            int: The total length of the combined datasets.
        """
        return self.dataset_offsets[-1]

    def split(self, train_ratio: float, val_ratio: float):
        """
        Split the combined dataset into train, validation, and test sets.

        Args:
            train_ratio (float): Proportion of the dataset to use for training.
            val_ratio (float): Proportion of the dataset to use for validation.

        Returns:
            tuple: Three new CombinedDataset instances for train, validation, and test sets.
        """
        train_splits, val_splits, test_splits = [], [], []

        for ds in self.datasets:
            train_ds, val_ds, test_ds = ds.split(train_ratio, val_ratio)
            train_splits.append(train_ds)
            val_splits.append(val_ds)
            test_splits.append(test_ds)

        return (
            CombinedDataset(train_splits),
            CombinedDataset(val_splits),
            CombinedDataset(test_splits),
        )
