class ComparisonModule:
    """
    Comparison Module - Compares holidays between two countries.
    """

    @staticmethod
    def compare_holidays(country1_holidays, country2_holidays, country1_code="Country 1", country2_code="Country 2"):
        """
        Compares two lists of Holiday objects or dictionaries.
        """
        shared_holidays = []
        overlapping_dates = []
        unique_country1 = []
        unique_country2 = []

        def parse_item(item):
            if isinstance(item, dict):
                return item.get("name", ""), item.get("date", ""), item.get("holiday_type", item.get("type", "Public"))
            return getattr(item, "name", ""), getattr(item, "date", ""), getattr(item, "holiday_type", "Public")

        c2_by_date = {}
        c2_by_name = {}
        for h in country2_holidays:
            name, date, h_type = parse_item(h)
            if date:
                c2_by_date[date] = (name, date, h_type)
            if name:
                c2_by_name[name.lower()] = (name, date, h_type)

        matched_c2_dates = set()
        matched_c2_names = set()

        for h1 in country1_holidays:
            name1, date1, type1 = parse_item(h1)
            name1_lower = name1.strip().lower()

            if name1_lower in c2_by_name:
                c2_name, c2_date, c2_type = c2_by_name[name1_lower]
                shared_holidays.append({
                    "name": name1,
                    f"{country1_code}_date": date1,
                    f"{country2_code}_date": c2_date,
                    "type": type1
                })
                matched_c2_dates.add(c2_date)
                matched_c2_names.add(name1_lower)

            elif date1 in c2_by_date:
                c2_name, c2_date, c2_type = c2_by_date[date1]
                overlapping_dates.append({
                    "date": date1,
                    f"{country1_code}_holiday": name1,
                    f"{country2_code}_holiday": c2_name
                })
                matched_c2_dates.add(date1)

            else:
                unique_country1.append({"name": name1, "date": date1, "type": type1})

        for h2 in country2_holidays:
            name2, date2, type2 = parse_item(h2)
            if date2 not in matched_c2_dates and name2.lower() not in matched_c2_names:
                unique_country2.append({"name": name2, "date": date2, "type": type2})

        return {
            "summary": {
                "country1": country1_code,
                "country2": country2_code,
                "total_shared": len(shared_holidays),
                "total_overlapping": len(overlapping_dates)
            },
            "shared_holidays": shared_holidays,
            "overlapping_dates": overlapping_dates,
            f"unique_to_{country1_code}": unique_country1,
            f"unique_to_{country2_code}": unique_country2
        }
