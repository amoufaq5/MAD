import requests
from bs4 import BeautifulSoup
import os

# Dictionary of source names and their URLs
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
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, "html.parser")
        # Remove scripts and styles for cleaner text extraction
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved scraped content from {url} to {output_file}")
    except Exception as e:
        print(f"Failed to scrape {url}. Error: {e}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    for source, url in SOURCES.items():
        output_file = os.path.join("data/raw", f"{source}.txt")
        print(f"Scraping {source}: {url}")
        scrape_site(url, output_file)
