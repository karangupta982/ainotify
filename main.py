"""CLI entrypoint that kicks off the daily aggregation pipeline."""

from app.daily_runner import run_daily_pipeline


def main(hours: int = 24, top_n: int = 10):
    """
    Run the end-to-end aggregation flow.

    Args:
        hours: Lookback window for new content.
        top_n: How many ranked digests to include in the email.
    """
    return run_daily_pipeline(hours=hours, top_n=top_n)


if __name__ == "__main__":
    import sys

    hours = 24
    top_n = 10

    # Allow overriding defaults via CLI args to support scheduled/adhoc runs.
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    if len(sys.argv) > 2:
        top_n = int(sys.argv[2])

    result = main(hours=hours, top_n=top_n)
    # Exit code signals success/failure to schedulers (cron/Render jobs).
    exit(0 if result["success"] else 1)
