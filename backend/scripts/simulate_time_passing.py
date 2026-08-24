import sys
from datetime import datetime, timedelta

from app.db.client import supabase


def simulate_time_passing(hours: int) -> None:
    attempts = (
        supabase.table("recovery_attempts")
        .select("id, next_retry_at")
        .not_.is_("next_retry_at", "null")
        .execute()
        .data
    )

    for attempt in attempts:
        retry_time = datetime.fromisoformat(
            attempt["next_retry_at"].replace("Z", "+00:00")
        )
        new_retry_time = retry_time - timedelta(hours=hours)

        supabase.table("recovery_attempts").update(
            {"next_retry_at": new_retry_time.isoformat()}
        ).eq("id", attempt["id"]).execute()

    print(f"Updated {len(attempts)} retry schedules by {hours} hours.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m scripts.simulate_time_passing <hours>")
        sys.exit(1)

    simulate_time_passing(int(sys.argv[1]))