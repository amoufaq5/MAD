import requests
import logging
import os
import json

# Set up logging configuration for API scraping
logging.basicConfig(
    filename='api_scraper.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

def scrape_clinical_trials(output_file):
    try:
        url = "https://clinicaltrials.gov/api/query/study_fields"
        params = {
            "expr": "common cold pneumonia bronchitis influenza herpes covid hepatitis b chlamydia chicken pox",
            "fields": "NCTId,Condition,Intervention",
            "min_rnk": 1,
            "max_rnk": 100,
            "fmt": "json"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Successfully scraped ClinicalTrials.gov API data to {output_file}")
    except Exception as e:
        logging.error(f"Error scraping ClinicalTrials.gov API: {e}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    output_file = os.path.join("data/raw", "clinical_trials.json")
    scrape_clinical_trials(output_file)
