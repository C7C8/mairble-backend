import json
import time

from app.analysis.pricing_analysis import analyze_night


def main():
    with open("nightly_records.json") as f:
        records = json.load(f)
    results = []
    for i, record in enumerate(records):
        print(f"Analyzing {record['date']} for {record['listing_name']}...")
        ai_output = analyze_night(record)
        record['ai_analysis'] = ai_output
        results.append(record)
        time.sleep(1.2)  # To avoid rate limits
    with open("nightly_records_with_ai.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Exported nightly_records_with_ai.json")


if __name__ == "__main__":
    main()