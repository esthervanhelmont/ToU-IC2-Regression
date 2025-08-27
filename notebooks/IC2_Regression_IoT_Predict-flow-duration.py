#!/usr/bin/env python3
# Predict flow_duration with a saved sklearn Pipeline (preprocess + model).
# FIX A: enforce scikit-learn==1.6.1 (the version used to save the model).

# ---------- Auto-install / enforce exact versions ----------
import os, sys, subprocess, importlib

def ensure_exact_package(pkg_name: str, required_version: str):
    """
    Ensure pkg_name==required_version is installed.
    If not, pip install and re-exec the current process.
    """
    try:
        mod = importlib.import_module(pkg_name)
        current = getattr(mod, "__version__", "")
        if current != required_version:
            print(f"⚠️  {pkg_name} {current} found, but {required_version} required. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg_name}=={required_version}"])
            # Re-exec current process with same args, so the freshly installed version is loaded.
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except ImportError:
        print(f"⚠️  {pkg_name} not found. Installing {pkg_name}=={required_version} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"{pkg_name}=={required_version}"])
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Enforce the versions used when saving the pipeline
ensure_exact_package("scikit_learn", "1.6.1")  # module name is scikit_learn
ensure_exact_package("joblib", "1.4.2")

# Optional: make sure core deps exist (no strict version pin)
for _pkg in ["numpy", "pandas"]:
    try:
        importlib.import_module(_pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", _pkg])

# ---------- Now import the rest (safe to import sklearn/joblib) ----------
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from joblib import load

# ---------- Small helpers ----------
def eprint(*a): print(*a, file=sys.stderr)

def find_model(default_candidates):
    for p in default_candidates:
        if p.exists():
            return p
    return None

def download(url: str, dest: Path):
    import urllib.request
    dest.parent.mkdir(parents=True, exist_ok=True)
    eprint(f"Downloading model from {url} → {dest}")
    urllib.request.urlretrieve(url, dest)
    return dest

def parse_args():
    p = argparse.ArgumentParser(description="Score flow_duration using a saved sklearn Pipeline.")
    p.add_argument("--model-path", type=str, default=None, help="Local path to best_pipeline_gbr.joblib")
    p.add_argument("--model-url", type=str, default=None, help="URL to download the model if not present")
    p.add_argument("--input-csv", type=str, default=None, help="CSV to score (must match training columns)")
    p.add_argument("--output-csv", type=str, default="predictions.csv", help="Where to write predictions CSV")
    p.add_argument("--print-json", action="store_true", help="Also print predictions as JSON to stdout")
    return p.parse_args()

# ---------- Main ----------
def main():
    args = parse_args()

    # repo-relative discovery (works locally and in CI)
    BASE = Path(__file__).resolve().parent
    candidates = [
        BASE / "artifacts" / "best_pipeline_gbr.joblib",           # notebooks/artifacts
        BASE.parent / "artifacts" / "best_pipeline_gbr.joblib",    # project-root/artifacts
        Path.cwd() / "artifacts" / "best_pipeline_gbr.joblib",     # CWD/artifacts
    ]

    # resolve model path
    if args.model_path:
        model_path = Path(args.model_path).expanduser().resolve()
        if not model_path.exists():
            eprint(f"❌ --model-path not found: {model_path}")
            sys.exit(1)
    else:
        model_path = find_model([p.resolve() for p in candidates])

    if model_path is None and args.model_url:
        target = (BASE / "artifacts" / "best_pipeline_gbr.joblib").resolve()
        model_path = download(args.model_url, target)

    if model_path is None or not model_path.exists():
        eprint("❌ Could not find model 'best_pipeline_gbr.joblib'. Tried:")
        for p in candidates:
            eprint(f" - {p}")
        eprint("\nFix by either passing --model-path /path/to/best_pipeline_gbr.joblib "
               "or providing --model-url https://.../best_pipeline_gbr.joblib")
        sys.exit(1)

    eprint(f"✅ Using model: {model_path}")

    # load pipeline (preprocess + model)
    pipeline = load(model_path)

    # load data
    if args.input_csv:
        df = pd.read_csv(args.input_csv)
        eprint(f"Scoring {len(df)} rows from {args.input_csv}")
    else:
        # minimal example row (adjust to your schema if needed)
        df = pd.DataFrame([{
            "proto": "tcp",
            "service": "http",
            "fwd_pkts_tot": 120,
            "down_up_ratio": 1.5,
            "fwd_header_size_tot": 320,
            "bwd_header_size_min": 40,
            "flow_syn_flag_count": 1,
            "flow_rst_flag_count": 0,
            "flow_ack_flag_count": 10,
            "fwd_pkts_payload_tot": 200,
            "fwd_pkts_payload_avg": 100,
            "bwd_pkts_payload_max": 150,
            "bwd_pkts_payload_avg": 70,
            "flow_pkts_payload_avg": 85,
            "fwd_iat_min": 5,
            "bwd_iat_min": 7,
            "fwd_subflow_pkts": 15,
            "bwd_subflow_pkts": 10,
            "fwd_subflow_bytes": 2048
        }])
        eprint("No --input-csv provided → scoring example row.")

    # predict: pipeline outputs log-space → invert to original units
    log_pred = pipeline.predict(df)
    pred = np.expm1(log_pred)

    # write CSV
    out = df.copy()
    out["pred_flow_duration"] = pred
    out_path = Path(args.output_csv).resolve()
    out.to_csv(out_path, index=False)
    eprint(f"💾 Saved predictions → {out_path}")

    if args.print_json:
        print(json.dumps(out.to_dict(orient="records"), indent=2))

if __name__ == "__main__":
    main()
