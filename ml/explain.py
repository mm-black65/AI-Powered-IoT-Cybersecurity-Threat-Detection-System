from pathlib import Path
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT / "models"
DATASET_PATH = ROOT / "datasets" /"iot_dataset.csv"

# Load model and supporting files
model = joblib.load(MODEL_DIR / "random_forest.pkl")
encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")

# Load dataset
df = pd.read_csv(DATASET_PATH)
X = df.drop(columns=["label"])
y = df["label"]

# Ensure feature order
X = X[feature_names]


def explain_prediction(sample_idx=0, plot=True):
    """
    Explain a single prediction using SHAP values.
    
    Args:
        sample_idx: Index of sample to explain (default: 0)
        plot: Whether to display SHAP force plot (default: True)
    
    Returns:
        SHAP explanation values
    """
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    
    # Get sample
    sample = X.iloc[sample_idx:sample_idx+1]
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(sample)
    
    print(f"\n{'='*60}")
    print(f"EXPLAINING PREDICTION FOR SAMPLE {sample_idx}")
    print(f"{'='*60}")
    
    print(f"\nActual Label: {y.iloc[sample_idx]}")
    print(f"Prediction: {encoder.inverse_transform([model.predict(sample)[0]])[0]}")
    print(f"Confidence: {model.predict_proba(sample).max() * 100:.2f}%\n")
    
    if plot:
        # Force plot (shows contribution of each feature)
        shap.force_plot(
            explainer.expected_value[0],
            shap_values[0][0],
            sample.iloc[0],
            feature_names=feature_names,
            matplotlib=True,
            show=True
        )
    
    return shap_values


def feature_importance_global(num_samples=100):
    """
    Calculate global feature importance using mean absolute SHAP values.
    
    Args:
        num_samples: Number of samples to use for calculation (default: 100)
    
    Returns:
        DataFrame with feature importance rankings
    """
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    
    # Sample data
    sample_data = X.sample(n=min(num_samples, len(X)), random_state=42)
    
    print(f"\nCalculating SHAP values for {len(sample_data)} samples...")
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(sample_data)
    print(type(shap_values))
    print(np.array(shap_values).shape)
    # Mean absolute SHAP values for global importance
    # For multi-class, average across classes
    shap_values = explainer.shap_values(sample_data)

    # Handle different SHAP output formats
    if isinstance(shap_values, list):
    # Older SHAP versions (multiclass)
        shap_values_array = np.mean(np.abs(np.array(shap_values)), axis=0)
    elif len(shap_values.shape) == 3:
    # Newer SHAP versions: (samples, features, classes)
        shap_values_array = np.mean(np.abs(shap_values), axis=2)
    else:
    # Binary classification/regression
        shap_values_array = np.abs(shap_values)

    importance = shap_values_array.mean(axis=0)

   # Ensure it's 1D
    importance = np.ravel(importance)
    
    # Create DataFrame
    print("Importance shape:", np.array(importance).shape)
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importance
    }).sort_values('Importance', ascending=False)
    
    print(f"\n{'='*60}")
    print("GLOBAL FEATURE IMPORTANCE (Top 15)")
    print(f"{'='*60}\n")
    print(importance_df.head(15).to_string(index=False))
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'].head(15), importance_df['Importance'].head(15))
    plt.xlabel('Mean |SHAP value|')
    plt.title('Top 15 Most Important Features')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
    
    return importance_df


def dependence_plot(feature_name, num_samples=100):
    """
    Create SHAP dependence plot for a specific feature.
    
    Args:
        feature_name: Name of feature to analyze
        num_samples: Number of samples to use (default: 100)
    """
    if feature_name not in feature_names:
        print(f"Feature '{feature_name}' not found!")
        return
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)
    
    # Sample data
    sample_data = X.sample(n=min(num_samples, len(X)), random_state=42)
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(sample_data)
    
    # Average across classes if multi-class
    if isinstance(shap_values, list):
        shap_values_array = np.array(shap_values).mean(axis=0)
    else:
        shap_values_array = shap_values
    
    feature_idx = feature_names.index(feature_name)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(sample_data.iloc[:, feature_idx], shap_values_array[:, feature_idx])
    plt.xlabel(feature_name)
    plt.ylabel('SHAP value')
    plt.title(f'SHAP Dependence Plot: {feature_name}')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage
    print("🔍 MODEL EXPLAINABILITY ANALYSIS\n")
    
    # 1. Explain a single prediction
    print("1️⃣  EXPLAINING SINGLE PREDICTION")
    explain_prediction(sample_idx=0, plot=False)
    
    # 2. Global feature importance
    print("\n\n2️⃣  GLOBAL FEATURE IMPORTANCE")
    importance_df = feature_importance_global(num_samples=50)
    
    # 3. Dependence plot for top feature
    print("\n\n3️⃣  DEPENDENCE PLOT FOR TOP FEATURE")
    top_feature = importance_df.iloc[0]['Feature']
    print(f"\nGenerating dependence plot for: {top_feature}")
    # dependence_plot(top_feature, num_samples=50)  # Uncomment to view plot
    
    print("\n✅ Explainability analysis complete!")
