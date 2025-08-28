import joblib
from pathlib import Path
import numpy as np
import pandas as pd

# Absoluut pad naar je model
model_path = Path("/Users/esthervanhelmont/Documents/#Python/IC2 Regression/final model/best_pipeline_gbr.joblib")

# Model laden
loaded_model = joblib.load(model_path)
print("✅ Model loaded:", model_path)



# Build per-service p90 thresholds from TRAIN data
train_with_service = X_train.copy()
train_with_service["flow_duration"] = np.expm1(y_train_log)
service_p90 = (
    train_with_service.groupby("service")["flow_duration"]
    .quantile(0.85)
    .to_dict()
)

# Make predictions for the first N test rows
N = 10
pred_log = loaded_model.predict(X_test[:N])
pred_sec = np.expm1(pred_log)

# Create a DataFrame for flagging (don't call it 'results' to avoid name clash)
flags_df = pd.DataFrame({
    "service": X_test.loc[X_test.index[:N], "service"].values if "service" in X_test.columns else ["-"] * N,
    "Predicted_flow_duration_sec": pred_sec.round(2)
})

# Flag rows whose prediction is above the p90 for their own service
def mark_redflag(row):
    s = row["service"]
    val = row["Predicted_flow_duration_sec"]
    thr = service_p90.get(s, np.inf)
    return "⚠️" if val > thr else ""

flags_df["RedFlag"] = flags_df.apply(mark_redflag, axis=1)

print(flags_df.to_string(index=False))
