"""holiday_api.py - Fetches public holiday data from the Nager.Date API."""

from typing import Any
import requests

class HolidayAPIError(Exception):
      """Raised when holiday data cannot be retrieved. """
      pass

class Holiday:
      """Represents a single public holiday."""

      def __init__(self, name,  date, holiday_type  ) -> None:   
          """Store the holiday's name, date, and type.""" 

          self.name = name
          self.date = date
          self.holiday_type = holiday_type
   
      def __str__(self) -> str:
          """Return a readable one-line description of the holiday."""
          
          return f"{self.date} - {self.name} ({self.holiday_type})"   
        
class Country:
      """Represents a country by its name and ISO country code."""

      def __init__(self, name, code ) -> None:
          """Store the country's name and its cleaned, uppercase code."""

          self.name = name
          self.code = code.strip().upper()

      def __str__(self) -> str:
          """Return the country as 'Name (CODE)', e.g. 'Nigeria (NG)'."""

          return f"{self.name} ({self.code})"       

            
class HolidayAPIClient:
      """Fetches public holiday data from the Nager.Date API."""

      def __init__(self) -> None:
          """Set up the API's base URL."""

          self.base_url = "https://date.nager.at/api/v3"

      def get_holidays(self, country_code, year)-> list[Any]:
          """Return a list of Holiday objects for the given country code and year."""

          url = f"{self.base_url}/PublicHolidays/{year}/{country_code}"

          try:
              response = requests.get(url, timeout= 10) 
          except requests.exceptions.RequestException:
              raise HolidayAPIError("Could not connect to the holiday service. Check your internet connection.")       

          if response.status_code == 404:
              raise HolidayAPIError(
                        f"No holiday data found for country code '{country_code}' in {year}. "
                        + "Check that the code is valid (e.g. NG, US, GB) and the year is supported."
              )

          if response.status_code != 200:
              raise HolidayAPIError(   
                        f"The holiday service returned an unexpected response (status {response.status_code}). "
                        + "Please try again later."
              )                   

          data = response.json()

          if not data:
              raise HolidayAPIError( f"No public holidays were found for '{country_code}' in {year}." )

          holidays = []
          for item in data:
              holiday = Holiday(
                   name = item["name"],
                   date = item["date"],
                   holiday_type =", ".join(item["types"]),
              )
              holidays.append(holiday)

          return holidays

      def get_available_countries(self) -> list[Any]:
          """Return a list of Country objects for all countries the API supports."""

          url = f"{self.base_url}/AvailableCountries" 

          try:
              response = requests.get(url, timeout= 10)
          except requests.exceptions.RequestException:
              raise HolidayAPIError("Could not connect to the holiday service. Check your internet connection.") 

          if response.status_code != 200:
              raise HolidayAPIError(f"Unexpected error occurred: status{response.status_code} ") 

          data = response.json()   

          if not data:
              raise HolidayAPIError ("No countries were returned by the holiday service.")
          countries = []
          for item in data:
                  country = Country(
                        name = item["name"],
                        code = item["countryCode"]
                  )
                  countries.append(country)
          return countries      
                  


if __name__ == "__main__":
    client = HolidayAPIClient()
    for code, year in [("NG", 2026), ("XX", 2026)]:
        try:
            for holiday in client.get_holidays(code, year):
                print(holiday)
        except HolidayAPIError as error:
            print(f"Error: {error}")

    countries = client.get_available_countries()
    print(len(countries))
    print(countries[0])
