from datetime import datetime, timedelta, timezone


def convert_views(view_text: str) -> int:
    """
    Convert:
        1.2K -> 1200
        4.5M -> 4500000
        987 -> 987
    """

    value = view_text.replace(",", "").strip().upper()

    if value.endswith("K"):
        return int(float(value[:-1]) * 1000)

    if value.endswith("M"):
        return int(float(value[:-1]) * 1_000_000)

    if value.endswith("B"):
        return int(float(value[:-1]) * 1_000_000_000)

    return int(float(value))


def is_within_last_days(posted_date: datetime, days: int):

    now = datetime.now(timezone.utc)

    return posted_date >= now - timedelta(days=days)


def print_divider():

    print("=" * 80)