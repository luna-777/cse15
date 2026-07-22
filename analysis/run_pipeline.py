"""CLI entrypoint: load → clean → features → summarize → write."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `python analysis/run_pipeline.py` from repo root
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis import config
from analysis.clean import clean_prompts, clean_tags
from analysis.features import add_prompt_features
from analysis.load import load_pilot_tags, load_prompts
from analysis.summarize import (
    code_counts,
    codes_by_length,
    codes_by_repo,
    prompt_length_by_repo,
    specificity_summary,
    write_outputs,
)


def build_tables(tags, prompts=None) -> dict:
    tables = {
        "pilot_code_counts": code_counts(tags),
        "pilot_specificity_rate": specificity_summary(tags),
        "pilot_codes_by_length": codes_by_length(tags),
        "pilot_codes_by_repo": codes_by_repo(tags),
    }
    if prompts is not None and not prompts.empty:
        tables["prompt_length_by_repo"] = prompt_length_by_repo(prompts)
        tables["prompt_len_bucket_counts"] = (
            prompts["len_bucket"].value_counts(dropna=False).rename("count").reset_index()
        )
    return tables


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run prompt specificity pandas pipeline")
    parser.add_argument(
        "--prompts",
        type=Path,
        default=config.USER_PROMPTS_CSV,
        help="Path to user_prompts.csv (optional if missing)",
    )
    parser.add_argument(
        "--tags",
        type=Path,
        default=config.PILOT_TAGS_CSV,
        help="Path to pilot_tags.csv",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=config.DERIVED_DIR,
        help="Directory for derived CSV outputs",
    )
    args = parser.parse_args(argv)

    tags = add_prompt_features(clean_tags(load_pilot_tags(args.tags)))

    prompts = None
    if args.prompts.exists():
        prompts = add_prompt_features(clean_prompts(load_prompts(args.prompts)))
    else:
        print(f"note: {args.prompts} not found; running tags-only summaries")

    tables = build_tables(tags, prompts)
    written = write_outputs(tables, args.out)

    print(f"tags_rows: {len(tags)}")
    if prompts is not None:
        print(f"prompts_rows: {len(prompts)}")
    print(f"wrote {len(written)} files under {args.out}:")
    for path in written:
        print(f"  - {path.relative_to(config.ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
