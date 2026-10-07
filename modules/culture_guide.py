"""culture_guide.py - Generates cultural/historical explanations and greetings using the Gemini API."""

import os
import requests


class CultureGuideError(Exception):
    """Raised when a cultural guide cannot be generated."""
    pass


class CultureGuideGenerator:
    """Generates cultural/historical explanations and greetings for a holiday using the Gemini API."""

    def __init__(self, api_key: str = None) -> None:
        """Set up the Gemini API key and endpoint.

        If api_key is not passed in, it's read from the GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.base_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash:generateContent"
        )

        if not self.api_key:
            raise CultureGuideError(
                "No Gemini API key found. Set the GEMINI_API_KEY environment "
                "variable or pass api_key when creating CultureGuideGenerator."
            )

    def _call_gemini(self, prompt: str) -> str:
        """Send a prompt to the Gemini API and return the generated text."""
        url = f"{self.base_url}?key={self.api_key}"
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        try:
            response = requests.post(url, json=payload, timeout=15)
        except requests.exceptions.RequestException:
            raise CultureGuideError(
                "Could not connect to the Gemini API. Check your internet connection."
            )

        if response.status_code == 401:
            raise CultureGuideError(
                "Gemini API rejected the request. Check that your API key is valid."
            )

        if response.status_code != 200:
            raise CultureGuideError(
                f"The Gemini API returned an unexpected response (status {response.status_code}). "
                "Please try again later."
            )

        data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError):
            raise CultureGuideError(
                "The Gemini API response was empty or in an unexpected format."
            )

    def get_cultural_explanation(self, holiday_name: str, country_name: str) -> str:
        """Return a short explanation of the cultural/historical meaning of a holiday."""
        prompt = (
            f"In 2-3 sentences, explain the cultural or historical significance of "
            f"'{holiday_name}' as celebrated in {country_name}. Keep it factual and concise."
        )
        return self._call_gemini(prompt)

    def get_greeting_suggestion(self, holiday_name: str, country_name: str) -> str:
        """Return a suggested greeting or custom associated with a holiday."""
        prompt = (
            f"In 1-2 sentences, suggest an appropriate greeting or common custom "
            f"for '{holiday_name}' as celebrated in {country_name}."
        )
        return self._call_gemini(prompt)

    def get_full_guide(self, holiday_name: str, country_name: str) -> dict:
        """Return both the cultural explanation and greeting suggestion for a holiday."""
        return {
            "holiday_name": holiday_name,
            "country_name": country_name,
            "explanation": self.get_cultural_explanation(holiday_name, country_name),
            "greeting": self.get_greeting_suggestion(holiday_name, country_name),
        }


if __name__ == "__main__":
    try:
        generator = CultureGuideGenerator()
        guide = generator.get_full_guide("New Year's Day", "Nigeria")
        print(guide)
    except CultureGuideError as error:
        print(f"Error: {error}")
