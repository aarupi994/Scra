import requests
import json

# API base URL
BASE_URL = "https://osintapi.store/cutieee/api.php?key=jerry&type=mobile&term="

# Only 6 and 7 series number ranges
ranges = [
    (6000000000, 6999999999),
    (7000000000, 7999999999),
]

# Function to fetch data for one number with +91 prefix
def fetch_number_data(number):
    try:
        full_number = "+91" + str(number)
        url = BASE_URL + full_number
        r = requests.get(url, timeout=5)
        if r.status_code == 200 and r.text.strip():
            return {full_number: r.json()}
    except Exception:
        pass
    return None

# Save results line by line
def save_results(data, filename="output.json"):
    with open(filename, "a", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Main scraper function
def run_scraper():
    for start, end in ranges:
        for number in range(start, end + 1):
            data = fetch_number_data(number)
            if data:
                save_results([data])
            print(f"Processed {number}")

if __name__ == "__main__":
    run_scraper()
