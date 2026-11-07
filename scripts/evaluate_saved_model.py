"""Reproduce validation metrics of the trusted saved delivery model."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import joblib
import numpy as np
import sklearn
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, recall_score

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def evaluate():
    directory = ROOT / "data/processed"
    files = [directory / name for name in ["modelo_mlp_profilaxia.pkl", "X_val_emb.npy", "y_val.npy"]]
    model = joblib.load(files[0])
    features = np.load(files[1], allow_pickle=False)
    labels = np.load(files[2], allow_pickle=False)
    prediction = model.predict(features)
    return {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "evaluation": "saved fixed validation split", "samples": len(labels),
        "model_type": type(model).__name__, "classes": ["SUPPORTED", "REFUTED", "NEUTRAL"],
        "accuracy": float(accuracy_score(labels, prediction)),
        "f1_macro": float(f1_score(labels, prediction, average="macro")),
        "recall_macro": float(recall_score(labels, prediction, average="macro")),
        "classification_report": classification_report(labels, prediction, labels=[0, 1, 2],
            target_names=["SUPPORTED", "REFUTED", "NEUTRAL"], output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(labels, prediction, labels=[0, 1, 2]).tolist(),
        "artifacts": [{"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)} for path in files],
        "environment": {"python": platform.python_version(), "sklearn": sklearn.__version__,
                        "numpy": np.__version__, "joblib": joblib.__version__},
        "scope": "No retraining, no test-set evaluation and no live retrieval or translation."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/validation_metrics.json")
    args = parser.parse_args()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result = evaluate()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ["samples", "accuracy", "f1_macro", "recall_macro"]}))
