"""Paths and constants for the analysis pipeline."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DERIVED_DIR = DATA_DIR / "derived"

USER_PROMPTS_CSV = DATA_DIR / "user_prompts.csv"
PILOT_TAGS_CSV = DATA_DIR / "pilot_tags.csv"

USABLE_CODES = ("SPECIFIC", "VAGUE")
EXCLUDE_CODE = "EXCLUDE"

LENGTH_BINS = [0, 60, 250, 1000, 10_000_000]
LENGTH_LABELS = ["short", "medium", "long", "xl"]
