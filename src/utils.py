import re


def to_float(value):
    try:
        return float(value)
    except:
        return None


def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None


def in_range(value, min_val, max_val):
    return min_val <= value <= max_val


def clean_string(text):
    return " ".join(text.strip().split())


def is_empty(text):
    return text.strip() == ""
