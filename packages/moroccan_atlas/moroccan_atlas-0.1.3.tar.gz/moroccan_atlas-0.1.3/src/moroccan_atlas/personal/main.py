import re
from typing import Dict
from .constants import CIN_REGEXP
from .utils import find_city_by_cin_prefix


########################################################################
# Carte d'Identite Nationale (CIN)
########################################################################
def is_valid_cin(value: str) -> bool:
    """
    # TODO
    Examples: AB123456, K45678
    """
    return bool(re.fullmatch(CIN_REGEXP, value.upper()))


def parse_cin(value: str) -> Dict[str, str]:
    """
    Parses a Moroccan CIN, validates the format, and extracts useful information.

    Parameters:
        value (str): CIN string (e.g., 'AB123456')

    Returns:
        dict: A dictionary with 'prefix', 'number', and 'origin' keys.
    """
    value = value.strip().upper()
    if not is_valid_cin(value):
        raise Exception(f"Invalid CIN format: {value}")

    # Extract structured information using the extractor
    match = re.fullmatch(CIN_REGEXP, value)
    if not match:
        return None # TODO

    prefix, number, suffix = match.groups()
    # origin = CIN_PREFIX_MAP.get(prefix)
    origin = find_city_by_cin_prefix(prefix)

    return {
        "prefix": prefix,
        "number": number,
        "origin": origin  # could be None if unknown
    }


########################################################################
# Phone number
########################################################################
def is_valid_phone(value: str) -> bool:
    """
    Validates Moroccan phone number.
    Formats: starts with +212, 212, or 0 followed by 9 digits.
    Examples: +212612345678, 0612345678, 212612345678
    """
    normalized = re.sub(r'\s|-|\.', '', value)
    return bool(re.fullmatch(r'(\+212|212|0)([5-7]\d{8})', normalized))

########################################################################
# Passport number
########################################################################
def is_valid_passport(value: str) -> bool:
    """
    Validates Moroccan passport number.
    Typically starts with a letter followed by 7 digits.
    Example: U1234567
    """
    return bool(re.fullmatch(r'[A-Z]\d{7}', value.upper()))


# Bank account (RIB)
def is_valid_rib(value: str) -> bool:
    """
    Validates Moroccan RIB.
    Format: 24 digits, can optionally include spaces.
    Example: 123 456 7890 123456789012
    """
    digits_only = re.sub(r'\s', '', value)
    return bool(re.fullmatch(r'\d{24}', digits_only))