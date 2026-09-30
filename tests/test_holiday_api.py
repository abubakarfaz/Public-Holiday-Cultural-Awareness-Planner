import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "modules"))

from holiday_api import Holiday, Country, HolidayAPIClient, HolidayAPIError

class TestHoliday(unittest.TestCase):
    """Tests for the Holiday class."""

    def test_str_format(self):
        """Check that __str__ formats correctly."""
        holiday = Holiday(name="New Year's Day", date="2026-01-01", holiday_type="Public")
        result = str(holiday)
        self.assertEqual(result, "2026-01-01 - New Year's Day (Public)")

class TestCountry(unittest.TestCase):
    """Tests for the Country class."""

    def test_code_is_cleaned(self) -> None:
        """Check that the country code is stripped and uppercased."""
        country = Country(name="Nigeria", code =" ng ")
        self.assertEqual(country.code, "NG")

    def test_str_format(self) -> None:
        """Check that __str__ formats correctly."""
        country = Country(name = "Nigeria", code = "NG")
        result = str(country)
        self.assertEqual(result, "Nigeria (NG)")        

class TestHolidayAPIClient(unittest.TestCase):
    """Tests for the HolidayAPIClient class (live API calls)."""

    def setUp(self) -> None:
        """Create a client before each test."""
        self.client = HolidayAPIClient()

    def test_get_holidays_returns_list(self) -> None:
        """Check that a valid country/year returns Holiday objects."""
        holidays = self.client.get_holidays(country_code="NG", year=2026)
        self.assertGreater(len(holidays), 0)
        self.assertIsInstance(holidays[0], Holiday )

    def test_get_holidays_invalid_code_raises_error(self) -> None:
        """Check that an invalid country code raises HolidayAPIError."""
        with self.assertRaises(HolidayAPIError):
            self.client.get_holidays(country_code="XX", year=2026)

    def test_get_available_countries_returns_list(self) -> None:
        """Check that the countries list is returned correctly."""
        countries = self.client.get_available_countries()
        self.assertGreater(len(countries), 0)
        self.assertIsInstance(countries[0], Country)

if __name__ == "__main__":
    unittest.main()