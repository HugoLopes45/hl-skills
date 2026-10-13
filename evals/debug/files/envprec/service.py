def fetch(timeout):
    """Stand-in for the status endpoint, which is down during the incident."""
    raise ConnectionError(f"status.example.com timed out after {timeout}s")
