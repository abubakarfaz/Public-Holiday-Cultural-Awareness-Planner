import unittest
import os
import shutil
from modules.favourites import FavouritesManager

class TestFavouritesManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests/temp_data"
        self.fav_file = os.path.join(self.test_dir, "test_favs.json")
        self.guides_file = os.path.join(self.test_dir, "test_guides.json")
        self.manager = FavouritesManager(self.fav_file, self.guides_file)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_add_and_get_favourite(self):
        result = self.manager.add_favourite_country("NG", "Nigeria")
        self.assertTrue(result)
        favs = self.manager.get_favourite_countries()
        self.assertEqual(len(favs), 1)
        self.assertEqual(favs[0]["code"], "NG")

    def test_prevent_duplicate_favourite(self):
        self.manager.add_favourite_country("NG", "Nigeria")
        duplicate = self.manager.add_favourite_country("NG", "Nigeria")
        self.assertFalse(duplicate)

    def test_save_and_retrieve_guide(self):
        self.manager.save_holiday_guide("NG", 2026, [{"name": "Independence Day"}], "Cultural Insight")
        guide = self.manager.get_saved_guide("NG", 2026)
        self.assertIsNotNone(guide)
        self.assertEqual(guide["country_code"], "NG")

if __name__ == "__main__":
    unittest.main()