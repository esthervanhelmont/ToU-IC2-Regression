# ToU-IC2-Regression

# **Machine Learning Regression for proactive attack pattern detection in IoT networks**

By **predicting** `flow_duration` **from basic network telemetry** in real-time IoT traffic, we can spot unusual resource use early and surface potential attack patterns before they escalate. This enables proactive capacity planning *(autoscaling, QoS tuning)* and faster security response, reducing downtime and operating costs while keeping connected devices reliable.

In line with **SDG 9 *(Industry, Innovation & Infrastructure)*** and **SDG 16 *(Peace, Justice & Strong Institutions)***, this approach strengthens digital infrastructure and improves cyber-resilience for services that increasingly depend on IoT.

**Impact:** Securing IoT networks helps keep critical infrastructure - such as smart cities, healthcare, and energy systems - safe and reliable. **Concretely,** this means hospital sensor networks remain stable and smart city street lighting is protected from attack-driven disruptions.

[Dataset index](https://www.notion.so/Dataset-index-25898c6768cd80579f7dcc23e99f9c7a?pvs=21)

[Stakeholder report](https://www.notion.so/Stakeholder-report-Machine-Learning-Regression-for-proactive-attack-pattern-detection-in-IoT-netwo-25d98c6768cd80ac9c52ef4ed8405883#25d98c6768cd804bb121caefc7765c0b)


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
