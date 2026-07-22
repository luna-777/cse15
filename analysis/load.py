"""Load flat CSV inputs for the pipeline."""

from pathlib import Path

import pandas as pd


def load_prompts(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run `python extract_prompts.py` first, or pass only pilot tags."
        )
    df = pd.read_csv(path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    if "analyzed_at" in df.columns:
        df["analyzed_at"] = pd.to_datetime(df["analyzed_at"], errors="coerce", utc=True)
    return df


def load_pilot_tags(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    return df
