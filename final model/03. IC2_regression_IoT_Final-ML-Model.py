# Simple predictor: load saved pipeline, score a CSV, save predictions
# Paths are RELATIVE to this script (placed in: final model/)

from pathlib import Path
import joblib
import pandas as pd
import numpy as np

# --- Config ---
# If your model was trained on log(target), keep this True to invert with expm1
LOG_TARGET = True

# Relative paths
MODEL_PATH = Path("best_pipeline_gbr.joblib")  # file lives next to this script
DATA_PATH  = Path("../data/processed/rt_iot2022_Test-sample_Final-model.csv")  # adjust if your filename differs
OUT_PATH   = Path("predictions.csv")

# --- Load model ---
model = joblib.load(MODEL_PATH)
print(f"✅ Loaded model: {MODEL_PATH.resolve()}")

# --- Load data (features only; no target column) ---
X = pd.read_csv(DATA_PATH)
print(f"✅ Loaded data: {DATA_PATH.resolve()}  shape={X.shape}")

# --- Predict ---
y_pred = model.predict(X)
if LOG_TARGET:
    y_pred = np.expm1(y_pred)  # invert log1p/ln transformation

# --- Build output table (show service if present) ---
out = pd.DataFrame({
    "service": X["service"] if "service" in X.columns else ["-"] * len(X),
    "predicted_flow_duration_sec": np.round(y_pred, 2)
})

# --- Save & preview ---
out.to_csv(OUT_PATH, index=False)
print(f"💾 Saved predictions → {OUT_PATH.resolve()}")
print("\nPreview:")
print(out.head(10).to_string(index=False))
