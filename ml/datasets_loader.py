import os
import pandas as pd


CACHE_DIR = "cache"


def _cache_path(csv_path: str) -> str:
    base = os.path.basename(csv_path).replace(".csv", ".parquet")
    return os.path.join(CACHE_DIR, base)


def load_dataset(csv_path: str, use_cache: bool = True) -> pd.DataFrame:
    """
    Load a single dataset CSV file, with optional parquet caching
    for faster repeated loads (CICIoT2023 CSVs are large, so this
    saves significant time during development/iteration).
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset file not found: {csv_path}\n"
            f"Download CICIoT2023 from https://www.unb.ca/cic/datasets/iotdataset-2023.html "
            f"or the Kaggle mirror, and place CSVs in the expected folder."
        )

    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = _cache_path(csv_path)

    if use_cache and os.path.exists(cache_file):
        print(f"Loading cached version: {cache_file}")
        return pd.read_parquet(cache_file)

    print(f"Loading raw CSV: {csv_path}")
    df = pd.read_csv(csv_path)

    if use_cache:
        df.to_parquet(cache_file)
        print(f"Cached to: {cache_file}")

    return df


def load_multiple_datasets(csv_paths: list[str], use_cache: bool = True) -> pd.DataFrame:
    """Load and concatenate several dataset files, skipping any that fail to load."""
    frames = []
    for path in csv_paths:
        try:
            frames.append(load_dataset(path, use_cache=use_cache))
        except FileNotFoundError as e:
            print(f"Skipping missing file: {e}")

    if not frames:
        raise RuntimeError("No valid dataset files were loaded.")

    combined = pd.concat(frames, ignore_index=True)
    print(f"Combined dataset shape: {combined.shape}")
    return combined


def validate_dataset(df: pd.DataFrame, expected_label_col: str = "label") -> bool:
    """Basic sanity checks before training — catches silent data issues early."""
    issues = []

    if expected_label_col not in df.columns:
        issues.append(f"Missing expected label column: '{expected_label_col}'")

    if df.empty:
        issues.append("Dataset is empty.")

    null_ratio = df.isna().mean().mean()
    if null_ratio > 0.5:
        issues.append(f"More than 50% of values are missing (null_ratio={null_ratio:.2f})")

    if issues:
        print("Dataset validation FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("Dataset validation passed.")
    return True


def list_available_datasets(folder: str = "dataset") -> list[str]:
    """List all CSV files available in the dataset folder."""
    if not os.path.exists(folder):
        return []
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")]


if __name__ == "__main__":
    available = list_available_datasets()
    print("Available dataset files:", available)

    if available:
        df = load_multiple_datasets(available[:2])  # load first 2 for a quick check
        validate_dataset(df)