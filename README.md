# 🛡️ AI-Powered IoT Cybersecurity Threat Detection System

An intelligent IoT cybersecurity platform that combines **Machine Learning**, **Retrieval-Augmented Generation (RAG)**, **Google Gemini**, and **MQTT-based IoT communication** to detect network attacks and generate human-readable security reports in real time.

---

## 📌 Project Overview

This project monitors telemetry data from an **ESP32 IoT device**, converts it into network-flow features, predicts cyber attacks using a **Random Forest classifier**, retrieves relevant threat information through a **RAG knowledge base**, and generates AI-powered security analysis using **Google Gemini**.

The complete pipeline provides:

- Real-time telemetry monitoring
- Machine Learning based threat detection
- Threat severity classification
- Explainable AI predictions
- AI-generated mitigation reports
- Dashboard visualization
- MQTT communication between ESP32 and backend

---

# 🏗️ System Architecture

```
                 ESP32
                   │
                   │ MQTT
                   ▼
          Mosquitto Broker
                   │
                   ▼
             backend/mqtt.py
                   │
                   ▼
      Feature Mapping (38 Features)
                   │
                   ▼
            FastAPI Backend
                   │
      ┌────────────┴────────────┐
      ▼                         ▼
Random Forest Model         SQLite Database
      │
      ▼
Threat Prediction
      │
      ▼
RAG Knowledge Base
      │
      ▼
Google Gemini API
      │
      ▼
AI Security Report
      │
      ▼
Streamlit Dashboard
```

---

# 🚀 Features

- Real-time IoT telemetry collection
- MQTT communication using Mosquitto
- FastAPI REST API
- Random Forest attack classification
- Confidence score prediction
- Threat level estimation
- Retrieval-Augmented Generation (RAG)
- Google Gemini security analysis
- SQLite data storage
- Streamlit visualization dashboard
- SHAP model explainability
- Modular project architecture

---

# 🧠 Machine Learning

Model:

- Random Forest Classifier

Dataset:

- CICIoT2023 Dataset

Preprocessing:

- Missing value handling
- Label encoding
- Feature scaling
- Outlier clipping (IQR)
- Train-Test Split

Current Performance

| Metric | Score |
|---------|-------|
| Accuracy | 99.96% |
| Precision | 99.96% |
| Recall | 99.96% |
| F1 Score | 99.96% |

---

# 📂 Project Structure

```
AI-Powered-IoT-Cybersecurity-Threat-Detection-System/
│
├── backend/
│   ├── main.py
│   ├── routes.py
│   ├── mqtt.py
│   ├── ml_service.py
│   ├── feature_mapper.py
│   ├── rag.py
│   ├── database.py
│   └── schemas.py
│
├── ml/
│   ├── explore.py
│   ├── preprocess.py
│   ├── train.py
│   ├── explain.py
│   └── dataset_loader.py
│
├── models/
│   ├── random_forest.pkl
│   ├── label_encoder.pkl
│   ├── feature_names.pkl
│   └── scaler.pkl
│
├── datasets/
│   └── raw/
│       └── iot_dataset.csv
│
├── dashboard/
│   └── app.py
│
├── tests/
│
├── results/
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Tech Stack

### Backend

- FastAPI
- Uvicorn

### Machine Learning

- Scikit-Learn
- Pandas
- NumPy
- SHAP
- Joblib

### IoT

- ESP32
- MQTT
- Mosquitto

### AI

- Google Gemini API
- Retrieval-Augmented Generation (RAG)

### Database

- SQLite

### Dashboard

- Streamlit

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/mm-black65/AI-Powered-IoT-Cybersecurity-Threat-Detection-System.git

cd AI-Powered-IoT-Cybersecurity-Threat-Detection-System
```

Create virtual environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 📁 Dataset

Download the **CICIoT2023 Dataset** and place it inside:

```
datasets/raw/
```

Example:

```
datasets/raw/iot_dataset.csv
```

---

# 🏋️ Train the Model

```bash
python ml/train.py
```

Generated files

```
models/random_forest.pkl

models/label_encoder.pkl

models/feature_names.pkl

models/scaler.pkl
```

---

# 📈 Explain Model

```bash
python ml/explain.py
```

Outputs

- SHAP explanation
- Global Feature Importance
- Dependence plots

---

# 🚀 Start Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

Swagger API

```
http://127.0.0.1:8000/docs
```

---

# 📡 Start MQTT Service

```bash
python -m backend.mqtt
```

---

# 📊 Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 🧪 Testing

Run tests

```bash
python tests/test_predict.py

python tests/test_mapper.py

python tests/test_rag.py

python tests/test_mqtt_publish.py
```

---

# 📸 Results

The project automatically generates

- Overall Performance Plot
- Confusion Matrix
- ROC Curves
- Feature Importance
- Classification Report
- SHAP Explainability

Stored inside

```
results/
```

---

# 📚 API Endpoints

### Predict Threat

```
POST /predict-threat
```

Returns

```json
{
    "prediction": "DDoS-TCP_Flood",
    "confidence": 99.98,
    "threat_level": "HIGH",
    "rag_information": "...",
    "ai_analysis": "..."
}
```

---

# 🔐 Threat Levels

| Confidence | Threat |
|------------|---------|
| >90% | HIGH |
| 60-90% | MEDIUM |
| <60% | LOW |

---

# 🔮 Future Improvements

- Deep Learning models
- XGBoost comparison
- Live SHAP dashboard
- Docker deployment
- Kubernetes support
- Cloud MQTT Broker
- User Authentication
- Real-time alert notifications
- Edge deployment on ESP32

---

# 👨‍💻 Contributors

1. Mahi Ahalawat - 2501270021
2. Aishni Rathore - 2501270009
3. Govind Agarwal - 2501270026
4. Yashika Naryani - 2501270027
5. Kshitiz Goyal - 250170042

---
---

# 📄 License

This project is developed for educational and research purposes.

---

# ⭐ If you found this project useful, consider giving it a star.

