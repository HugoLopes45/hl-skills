import os

DEFAULTS = {"retries": 1, "timeout": 5}


def resolve(cli):
    """Return the settings; precedence is documented in README.md."""
    settings = dict(DEFAULTS)
    for key in settings:
        cli_value = getattr(cli, key)
        if cli_value is not None:
            settings[key] = cli_value
        env_value = os.environ.get("APP_" + key.upper())
        if env_value is not None:
            settings[key] = int(env_value)
    return settings
