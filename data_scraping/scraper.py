import requests
import logging
from bs4 import BeautifulSoup
import os

# Set up logging configuration for web scraping
logging.basicConfig(
    filename='scraper.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

# Dictionary of reputable sources and their URLs
SOURCES = {
    "FDA_Drug_Databases": "https://www.fda.gov/drugs/drug-approvals-and-databases",
    "Drugs.com": "https://www.drugs.com",
    "DailyMed": "https://dailymed.nlm.nih.gov/dailymed/index.cfm",
    "MedlinePlus": "https://medlineplus.gov",
    "CDC": "https://www.cdc.gov",
    "WHO": "https://www.who.int",
    "Mayo_Clinic": "https://www.mayoclinic.org",
    "WebMD": "https://www.webmd.com",
    "PubMed": "https://pubmed.ncbi.nlm.nih.gov",
    "Cochrane_Library": "https://www.cochranelibrary.com",
    "ClinicalTrials": "https://clinicaltrials.gov",
    "PubMedCentral": "https://www.pubmedcentral.nih.gov"
}

def scrape_site(url, output_file):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AI Medical Diagnostic Bot/1.0; +http://yourdomain.com/bot)'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad responses

        soup = BeautifulSoup(response.content, "html.parser")
        # Remove scripts and styles for cleaner text extraction
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Successfully scraped {url} to {output_file}")
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    for source, url in SOURCES.items():
        output_file = os.path.join("data/raw", f"{source}.txt")
        logging.info(f"Starting scrape for {source}: {url}")
        scrape_site(url, output_file)
