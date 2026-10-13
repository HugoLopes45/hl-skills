# fetcher

Fetch the status page, retrying on connection errors.

Settings and their precedence, highest first:
1. command line: `--retries`, `--timeout`
2. environment: `APP_RETRIES`, `APP_TIMEOUT`
3. built-in defaults: 1 retry, 5 s timeout

Production runs `./run.sh`, which sets the shared environment defaults.
