from pathlib import Path
import pandas as pd
import requests
from pprint import pprint

ROOT = Path(__file__).resolve().parent.parent

# Load one sample from dataset
df = pd.read_csv(ROOT / "datasets" / "raw" / "iot_dataset.csv")

sample = df.iloc[0].drop("label").to_dict()

# Send to FastAPI
response = requests.post(
    "http://127.0.0.1:8000/predict-threat",
    json=sample
)

print("\n============================== ")
print("Status Code:", response.status_code)
print("==============================\n ")

if response.status_code == 200:

    result = response.json()

    print("Prediction      : ", result["prediction"])
    print("Confidence      : ", result["confidence"], "%")
    print("Threat Level    : ", result["threat_level"])

    print("\n============================== ")
    print("AI Security Analysis ")
    print("==============================\n ")

    print(result["ai_analysis"])

else:

    print("Request Failed! ")
    print(response.text)