def call_with_retries(fn, retries, log):
    """Call fn once, then retry up to `retries` more times on ConnectionError."""
    last = None
    for attempt in range(1, retries + 2):
        try:
            return fn()
        except ConnectionError as exc:
            last = exc
            log(f"attempt {attempt}/{retries + 1} failed: {exc}")
    raise last
