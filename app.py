import os

from dotenv import load_dotenv
import streamlit as st

from modules.comparison import ComparisonModule
from modules.culture_guide import CultureGuideError, CultureGuideGenerator
from modules.favourites import FavouritesManager
from modules.holiday_api import HolidayAPIClient, HolidayAPIError
from modules.validation import ValidationError, validate_country_code, validate_year


def get_manager() -> FavouritesManager:
    return FavouritesManager(
        fav_filepath="data/favourites.json",
        guides_filepath="data/saved_guides.json",
    )


def show_holiday_list(holidays):
    if not holidays:
        st.write("No holidays found.")
        return

    for holiday in holidays:
        st.write(f"{holiday.date} - {holiday.name} ({holiday.holiday_type})")


load_dotenv()


def main() -> None:
    st.set_page_config(page_title="Public Holiday Planner", layout="centered")
    st.title("Public Holiday Planner")
    st.write("Simple holiday lookup, comparison, and saved favourites.")

    manager = get_manager()

    st.header("Favourites")
    with st.form("add_favourite_form"):
        country_code = st.text_input("Country code", value="NG")
        country_name = st.text_input("Country name", value="Nigeria")
        submitted = st.form_submit_button("Add favourite")

        if submitted:
            try:
                cleaned_code = validate_country_code(country_code)
                if manager.add_favourite_country(cleaned_code, country_name):
                    st.success(f"Added {country_name.strip()} ({cleaned_code}).")
                    st.rerun()
                else:
                    st.warning(f"{cleaned_code} is already in favourites.")
            except ValidationError as exc:
                st.error(str(exc))

    favourites = manager.get_favourite_countries()
    if favourites:
        for favourite in favourites:
            code = favourite.get("code", "Unknown")
            name = favourite.get("name", "Unnamed country")
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{name} ({code})")
            with col2:
                if st.button("Remove", key=f"remove_{code}_{name}"):
                    manager.remove_favourite_country(code)
                    st.rerun()
    else:
        st.write("No favourite countries saved yet.")

    st.header("Holiday lookup")
    with st.form("holiday_lookup_form"):
        lookup_code = st.text_input("Country code", value="NG")
        lookup_year = st.number_input("Year", min_value=1900, max_value=2100, value=2026, step=1)
        lookup_submit = st.form_submit_button("Search holidays")

        if lookup_submit:
            try:
                cleaned_code = validate_country_code(lookup_code)
                validated_year = validate_year(lookup_year)
                client = HolidayAPIClient()
                holidays = client.get_holidays(cleaned_code, validated_year)
                st.write(f"Public holidays for {cleaned_code} in {validated_year}")
                show_holiday_list(holidays)
            except (ValidationError, HolidayAPIError) as exc:
                st.error(str(exc))

    st.header("Compare countries")
    with st.form("compare_form"):
        country_one = st.text_input("First country code", value="NG")
        country_two = st.text_input("Second country code", value="US")
        compare_year = st.number_input("Year", min_value=1900, max_value=2100, value=2026, step=1)
        compare_submit = st.form_submit_button("Compare")

        if compare_submit:
            try:
                code_1 = validate_country_code(country_one)
                code_2 = validate_country_code(country_two)
                year = validate_year(compare_year)
                api_client = HolidayAPIClient()
                holiday_list_1 = api_client.get_holidays(code_1, year)
                holiday_list_2 = api_client.get_holidays(code_2, year)
                comparison = ComparisonModule.compare_holidays(
                    holiday_list_1,
                    holiday_list_2,
                    code_1,
                    code_2,
                )

                summary = comparison["summary"]
                st.write(
                    f"Shared holidays: {summary['total_shared']} | "
                    f"Overlapping dates: {summary['total_overlapping']}"
                )

                if comparison["shared_holidays"]:
                    st.write("Shared holidays:")
                    for item in comparison["shared_holidays"]:
                        st.write(f"- {item['name']} ({item[f'{code_1}_date']} / {item[f'{code_2}_date']})")
                else:
                    st.write("No shared holiday names found.")

                if comparison[f"unique_to_{code_1}"]:
                    st.write(f"Unique to {code_1}:")
                    for item in comparison[f"unique_to_{code_1}"]:
                        st.write(f"- {item['name']} ({item['date']})")

                if comparison[f"unique_to_{code_2}"]:
                    st.write(f"Unique to {code_2}:")
                    for item in comparison[f"unique_to_{code_2}"]:
                        st.write(f"- {item['name']} ({item['date']})")

            except (ValidationError, HolidayAPIError) as exc:
                st.error(str(exc))

    st.header("Cultural guide")
    with st.form("culture_guide_form"):
        guide_country = st.text_input("Country name", value="Nigeria")
        guide_holiday = st.text_input("Holiday name", value="Independence Day")
        guide_submit = st.form_submit_button("Generate guide")

        if guide_submit:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                st.warning("Set the GEMINI_API_KEY environment variable to generate cultural guide text.")
            else:
                try:
                    generator = CultureGuideGenerator(api_key=api_key)
                    guide = generator.get_full_guide(guide_holiday, guide_country)
                    st.write("Explanation:")
                    st.write(guide["explanation"])
                    st.write("Greeting suggestion:")
                    st.write(guide["greeting"])
                except CultureGuideError as exc:
                    st.error(str(exc))

    st.header("Saved guides")
    saved_guides = manager.list_saved_guides()
    if saved_guides:
        for guide in saved_guides:
            country = guide.get("country_code", "Unknown")
            year = guide.get("year", "Unknown")
            with st.expander(f"{country} - {year}"):
                st.write(guide.get("ai_insights", "No insight saved."))
                for holiday in guide.get("holidays", []):
                    st.write(f"- {holiday.get('name', 'Unnamed holiday')}")
    else:
        st.write("No saved holiday guides yet.")


if __name__ == "__main__":
    main()

