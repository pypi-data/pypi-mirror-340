# chart-pip-det

## 📈 Generating Pip Data for ML/DL

This Python package is designed to extract perceptually important points (pips) from financial market OHLC (Open, High, Low, Close) charts. By analyzing market price movements at a granular level, it generates pip-level data that can be used to build datasets for machine learning (ML) and deep learning (DL) models focused on financial analysis, technical analysis patterns, and market prediction.

The package is optimized for speed and accuracy, making it ideal for both rapid analysis and large-scale data processing. It provides key insights into market behavior and geometric properties, offering a solid foundation for training models to recognize patterns and predict market trends.

![Pip importance of points](images/pip_score.png)

The example shows pip points on an OHLC chart. Red circles represent the depth of each pip point, with the size indicating the depth or perceptual importance of the point. Larger circles represent more significant pip points.

![Pip line segments](images/pip_segment_line.png)

Pip points are conceptually important in geometry as they highlight key turning points in market price movements. By identifying these points, we can simplify chart patterns and recognize critical market structures more easily.

## 🔑 Key Features

**📊 Generating Data for ML/DL**  
Generating Data for ML/DL: Automatically generates pip data and creates datasets tailored for machine learning and deep learning models focused on market analysis and predictions, also be compatible with deep learning data loaders (e.g., PyTorch, TensorFlow).

**🔍 Efficient Pip Detection**  
Detects pip points quickly and provides a complete data view of pip point information, including position and perceptual importance data.

**📉 Technical Analysis Focused & Easy to Use**  
Optimized for technical analysis, the package is user-friendly and designed to simplify pip point detection for market chart analysis.

## 🚀 Installation

**📦 Option 1: Install via pip**
```bash
pip install chart-pip-det
```
**🛠 Option 2: Clone and install manually**
```bash
git clone https://github.com/mehranESB/chart-pip-detector.git
cd chart-pip-detector
python setup.py install
```

## 📚 Usage Guide

**1️⃣ Finding Pip Points on Market Chart**

In the example below, we demonstrate how to find pip points in a financial market chart using normalized OHLC data. The OHLC data represents the y-coordinates (price values), while an additional 'X' column is added to represent the x-coordinates (time) in 2D space. This normalization allows for a more comprehensive view of the market's price movement.

```python
from pipdet.pip import FastPip
from chartDL.utils.csv import import_ohlcv_from_csv
from pathlib import Path
import numpy as np

# Import source DataFrame
csv_source_path = Path("./DATA/csv/EURUSD-1h.csv")
df_source = import_ohlcv_from_csv(
    csv_source_path, header=True, datetime_format="%Y-%m-%d %H:%M:%S"
)

# get ohlcv sample data and normalize it
data_len = 128
market_data = df_source.loc[:data_len, ["Open", "High", "Low", "Close"]]
low_min = market_data["Low"].min()
high_max = market_data["High"].max()
market_data = (market_data - low_min) / (high_max - low_min)
market_data["X"] = np.linspace(0, 1, data_len)

# initialize pip finder and find pip points
pip_finder = FastPip(market_data, dist_method="perpendicular", num_points=10)
market_data_with_pip = pip_finder.find_pips(dtype="df", time_it=True) # a table with all pip information data
```

**2️⃣ Generating Pip Information for a Dataset**

We demonstrate how to generate pip information for a dataset and save it as a `.pkl` file. The process is customizable, allowing you to specify custom column names for the pip information and adjust the index increment or skip over data points in the source.

```python
from pipdet.pipgen import generate_pip
from pathlib import Path

# Path to the CSV file containing the market OHLCV data
csv_path = Path("./DATA/csv/EURUSD-1h.csv")

# Path where the generated PIP data will be saved (in .pkl format)
save_path = Path("./DATA/pip/EURUSD-1h.pkl")
save_path.parent.mkdir(parents=True, exist_ok=True)

# Generate the PIP points and distances
generate_pip(csv_path, pip_info_to_save=["dist", "hilo"],
    seq_len=128, inc_index=20, dist_method="perpendicular",
    save_path=save_path
)
```

**3️⃣ Creating a Dataset for PyTorch**

In this example, we demonstrate how to create a combined dataset from multiple pip data files and prepare it for training by using a PyTorch `DataLoader`.

```python
from pipdet.dataset import PipDataset, CombinedDataset
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

class CustomDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = dataset  # store to use it as data source

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        pip_data = self.dataset[index]

        retrive_data = {
            "input": pip_data[["High", "Low", "X"]].to_numpy(),
            "target": pip_data[["dist", "hilo"]].to_numpy(),
        }

        return retrive_data

# Define the paths to the .pkl files containing PipDatasets
pkl_path1 = Path("./DATA/pip/EURUSD-1h.pkl")
pkl_path2 = Path("./DATA/pip/EURUSD-15m.pkl")

# Load the PipDatasets and Combine the PipDatasets into a single CombinedDataset
dataset1 = PipDataset(pkl_path1)
dataset2 = PipDataset(pkl_path2)
combined_dataset = CombinedDataset([dataset1, dataset2])

# Split the combined dataset into training (80%), validation (15%), and testing (5%)
train_ds, valid_ds, test_ds = combined_dataset.split(0.8, 0.15)

# Create a DataLoader for batching and shuffling
data_loader = DataLoader(CustomDataset(train_ds), batch_size=64, shuffle=True)

# Iterate through batches during model training
for batch in data_loader:
    ...
```
**🧪 Explore More**

For more examples and detailed usage, check the `example/` folder in the repository.

## 🤝 Contributing
Contributions are welcome and appreciated!

Feel free to fork the repository, submit pull requests, or open issues for bugs, feature suggestions, or improvements.

## 📄 License
This project is licensed under the MIT License.
See the `LICENSE.txt` file for details.