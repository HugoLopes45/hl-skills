MAX_RETRIES = 5


def fetch(call):
    for attempt in range(MAX_RETRIES):
        try:
            return call()
        except ConnectionError:
            if attempt == MAX_RETRIES - 1:
                raise
