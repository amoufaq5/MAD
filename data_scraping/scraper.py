import requests
import logging
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='scraper.log',
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

# Dictionary of sources including Drugs.com OTC
SOURCES = {
    "FDA_Drug_Databases": "https://www.fda.gov/drugs/drug-approvals-and-databases",
    "Drugs_com_Home": "https://www.drugs.com",
    "Drugs_com_OTC": "https://www.drugs.com/otc.html",  # Specifically for OTC meds
    "DailyMed": "https://dailymed.nlm.nih.gov/dailymed/index.cfm",
    "MedlinePlus": "https://medlineplus.gov",
    "CDC": "https://www.cdc.gov",
    "WHO": "https://www.who.int",
    "Mayo_Clinic": "https://www.mayoclinic.org",
    "WebMD": "https://www.webmd.com",
    "PubMed": "https://pubmed.ncbi.nlm.nih.gov",
    "Cochrane_Library": "https://www.cochranelibrary.com",
    "ClinicalTrials_Home": "https://clinicaltrials.gov",
    "PubMedCentral": "https://www.pubmedcentral.nih.gov"
}

def scrape_site(url, output_file):
    """
    Generic HTML scrape using requests + BeautifulSoup.
    Removes script/style tags and writes raw text to a file.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MAD/1.0; +http://example.com/bot)'
        }
        logging.info(f"Attempting to scrape: {url}")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()  # Raise HTTPError if status_code >= 400

        soup = BeautifulSoup(response.text, "html.parser")
        # Remove script/style to clean text
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")

        # Write raw text to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)

        logging.info(f"Successfully scraped {url} and saved to {output_file}")
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # Loop through each source in SOURCES
    for name, url in SOURCES.items():
        output_file = os.path.join("data/raw", f"{name}_{timestamp}.txt")
        scrape_site(url, output_file)
