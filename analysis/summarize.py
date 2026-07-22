"""Aggregate tables and write derived outputs."""

from pathlib import Path

import pandas as pd

from analysis.clean import usable_tags


def code_counts(tags: pd.DataFrame) -> pd.DataFrame:
    counts = tags["primary_code"].value_counts(dropna=False).rename("count")
    rates = tags["primary_code"].value_counts(normalize=True, dropna=False).rename("rate")
    return pd.concat([counts, rates], axis=1).reset_index(names="primary_code")


def specificity_summary(tags: pd.DataFrame) -> pd.DataFrame:
    usable = usable_tags(tags)
    if usable.empty:
        return pd.DataFrame(columns=["primary_code", "count", "rate"])
    counts = usable["primary_code"].value_counts().rename("count")
    rates = usable["primary_code"].value_counts(normalize=True).rename("rate")
    return pd.concat([counts, rates], axis=1).reset_index(names="primary_code")


def codes_by_length(tags: pd.DataFrame) -> pd.DataFrame:
    if "len_bucket" not in tags.columns or "primary_code" not in tags.columns:
        return pd.DataFrame()
    usable = usable_tags(tags)
    if usable.empty:
        return pd.DataFrame()
    ct = pd.crosstab(usable["len_bucket"], usable["primary_code"], dropna=False)
    return ct.reset_index()


def codes_by_repo(tags: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    repo_col = "repo" if "repo" in tags.columns else "repo_url"
    if repo_col not in tags.columns:
        return pd.DataFrame()
    usable = usable_tags(tags)
    if usable.empty:
        return pd.DataFrame()
    ct = pd.crosstab(usable[repo_col], usable["primary_code"], dropna=False)
    ct["total"] = ct.sum(axis=1)
    return ct.sort_values("total", ascending=False).head(top_n).reset_index()


def prompt_length_by_repo(prompts: pd.DataFrame) -> pd.DataFrame:
    repo_col = "repo" if "repo" in prompts.columns else "repo_url"
    if repo_col not in prompts.columns or "char_len" not in prompts.columns:
        return pd.DataFrame()
    return (
        prompts.groupby(repo_col, dropna=False)["char_len"]
        .describe()
        .sort_values("count", ascending=False)
        .reset_index()
    )


def write_outputs(tables: dict[str, pd.DataFrame], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name, table in tables.items():
        if table is None or table.empty:
            continue
        path = out_dir / f"{name}.csv"
        table.to_csv(path, index=False)
        written.append(path)
    return written
