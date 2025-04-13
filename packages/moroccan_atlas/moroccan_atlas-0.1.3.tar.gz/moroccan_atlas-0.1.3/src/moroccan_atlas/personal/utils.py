from .constants import CIN_PREFIX_MAP


def find_city_by_cin_prefix(prefix: str) -> str:
    """
    Finds the city corresponding to a given CIN prefix.
    """
    prefix = prefix.upper()

    for city, prefixes in CIN_PREFIX_MAP.items():
        if prefix in prefixes:
            return city

    raise Exception(f"No city found for prefix: {prefix}") # TODO specify a better exception
