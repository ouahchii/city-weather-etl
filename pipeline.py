import sys
import os
import time
import csv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.extract import extract_all_cities


def save_to_seed(raw_data: list[dict], seed_path: str):
    """Save extracted data as a dbt seed CSV."""
    os.makedirs(os.path.dirname(seed_path), exist_ok=True)
    with open(seed_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=raw_data[0].keys())
        writer.writeheader()
        writer.writerows(raw_data)
    print(f"  ✓ Saved seed to {seed_path}")


def run_pipeline():
    start = time.time()
    print("=" * 50)
    print("  city-weather-etl pipeline starting")
    print("=" * 50)

    # Step 1 — Extract
    print("\n[1/3] Extracting weather data...")
    raw_data = extract_all_cities()
    print(f"  ✓ Extracted {len(raw_data)} cities")

    # Step 2 — Save as dbt seed
    print("\n[2/3] Saving to dbt seed...")
    save_to_seed(raw_data, "weather_transform/seeds/raw_weather.csv")

    # Step 3 — Run dbt
    print("\n[3/3] Running dbt models...")
    os.chdir("weather_transform")
    os.system("dbt seed && dbt run")
    os.chdir("..")

    elapsed = round(time.time() - start, 1)
    print("\n" + "=" * 50)
    print(f"  Pipeline complete in {elapsed}s")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()