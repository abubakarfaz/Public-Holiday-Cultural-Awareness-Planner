"""validation.py - Validates country codes and year inputs."""

import re


class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


def is_valid_country_code_format(country_code: str) -> bool:
    """Check that a country code is exactly two letters (e.g. NG, US, GB)."""
    pattern = r"^[A-Za-z]{2}$"
    return bool(re.match(pattern, country_code.strip()))


def is_valid_year(year) -> bool:
    """Check that a year is a 4-digit number within a reasonable range."""
    try:
        year_int = int(year)
    except (ValueError, TypeError):
        return False

    return 1900 <= year_int <= 2100


def validate_country_code(country_code: str, available_codes: list = None) -> str:
    """Validate a country code's format, and optionally check it against a known list.

    Returns the cleaned, uppercase code if valid.
    Raises ValidationError if invalid.
    """
    if not is_valid_country_code_format(country_code):
        raise ValidationError(
            f"'{country_code}' is not a valid country code format. "
            "Use a 2-letter code like NG, US, or GB."
        )

    cleaned_code = country_code.strip().upper()

    if available_codes is not None and cleaned_code not in available_codes:
        raise ValidationError(
            f"'{cleaned_code}' is not a supported country code."
        )

    return cleaned_code


def validate_year(year) -> int:
    """Validate a year input.

    Returns the year as an int if valid.
    Raises ValidationError if invalid.
    """
    if not is_valid_year(year):
        raise ValidationError(
            f"'{year}' is not a valid year. Enter a year between 1900 and 2100."
        )

    return int(year)


if __name__ == "__main__":
    # Quick manual tests
    test_cases = ["NG", " ng ", "US", "XYZ", "1", "", "123"]
    for code in test_cases:
        try:
            print(validate_country_code(code))
        except ValidationError as error:
            print(f"Error: {error}")

    year_cases = [2026, "2026", "abc", 1800, 2200]
    for year in year_cases:
        try:
            print(validate_year(year))
        except ValidationError as error:
            print(f"Error: {error}")
