"""Fetch rows from a Supabase table using credentials in .env."""

import os
import sys

from dotenv import load_dotenv
from supabase import create_client


def main() -> None:
    load_dotenv()

    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()
    table = os.getenv("SUPABASE_TABLE", "").strip()

    missing = [
        name
        for name, value in [
            ("SUPABASE_URL", url),
            ("SUPABASE_KEY", key),
            ("SUPABASE_TABLE", table),
        ]
        if not value or value.startswith("YOUR_") or value == "your_table_name"
    ]
    if missing:
        print(
            "Fill in these values in .env first:\n  - " + "\n  - ".join(missing),
            file=sys.stderr,
        )
        sys.exit(1)

    supabase = create_client(url, key)
    response = supabase.table(table).select("*").execute()
    print(response.data)


if __name__ == "__main__":
    main()
