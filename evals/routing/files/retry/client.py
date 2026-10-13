import urllib.request

from utils.retry import retry


@retry(attempts=5, base_delay=0.5)
def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read()
