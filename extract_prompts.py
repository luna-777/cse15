"""Pull analyses.ai_usage_csv from Supabase and export user_prompt rows."""

import csv
import io
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

OUT_PATH = Path(__file__).resolve().parent / "data" / "user_prompts.csv"
PAGE_SIZE = 50


def fetch_analyses_with_csv(supabase):
    rows = []
    start = 0
    while True:
        end = start + PAGE_SIZE - 1
        page = (
            supabase.table("analyses")
            .select("result_id, repo_url, team_name, course_id, analyzed_at, ai_usage_csv")
            .not_.is_("ai_usage_csv", "null")
            .range(start, end)
            .execute()
            .data
        )
        if not page:
            break
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break
        start += PAGE_SIZE
    return rows


def extract_user_prompts(analyses_rows):
    prompts = []
    for row in analyses_rows:
        raw = row.get("ai_usage_csv") or ""
        if not raw.strip():
            continue
        reader = csv.DictReader(io.StringIO(raw))
        for event in reader:
            if (event.get("event_type") or "").strip() != "user_prompt":
                continue
            text = (event.get("message_text") or "").strip()
            if not text:
                continue
            prompts.append(
                {
                    "result_id": row.get("result_id") or "",
                    "repo_url": row.get("repo_url") or "",
                    "team_name": row.get("team_name") or "",
                    "course_id": row.get("course_id") or "",
                    "analyzed_at": row.get("analyzed_at") or "",
                    "timestamp": event.get("timestamp") or "",
                    "event_type": event.get("event_type") or "",
                    "session_id": event.get("session_id") or "",
                    "coding_agent": event.get("coding_agent") or "",
                    "message_text": text,
                }
            )
    return prompts


def main() -> None:
    load_dotenv()
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()
    if not url or not key or url.startswith("YOUR_") or key.startswith("YOUR_"):
        print("Set SUPABASE_URL and SUPABASE_KEY in .env first.", file=sys.stderr)
        sys.exit(1)

    supabase = create_client(url, key)
    analyses = fetch_analyses_with_csv(supabase)
    prompts = extract_user_prompts(analyses)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "result_id",
        "repo_url",
        "team_name",
        "course_id",
        "analyzed_at",
        "timestamp",
        "event_type",
        "session_id",
        "coding_agent",
        "message_text",
    ]
    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prompts)

    print(f"analyses_with_csv: {len(analyses)}")
    print(f"user_prompts: {len(prompts)}")
    print(f"wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
