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

## Notebook Index

### 01. IC2_regression_IoT_Preprocessing.ipynb
1. Load & inspect data (incl. target distribution: `flow_duration`)
2. Remove unnecessary / leaking columns
3. Detect outliers (numeric features)
4. Remove quasi-constant features
5. Remove constant features
6. Drop duplicate rows
7. Prune highly correlated features
8. Simplify categorical features
9. Feature engineering (totals, ratios, variability measures, flag normalizations)
10. Save cleaned dataset

### 02. IC2_regression_IoT_ML.ipynb
1. Load preprocessed data
2. Leak & correlation checks
3. Explore target distribution (quick stats)
4. Log transform target (`flow_duration`)
5. Train/test split + stratified cross-validation
6. Preprocessing pipeline (numeric/categorical: impute, scale/encode)
7. Baseline model (mean predictor)
8. Model comparison  
   - Linear/Ridge/Lasso/ElasticNet  
   - Random Forest  
   - Gradient Boosting  
   - SVR  
   - KNN
9. Select best model (Gradient Boosting) & train on full train set
10. Evaluate performance & interpret (R², RMSE, MAE; feature importance)
11. Save model artifact
12. Load & test model: per-service p90 flagging of long durations
13. Visualize flagged predictions
14. Limitations, bias & ethical reflection

## Final Results

After testing multiple regression models, the **Gradient Boosting Regressor** delivered the best overall performance on our dataset.  
The final evaluation metrics (on the test set) are:

- **R² ≈ 0.81**  
- **RMSE ≈ 157.5** seconds  
- **MAE ≈ 11.1** seconds  

For comparison, here are the key results of all tested models:

| Model            | R²     | RMSE   | MAE   |
|------------------|--------|--------|-------|
| Ridge            | -2.129 | 632.60 | 33.14 |
| Lasso            | -2.139 | 633.65 | 33.26 |
| ElasticNet       | -2.082 | 627.80 | 32.66 |
| Random Forest    | 0.760  | 175.22 | 11.96 |
| Gradient Boosting| **0.806** | **157.53** | **11.14** |
| SVR              | -0.004 | 358.33 | 26.22 |
| KNN              | 0.510  | 250.28 | 15.23 |

**Takeaway:** Linear models performed poorly due to the non-linear nature of IoT traffic. Tree-based models (Random Forest, Gradient Boosting) captured complex patterns much better, with Gradient Boosting achieving the highest accuracy and lowest error.  

**With this model, we can flag unusually long network flows early and support faster response to potential attacks or malfunctions.**  



