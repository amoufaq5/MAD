# data_scraping/scraper.py
import os
import logging
import pandas as pd
import requests
from sources_config import SOURCES, generic_parser

logging.basicConfig(
    filename='scraper.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

def scrape_and_save_excel(output_excel="data/aggregated.xlsx"):
    os.makedirs("data/raw", exist_ok=True)
    records = []

    for source_info in SOURCES:
        name = source_info["name"]
        url = source_info["url"]
        parser_name = source_info["parser"]

        logging.info(f"Scraping {name} from {url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; AI Medical Diagnostic Bot/1.0; +http://yourdomain.com/bot)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Save raw HTML
            raw_file = os.path.join("data/raw", f"{name}.html")
            with open(raw_file, "wb") as f:
                f.write(response.content)

            # Parse
            if parser_name == "generic_parser":
                parsed_data = generic_parser(response.content, url)
            else:
                parsed_data = {}

            # Build record
            record = {
                "disease": parsed_data.get("disease", ""),
                "symptoms": parsed_data.get("symptoms", ""),
                "medication": parsed_data.get("medication", ""),
                "content": parsed_data.get("content", ""),
                "title": parsed_data.get("title", "")
            }
            records.append(record)

            logging.info(f"Successfully scraped {name}")
        except Exception as e:
            logging.error(f"Error scraping {name}: {e}")

    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(records, columns=["disease", "symptoms", "medication", "content", "title"])
    df.to_excel(output_excel, index=False)
    logging.info(f"Aggregated data saved to {output_excel}")

if __name__ == "__main__":
    scrape_and_save_excel()
