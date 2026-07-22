"""Normalize and filter prompt / tag tables."""

import re

import pandas as pd

from analysis.config import EXCLUDE_CODE, USABLE_CODES


_WRAPPER_RE = re.compile(r"</?user_query>|<timestamp>.*?</timestamp>", re.I | re.S)


def _normalize_text(value: object) -> str:
    text = "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
    text = _WRAPPER_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_prompts(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    text_col = "message_text" if "message_text" in out.columns else None
    if text_col is None:
        raise ValueError("prompts table needs a message_text column")

    out[text_col] = out[text_col].map(_normalize_text)
    out = out[out[text_col].str.len() > 0].copy()

    if "event_type" in out.columns:
        out = out[out["event_type"].fillna("") == "user_prompt"].copy()

    # Stable dedupe key when available
    subset = [c for c in ("result_id", "timestamp", text_col) if c in out.columns]
    if subset:
        out = out.drop_duplicates(subset=subset, keep="first")

    return out.reset_index(drop=True)


def clean_tags(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    text_col = "message_text" if "message_text" in out.columns else "message_preview"
    if text_col in out.columns:
        out[text_col] = out[text_col].map(_normalize_text)

    if "primary_code" not in out.columns:
        raise ValueError("tags table needs a primary_code column")

    out["primary_code"] = out["primary_code"].astype(str).str.strip().str.upper()
    return out.reset_index(drop=True)


def usable_tags(df: pd.DataFrame) -> pd.DataFrame:
    """SPECIFIC / VAGUE only (drop EXCLUDE and unknowns)."""
    return df[df["primary_code"].isin(USABLE_CODES)].copy().reset_index(drop=True)


def excluded_tags(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["primary_code"] == EXCLUDE_CODE].copy().reset_index(drop=True)
