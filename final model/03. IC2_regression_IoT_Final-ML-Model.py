# Load the saved pipeline
loaded_model = joblib.load(model_path)

# Compute per-service 90th percentile
service_p90 = (
    train_with_service.groupby("service")["flow_duration"]
    .quantile(0.90)
    .to_dict()
)

def mark_redflag(row):
    s = row["service"]
    val = row["Predicted_flow_duration_sec"]
    if s in service_p90 and val > service_p90[s]:
        return "⚠️"
    return ""

results["RedFlag"] = results.apply(mark_redflag, axis=1)

print(results.to_string(index=False))
