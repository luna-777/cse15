"""Derived columns for prompt tables."""

import pandas as pd

from analysis.config import LENGTH_BINS, LENGTH_LABELS


def add_prompt_features(df: pd.DataFrame, text_col: str = "message_text") -> pd.DataFrame:
    out = df.copy()
    if text_col not in out.columns:
        if "message_preview" in out.columns:
            text_col = "message_preview"
        else:
            raise ValueError("Need message_text or message_preview for features")

    text = out[text_col].fillna("").astype(str)
    out["char_len"] = text.str.len()
    out["word_len"] = text.str.split().str.len()
    out["len_bucket"] = pd.cut(
        out["char_len"],
        bins=LENGTH_BINS,
        labels=LENGTH_LABELS,
        include_lowest=True,
        right=True,
    )
    if "repo_url" in out.columns:
        out["repo"] = (
            out["repo_url"]
            .fillna("")
            .astype(str)
            .str.replace(r"^https://github.com/", "", regex=True)
        )
    return out
