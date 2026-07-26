from pathlib import Path
import pandas as pd

# Project root
ROOT = Path(__file__).resolve().parent.parent

# Dataset path
DATASET_PATH = ROOT / "datasets" / "iot_dataset.csv"

print("Looking for dataset at: - explore.py:10")
print(DATASET_PATH)

print("\nFile Exists: - explore.py:13", DATASET_PATH.exists())

if not DATASET_PATH.exists():
    raise FileNotFoundError(f"Dataset not found:\n{DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)

print("\n✅ Dataset Loaded Successfully! - explore.py:20")

print("\nShape: - explore.py:22")
print(df.shape)

print("\nColumns: - explore.py:25")
print(df.columns.tolist())

print("\nFirst 5 Rows: - explore.py:28")
print(df.head())

print("\nLast Column: - explore.py:31")
print(df.columns[-1])

print("\nUnique Classes: - explore.py:34")
print("\nUnique Classes:")
print(df["label"].value_counts())

print("\nNumber of Classes:")
print(df["label"].nunique())

print("\nClass Names:")
print(df["label"].unique())