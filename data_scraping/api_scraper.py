import requests
import os
import json

def scrape_clinical_trials(output_file):
    try:
        # Using the ClinicalTrials.gov API as an example for a data-rich source
        url = "https://clinicaltrials.gov/api/query/study_fields"
        params = {
            "expr": "common cold pneumonia bronchitis influenza herpes covid hepatitis b chlamydia chicken pox",
            "fields": "NCTId,Condition,Intervention",
            "min_rnk": 1,
            "max_rnk": 100,
            "fmt": "json"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Saved clinical trials data to {output_file}")
    except Exception as e:
        print(f"Failed to scrape ClinicalTrials.gov API. Error: {e}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    output_file = os.path.join("data/raw", "clinical_trials.json")
    scrape_clinical_trials(output_file)
