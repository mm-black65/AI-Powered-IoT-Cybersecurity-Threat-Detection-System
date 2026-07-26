import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_raw_data(csv_paths: list[str]) -> pd.DataFrame:
    """Load and concatenate one or more CICIoT2023 CSV files."""
    frames = []
    for path in csv_paths:
        df = pd.read_csv(path)
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    print(f"Loaded {len(combined)} rows from {len(csv_paths)} file(s).")
    return combined


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns that are entirely empty, fill remaining NaNs with column median."""
    df = df.dropna(axis=1, how="all")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    remaining_na = df.isna().sum().sum()
    if remaining_na > 0:
        df = df.fillna(0)

    return df


def remove_outliers_iqr(df: pd.DataFrame, columns: list[str], factor: float = 3.0) -> pd.DataFrame:
    """
    Basic IQR-based outlier clipping (not dropping rows, just capping extreme
    values) — dropping rows in an intrusion dataset can accidentally delete
    real attack samples, since attacks ARE the outliers by nature.
    """
    for col in columns:
        if col not in df.columns:
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        df[col] = df[col].clip(lower=lower, upper=upper)
    return df


def encode_labels(df: pd.DataFrame, label_col: str = "label") -> tuple[pd.DataFrame, dict]:
    """Convert string attack labels into integer classes; return the mapping."""
    unique_labels = sorted(df[label_col].unique())
    label_map = {label: idx for idx, label in enumerate(unique_labels)}
    df[label_col] = df[label_col].map(label_map)
    return df, label_map


def preprocess_pipeline(
    csv_paths: list[str],
    label_col: str = "label",
    test_size: float = 0.2,
    random_state: int = 42,
    scaler_output_path: str = "scaler.pkl",
):
    """
    Full pipeline: load -> clean -> scale -> split.
    Returns X_train, X_test, y_train, y_test, label_map, feature_columns
    """
    df = load_raw_data(csv_paths)
    df = handle_missing_values(df)

    if label_col not in df.columns:
        raise ValueError(f"Label column '{label_col}' not found. Available columns: {list(df.columns)}")

    feature_columns = [c for c in df.columns if c != label_col]

    df = remove_outliers_iqr(df, feature_columns)
    df, label_map = encode_labels(df, label_col)

    X = df[feature_columns]
    y = df[label_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    joblib.dump(scaler, scaler_output_path)
    print(f"Scaler saved to {scaler_output_path}")

    return X_train_scaled, X_test_scaled, y_train, y_test, label_map, feature_columns


if __name__ == "__main__":
    # Example usage — update paths to your actual CICIoT2023 CSV files
    csv_files = ["datasets/iot_dataset.csv"]

    X_train, X_test, y_train, y_test, label_map, feature_columns = preprocess_pipeline(
        csv_paths=csv_files,
        label_col="label",
    )

    print("Label mapping:", label_map)
    print("Feature columns:", feature_columns)
    print("Train shape:", X_train.shape, "Test shape:", X_test.shape)