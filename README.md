# 🛡️ AI-Powered IoT Cybersecurity Threat Detection System

An end-to-end intelligent cybersecurity platform that combines **IoT**, **Machine Learning**, **Explainable AI (XAI)**, and **Large Language Models (LLMs)** to detect, explain, and respond to cyber threats targeting IoT devices in real time.

The system continuously monitors telemetry from an **ESP32**, identifies malicious network activity using machine learning, explains every prediction with **SHAP**, and provides human-readable threat analysis and mitigation recommendations through a **Retrieval-Augmented Generation (RAG)** powered AI assistant.

---

# 📌 Overview

This project demonstrates a complete real-time IoT Intrusion Detection System (IDS) pipeline.

1. **ESP32 Telemetry Collection**

   * The ESP32 continuously publishes device and network telemetry (CPU usage, memory utilization, RSSI, connection statistics, MQTT message rate, etc.) via MQTT.

2. **Real-Time Threat Detection**

   * A Python backend subscribes to MQTT topics and performs live inference using a trained **Random Forest** or **XGBoost** model to classify network behavior as normal or malicious.

3. **Explainable AI**

   * Every prediction is interpreted using **SHAP (SHapley Additive exPlanations)**, highlighting the features that most influenced the model's decision.

4. **LLM-Powered Security Assistant**

   * Alert information and SHAP explanations are passed to a **RAG pipeline**, which retrieves relevant cybersecurity knowledge and generates easy-to-understand explanations, attack descriptions, and mitigation strategies.

5. **Interactive Dashboard**

   * A real-time dashboard visualizes telemetry, attack alerts, prediction confidence, SHAP feature importance, and includes a conversational AI assistant for security analysis.

---

# 🏗️ System Architecture

```text
               ESP32 Device
          (Live Telemetry Data)
                    │
                    ▼
              MQTT Broker
                    │
                    ▼
            Python Backend
                    │
                    ▼
      Machine Learning Classifier
      (Random Forest / XGBoost)
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   SHAP Explainability     Threat Prediction
        │                       │
        └───────────┬───────────┘
                    ▼
           RAG Knowledge Retrieval
                    │
                    ▼
           LLM Security Assistant
                    │
                    ▼
          Real-Time Monitoring Dashboard
```

Cyberattacks are launched from a separate attacker machine using tools such as **hping3**, **nmap**, and custom MQTT flooding scripts. The ESP32 requires no attack-specific firmware—it behaves as a standard network-connected IoT device, making the evaluation representative of real-world deployments.

---

# ⚙️ Tech Stack

| Layer                 | Technologies                                                     |
| --------------------- | ---------------------------------------------------------------- |
| **Edge Device**       | ESP32, Arduino Framework, PlatformIO                             |
| **Messaging**         | MQTT (Mosquitto), Paho MQTT                                      |
| **Machine Learning**  | Python, Pandas, NumPy, Scikit-learn, XGBoost                     |
| **Explainable AI**    | SHAP                                                             |
| **RAG Pipeline**      | LangChain / LlamaIndex, ChromaDB or FAISS, Sentence Transformers |
| **LLM**               | OpenAI API / Anthropic API                                       |
| **Backend**           | FastAPI or Flask                                                 |
| **Dashboard**         | Streamlit (or React)                                             |
| **Attack Simulation** | hping3, Nmap, Aireplay-ng (optional), Custom MQTT attack scripts |

---

# 📊 Dataset

The detection models are trained using the **CICIoT2023** dataset, a comprehensive public benchmark for IoT intrusion detection.

### Attack Categories

* DDoS
* DoS
* Reconnaissance
* Spoofing
* Brute Force
* Web-Based Attacks
* Mirai Botnet

The dataset contains **33 attack types** grouped into **7 major categories**, enabling the model to learn diverse real-world attack patterns.

---

# 📁 Project Structure

```text
AI-IoT-Cybersecurity/
│
├── firmware/              # ESP32 firmware
├── attacks/               # Attack simulation scripts
├── dataset/               # CICIoT2023 dataset
│
├── ml/
│   ├── preprocess.py
│   ├── train_rf.py
│   ├── train_xgb.py
│   └── evaluate.py
│
├── backend/
│   ├── mqtt_listener.py
│   ├── predictor.py
│   └── explainer.py
│
├── rag/
│   ├── knowledge_base/
│   ├── embed_store.py
│   └── assistant.py
│
├── dashboard/
│
└── README.md
```

---

# 🚀 Workflow

1. Flash the firmware to the ESP32 and connect it to Wi-Fi.
2. Start the Mosquitto MQTT broker.
3. Train the intrusion detection model.
4. Launch the backend MQTT listener.
5. Start the monitoring dashboard.
6. Simulate network attacks from a separate machine.
7. Observe live attack detection, SHAP explanations, and AI-generated mitigation recommendations in real time.

---

# ✨ Key Features

* Real-time IoT telemetry monitoring
* Machine Learning–based intrusion detection
* Support for multiple cyberattack categories
* Explainable AI using SHAP
* Retrieval-Augmented Generation (RAG) for contextual security guidance
* LLM-powered cybersecurity assistant
* Interactive real-time dashboard
* MQTT-based communication architecture
* Modular and scalable project design
* Easily extensible to additional IoT devices and security datasets
