from datetime import datetime, timezone


def now() -> datetime:
    return datetime.now(tz=timezone.utc)


def from_iso8601(val: str) -> datetime:
    return datetime.fromisoformat(val)
