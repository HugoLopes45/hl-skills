class ValidationError(ValueError):
    pass


def require_text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("must not be blank")
    return value
