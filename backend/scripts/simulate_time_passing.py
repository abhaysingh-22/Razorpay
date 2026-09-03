"""
Time-Travel / Clock Simulation Utility for Recovery Schedules.
Adjusts `next_retry_at` timestamps in `recovery_attempts` table backwards by N hours
to simulate the passage of real-world time for scheduled retries (e.g. salary dates).

Usage:
    python -m scripts.simulate_time_passing --hours 24
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from app.db.client import supabase


def simulate_time_passing(hours: int, dry_run: bool = False) -> int:
    """
    Shifts all future retry schedules backwards by `hours` to trigger retry queues.

    Args:
        hours: Number of hours to fast-forward time by.
        dry_run: If True, calculates changes without modifying the database.

    Returns:
        Number of updated attempt records.
    """
    try:
        attempts = (
            supabase.table("recovery_attempts")
            .select("id, transaction_id, attempt_number, next_retry_at")
            .not_.is_("next_retry_at", "null")
            .execute()
            .data
            or []
        )
    except Exception as e:
        print(f"❌ Error fetching recovery attempts: {e}", file=sys.stderr)
        return 0

    if not attempts:
        print("ℹ️  No scheduled recovery attempts found with active next_retry_at.")
        return 0

    updated_count = 0
    now = datetime.now(timezone.utc)

    for attempt in attempts:
        raw_retry = attempt.get("next_retry_at")
        if not raw_retry:
            continue

        try:
            # Handle ISO string formats (Z or +00:00)
            cleaned_str = raw_retry.replace("Z", "+00:00")
            retry_time = datetime.fromisoformat(cleaned_str)
            if retry_time.tzinfo is None:
                retry_time = retry_time.replace(tzinfo=timezone.utc)

            new_retry_time = retry_time - timedelta(hours=hours)

            if not dry_run:
                supabase.table("recovery_attempts").update(
                    {"next_retry_at": new_retry_time.isoformat()}
                ).eq("id", attempt["id"]).execute()

            status_indicator = (
                "⚡ Due Now" if new_retry_time <= now else "⏳ Still Future"
            )
            print(
                f"  • Attempt {attempt['id'][:8]} (Tx: {attempt.get('transaction_id', '')[:8]}): {raw_retry[:19]} ➔ {new_retry_time.isoformat()[:19]} [{status_indicator}]"
            )
            updated_count += 1
        except Exception as err:
            print(f"  ⚠️ Failed to adjust attempt {attempt.get('id')}: {err}")

    prefix = "[DRY-RUN] Would update" if dry_run else "✅ Successfully updated"
    print(f"\n{prefix} {updated_count} recovery schedules by {hours} hours.")
    return updated_count


def main():
    parser = argparse.ArgumentParser(
        description="Fast-forward recovery retry schedules by N hours."
    )
    parser.add_argument(
        "--hours",
        "-H",
        type=int,
        default=24,
        help="Hours to shift retry times into the past (default: 24)",
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Preview timestamp changes without writing to database",
    )
    args = parser.parse_args()

    simulate_time_passing(hours=args.hours, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
