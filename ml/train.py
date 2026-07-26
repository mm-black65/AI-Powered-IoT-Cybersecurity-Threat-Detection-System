from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = ROOT / "datasets" / "iot_dataset.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

print("Loading dataset... - train.py:16")

df = pd.read_csv(DATASET_PATH)

print("Dataset Shape: - train.py:20", df.shape)

# Remove missing values
df.dropna(inplace=True)

# Features
X = df.drop(columns=["label"])

# Target
y = df["label"]

# Save feature names
joblib.dump(list(X.columns), MODEL_DIR / "feature_names.pkl")

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# Save encoder
joblib.dump(encoder, MODEL_DIR / "label_encoder.pkl")

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Random Forest... - train.py:50")

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

acc = accuracy_score(y_test, pred)

print(f"\nAccuracy : {acc*100:.2f}%\n - train.py:64")

print(classification_report(y_test, pred))

# Save model
joblib.dump(model, MODEL_DIR / "random_forest.pkl")

print("\nModel Saved Successfully! - train.py:71")

RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Ploting 
# 1. Overall Performance Plot 
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Calculate metrics
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
values = [accuracy * 100, precision * 100, recall * 100, f1 * 100]

# Different colors for each bar
colors = ["royalblue", "forestgreen", "darkorange", "crimson"]

plt.figure(figsize=(8, 6))

bars = plt.bar(metrics, values, color=colors, edgecolor="black", linewidth=1.2)

# Make bars start from 95% since all values are close to 100
plt.ylim(95, 100.5)

plt.ylabel("Performance (%)", fontsize=12)

# Move title upward
plt.title("Overall Performance of Random Forest Classifier",
          fontsize=16,
          fontweight="bold",
          pad=20)

# Add value labels on bars
for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width()/2,
        value + 0.05,
        f"{value:.2f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold"
    )

# Add horizontal grid
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(RESULTS_DIR / "overall_performance.png", dpi=300)

plt.show()

# 2. Confusion Matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

plt.figure(figsize=(8,8))

ConfusionMatrixDisplay.from_estimator(
    model,
    X_test,
    y_test,
    cmap="Blues"
)

plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

# 3. Classification Report
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))
report = classification_report(y_test, y_pred)

with open("results/classification_report.txt","w") as f:
    f.write(report)

# 4. ROC Curves (Automatic)
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

classes = sorted(set(y_test))

y_test_bin = label_binarize(y_test, classes=classes)
y_score = model.predict_proba(X_test)

plt.figure(figsize=(8,6))

for i in range(len(classes)):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"Class {classes[i]} (AUC={roc_auc:.3f})")

plt.plot([0,1],[0,1],'k--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves")
plt.legend()
plt.tight_layout()
plt.show()

