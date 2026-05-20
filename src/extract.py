import requests
import json
import os
from datetime import datetime

# Cities we want to track
CITIES = ["London", "Paris", "Munich", "New York", "Tokyo"]

# Free API — no key needed
BASE_URL = "https://wttr.in/{city}?format=j1"


def fetch_weather(city: str) -> dict:
    """Fetch raw weather data for a single city."""
    url = BASE_URL.format(city=city.replace(" ", "+"))
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # raises an error if the request failed
    return response.json()


def extract_all_cities() -> list[dict]:
    """Fetch weather for all cities and return as a list of raw records."""
    results = []

    for city in CITIES:
        print(f"Fetching weather for {city}...")
        try:
            raw = fetch_weather(city)

            # Pull out just the fields we care about
            current = raw["current_condition"][0]
            record = {
                "city": city,
                "extracted_at": datetime.utcnow().isoformat(),
                "temp_c": int(current["temp_C"]),
                "feels_like_c": int(current["FeelsLikeC"]),
                "humidity_pct": int(current["humidity"]),
                "weather_desc": current["weatherDesc"][0]["value"],
                "wind_kmph": int(current["windspeedKmph"]),
            }
            results.append(record)
            print(f"  ✓ {city}: {record['temp_c']}°C, {record['weather_desc']}")

        except Exception as e:
            print(f"  ✗ Failed for {city}: {e}")

    return results


if __name__ == "__main__":
    data = extract_all_cities()
    print(f"\nExtracted {len(data)} cities successfully")
    print(json.dumps(data[0], indent=2))  # preview first record