import re


# SAFE FLOAT CONVERSION
def to_float(value):
    """Safely convert input to float; return None on failure."""
    try:
        return float(value)
    except:
        return None


# EMAIL VALIDATION
def is_valid_email(email):
    """
    Validates email format using regex.
    Returns True/False.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# RANGE VALIDATION (Generic)
def in_range(value, min_val, max_val):
    """
    Checks if value is within given range.
    Returns True/False.
    """
    return min_val <= value <= max_val


# SANITIZE STRING INPUT
def clean_string(text):
    """
    Removes leading/trailing spaces and collapses multiple spaces.
    """
    return " ".join(text.strip().split())


# CHECK EMPTY STRING
def is_empty(text):
    """Returns True if string is empty or only spaces."""
    return text.strip() == ""
