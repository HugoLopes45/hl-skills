def unique_users(events):
    """Count distinct non-empty users."""
    total = sum(1 for _ in events)
    if total == 0:
        return 0
    return len({event["user"] for event in events if event["user"].strip()})
