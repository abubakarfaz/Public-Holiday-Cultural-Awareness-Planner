class ComparisonModule:
    """Comparison Module - Compares holidays between two countries."""

    @staticmethod
    def compare_holidays(country1_holidays, country2_holidays, country1_code="Country 1", country2_code="Country 2"):
        """Compare two lists of Holiday objects or dictionaries."""
        shared_holidays = []
        overlapping_dates = []
        unique_country1 = []
        unique_country2 = []

        def parse_item(item):
            if isinstance(item, dict):
                name = item.get("name") or ""
                date = item.get("date") or ""
                holiday_type = item.get("holiday_type") or item.get("type") or "Public"
                return str(name), str(date), str(holiday_type)

            name = getattr(item, "name", "") or ""
            date = getattr(item, "date", "") or ""
            holiday_type = getattr(item, "holiday_type", "") or "Public"
            return str(name), str(date), str(holiday_type)

        country2_by_date = {}
        country2_by_name = {}
        for holiday in country2_holidays:
            name, date, holiday_type = parse_item(holiday)
            if date:
                country2_by_date[date] = {"name": name, "date": date, "type": holiday_type}
            if name:
                country2_by_name[name.strip().lower()] = {"name": name, "date": date, "type": holiday_type}

        matched_country2_dates = set()
        matched_country2_names = set()

        for holiday in country1_holidays:
            name, date, holiday_type = parse_item(holiday)
            name_lower = name.strip().lower()

            if name_lower and name_lower in country2_by_name:
                matched_holiday = country2_by_name[name_lower]
                shared_holidays.append({
                    "name": name,
                    f"{country1_code}_date": date,
                    f"{country2_code}_date": matched_holiday["date"],
                    "type": holiday_type,
                })
                if matched_holiday.get("date"):
                    matched_country2_dates.add(matched_holiday["date"])
                matched_country2_names.add(name_lower)
            elif date and date in country2_by_date:
                matched_holiday = country2_by_date[date]
                overlapping_dates.append({
                    "date": date,
                    f"{country1_code}_holiday": name,
                    f"{country2_code}_holiday": matched_holiday["name"],
                })
                matched_country2_dates.add(date)
            else:
                unique_country1.append({"name": name, "date": date, "type": holiday_type})

        for holiday in country2_holidays:
            name, date, holiday_type = parse_item(holiday)
            name_lower = name.strip().lower()
            if date not in matched_country2_dates and name_lower not in matched_country2_names:
                unique_country2.append({"name": name, "date": date, "type": holiday_type})

        return {
            "summary": {
                "country1": country1_code,
                "country2": country2_code,
                "total_shared": len(shared_holidays),
                "total_overlapping": len(overlapping_dates),
            },
            "shared_holidays": shared_holidays,
            "overlapping_dates": overlapping_dates,
            f"unique_to_{country1_code}": unique_country1,
            f"unique_to_{country2_code}": unique_country2,
        }
