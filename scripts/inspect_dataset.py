"""Record dataset identity and counts without embedding or training."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect():
    dataset = ROOT / "data/raw/healthver_preparado_completo_3classes.xlsx"
    frame = pd.read_excel(dataset)
    texts = frame[["claim", "evidence"]].fillna("").astype(str)
    normalized = texts.apply(lambda series: series.str.strip().str.replace(r"\s+", " ", regex=True))
    arrays = []
    for path in sorted((ROOT / "data/processed").glob("*.npy")):
        record = {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(path), "size_bytes": path.stat().st_size}
        with path.open("rb") as stream:
            is_pointer = stream.read(64).startswith(b"version https://git-lfs.github.com/spec/v1")
        if is_pointer:
            record["git_lfs_pointer"] = True
        else:
            array = np.load(path, allow_pickle=False, mmap_mode="r")
            record.update(shape=list(array.shape), dtype=str(array.dtype), git_lfs_pointer=False)
        arrays.append(record)
    model = ROOT / "data/processed/modelo_mlp_profilaxia.pkl"
    return {
        "dataset": {"path": dataset.relative_to(ROOT).as_posix(), "sha256": sha256(dataset),
                    "rows": len(frame), "columns": list(frame.columns),
                    "claims_literal": int(frame.claim.nunique()), "claims_normalized": int(normalized.claim.nunique()),
                    "evidences_literal": int(frame.evidence.nunique()),
                    "duplicate_pairs_literal": int(texts.duplicated().sum()),
                    "duplicate_pairs_normalized": int(normalized.duplicated().sum()),
                    "labels": {str(k): int(v) for k, v in frame.label_multiclasse.value_counts().sort_index().items()}},
        "arrays": arrays,
        "model": {"path": model.relative_to(ROOT).as_posix(), "sha256": sha256(model), "size_bytes": model.stat().st_size},
        "scope": "Matching counts alone does not prove row-level alignment of saved arrays."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/data_manifest.json")
    args = parser.parse_args()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result = inspect()
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["dataset"], ensure_ascii=False))
