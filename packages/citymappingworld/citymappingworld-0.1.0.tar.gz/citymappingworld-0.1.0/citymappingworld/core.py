import json
import os

def get_city_options():
    file_path = os.path.join(os.path.dirname(__file__), "worldcitymaster.json")
    with open(file_path, encoding="utf-8") as f:
        cities_data = json.load(f)

    options = []
    for city in cities_data:
        state_part = f"{city['state_name']}, " if city.get('state_name') else ""
        options.append({
            "label": f"{city['name']}, {state_part}{city['country_name']}",
            "utc_offset": city["utc_offset"],
            "latitude": city.get("latitude"),
            "longitude": city.get("longitude")
        })

    return options
