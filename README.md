# ToU-IC2-Regression

# **Machine Learning Regression for proactive attack pattern detection in IoT networks**

By **predicting** `flow_duration` **from basic network telemetry** in real-time IoT traffic, we can spot unusual resource use early and surface potential attack patterns before they escalate. This enables proactive capacity planning *(autoscaling, QoS tuning)* and faster security response, reducing downtime and operating costs while keeping connected devices reliable.

In line with **SDG 9 *(Industry, Innovation & Infrastructure)*** and **SDG 16 *(Peace, Justice & Strong Institutions)***, this approach strengthens digital infrastructure and improves cyber-resilience for services that increasingly depend on IoT.

**Impact:** Securing IoT networks helps keep critical infrastructure - such as smart cities, healthcare, and energy systems - safe and reliable. **Concretely,** this means hospital sensor networks remain stable and smart city street lighting is protected from attack-driven disruptions.

[Dataset index](https://www.notion.so/Dataset-index-25898c6768cd80579f7dcc23e99f9c7a?pvs=21)

[Stakeholder summary](https://www.notion.so/Stakeholder-summary-25898c6768cd8087997ac77af2b84b6b?pvs=21)

# IoT Flow Duration Prediction using Regression

## Summary
This project predicts **flow duration** in IoT (Internet of Things) network traffic using regression machine learning models.  
The goal is to **identify unusual traffic patterns early**, which may indicate anomalies or potential cyberattacks.  
By enabling proactive detection, this approach strengthens digital infrastructure resilience and supports capacity planning and security monitoring.  
This aligns with **SDG 9 (Industry, Innovation & Infrastructure)** and **SDG 16 (Peace, Justice & Strong Institutions)**.

## Hypothesis
We assume that **basic network telemetry features** (e.g., source/destination ports, packet counts, byte counts, protocol) contain enough information to predict `flow_duration`.  
If the model can accurately predict `flow_duration`, deviations from expected values may highlight unusual or suspicious activity.  

## Dataset Info
- **Source:** [RT-IoT2022 Dataset (UCI Machine Learning Repository)](https://archive.ics.uci.edu/dataset/942/rt-iot2022)  
- **Content:** Realistic IoT traffic data including benign and malicious traffic flows.  
- **Target variable:** `flow_duration` (continuous numeric value).  
- **Features:** Network-level metadata such as IP addresses, ports, bytes, packets, protocols, and flags.  
- **Preprocessing:**  
  - Removed quasi-constant and highly correlated features.  
  - Checked distribution of target → log-transformation applied to reduce skewness.  
  - Split dataset into train/test sets and built preprocessing pipelines.  

## Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/iot-flow-duration-prediction.git
cd iot-flow-duration-prediction
pip install -r requirements.txt
Main dependencies:

Python 3.10+

pandas, numpy, matplotlib

scikit-learn

joblib

Usage
Preprocessing: Run the notebook

bash
Code kopiëren
jupyter notebook "01. IC2_regression_IoT_Preprocessing.ipynb"
→ Cleans data, explores features, applies transformations.

Modeling: Run the notebook

bash
Code kopiëren
jupyter notebook "02. IC2_regression_IoT_ML.ipynb"
→ Trains multiple regression models, compares results, and saves the best pipeline.

Prediction (example):

python
Code kopiëren
import joblib
import pandas as pd

# Load model
model = joblib.load("notebooks/artifacts/best_pipeline_gbr.joblib")

# Example prediction
sample = pd.DataFrame({...})  # insert one or more rows with feature values
prediction = model.predict(sample)
print(prediction)
Folder Structure
Code kopiëren
.
├── notebooks/
│   ├── 01. IC2_regression_IoT_Preprocessing.ipynb
│   ├── 02. IC2_regression_IoT_ML.ipynb
│   └── artifacts/
│       └── best_pipeline_gbr.joblib
├── requirements.txt
└── README.md
notebooks/01...: Data exploration & preprocessing

notebooks/02...: Modeling & evaluation

artifacts/: Saved ML pipeline(s)

requirements.txt: Dependencies

Ethical Notes
Bias & Generalization: Dataset may not represent all IoT environments → results might not generalize to unseen devices/networks.

Fairness: Since target is numeric, fairness risks are limited. However, imbalance in service types could bias performance.

Transparency: Preprocessing and random seeds were fixed to ensure reproducibility.

Impact: Early anomaly detection in IoT networks helps prevent outages and cyberattacks, strengthening reliability of critical infrastructure (healthcare, smart cities, energy).
