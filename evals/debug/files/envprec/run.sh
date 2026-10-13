#!/bin/sh
# Production launcher: shared defaults for every environment.
export APP_RETRIES=3
export APP_TIMEOUT=2
exec python3 app.py "$@"
