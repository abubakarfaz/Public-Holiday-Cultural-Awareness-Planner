import json
import os
from typing import List, Dict, Any, Optional


class FavouritesManager:
    def __init__(
        self,
        fav_filepath: str = "data/favourites.json",
        guides_filepath: str = "data/saved_guides.json",
    ):
        self.fav_filepath = fav_filepath
        self.guides_filepath = guides_filepath

        os.makedirs(os.path.dirname(self.fav_filepath), exist_ok=True)
        os.makedirs(os.path.dirname(self.guides_filepath), exist_ok=True)

    def _load_json(self, filepath: str) -> list:
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_json(self, filepath: str, data: list) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_favourite_country(
        self, country_code: str, country_name: str
    ) -> bool:
        """Adds a country to favourites if not already present."""
        favs = self._load_json(self.fav_filepath)
        code_upper = country_code.strip().upper()

        for item in favs:
            if item.get("code") == code_upper:
                return False  # Duplicate found

        favs.append({"code": code_upper, "name": country_name.strip()})
        self._save_json(self.fav_filepath, favs)
        return True

    def remove_favourite_country(self, country_code: str) -> bool:
        """Removes a country from favourites."""
        favs = self._load_json(self.fav_filepath)
        code_upper = country_code.strip().upper()
        filtered = [item for item in favs if item.get("code") != code_upper]

        if len(filtered) == len(favs):
            return False  # Nothing removed

        self._save_json(self.fav_filepath, filtered)
        return True

    def get_favourite_countries(self) -> List[Dict[str, str]]:
        """Returns list of favourite countries."""
        return self._load_json(self.fav_filepath)

    def save_holiday_guide(
        self,
        country_code: str,
        year: int,
        holidays: List[Dict[str, Any]],
        ai_insights: str,
    ) -> bool:
        """Saves a full holiday guide so it can be reloaded offline without API calls."""
        guides = self._load_json(self.guides_filepath)
        guide_id = f"{country_code.strip().upper()}_{year}"

        new_guide = {
            "guide_id": guide_id,
            "country_code": country_code.strip().upper(),
            "year": year,
            "holidays": holidays,
            "ai_insights": ai_insights,
        }

        updated = False
        for i, g in enumerate(guides):
            if g.get("guide_id") == guide_id:
                guides[i] = new_guide
                updated = True
                break

        if not updated:
            guides.append(new_guide)

        self._save_json(self.guides_filepath, guides)
        return True

    def get_saved_guide(
        self, country_code: str, year: int
    ) -> Optional[Dict[str, Any]]:
        """Retrieves a saved guide to display without calling external APIs."""
        guides = self._load_json(self.guides_filepath)
        guide_id = f"{country_code.strip().upper()}_{year}"
        for g in guides:
            if g.get("guide_id") == guide_id:
                return g
        return None

    def list_saved_guides(self) -> List[Dict[str, Any]]:
        """Lists all saved holiday guide summaries."""
        return self._load_json(self.guides_filepath)