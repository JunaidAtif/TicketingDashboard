def strip_and_validate_not_blank(value: str) -> str:
    if value is None:
        return value
    stripped = value.strip()
    if not stripped:
        raise ValueError("Field cannot be empty or just whitespace.")
    return stripped

def reject_empty_strings(value: str) -> str:
    if value is not None and value.strip() == "":
        raise ValueError("Field cannot be empty or just whitespace.")
    return value
