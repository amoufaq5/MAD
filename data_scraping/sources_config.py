# data_scraping/sources_config.py
import requests
from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(
    filename='scraper.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

# We'll define a list of dictionaries, each describing how to scrape a source.
# Adjust each parser function for the specific site's structure.

SOURCES = [
    {
        "name": "FDA_Drug_Databases",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases",
        "parser": "generic_parser"
    },
    {
        "name": "Drugs_com",
        "url": "https://www.drugs.com",
        "parser": "generic_parser"
    },
    {
        "name": "DailyMed",
        "url": "https://dailymed.nlm.nih.gov/dailymed/index.cfm",
        "parser": "generic_parser"
    },
    {
        "name": "MedlinePlus",
        "url": "https://medlineplus.gov",
        "parser": "generic_parser"
    },
    {
        "name": "CDC",
        "url": "https://www.cdc.gov",
        "parser": "generic_parser"
    },
    {
        "name": "WHO",
        "url": "https://www.who.int",
        "parser": "generic_parser"
    },
    {
        "name": "Mayo_Clinic",
        "url": "https://www.mayoclinic.org",
        "parser": "generic_parser"
    },
    {
        "name": "WebMD",
        "url": "https://www.webmd.com",
        "parser": "generic_parser"
    },
    {
        "name": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov",
        "parser": "generic_parser"
    },
    {
        "name": "Cochrane_Library",
        "url": "https://www.cochranelibrary.com",
        "parser": "generic_parser"
    },
    {
        "name": "ClinicalTrials",
        "url": "https://clinicaltrials.gov",
        "parser": "generic_parser"
    },
    {
        "name": "PubMedCentral",
        "url": "https://www.ncbi.nlm.nih.gov/pmc/",
        "parser": "generic_parser"
    }
]

def generic_parser(html_content, url):
    """
    A generic parser that:
    - Extracts <title>
    - Extracts raw text
    - Attempts to guess disease, symptom, medication from simple regex (as a placeholder)
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Title
    title_tag = soup.find("title")
    title_text = title_tag.get_text().strip() if title_tag else "No Title"

    # Content
    for script in soup(["script", "style"]):
        script.decompose()
    raw_text = soup.get_text(separator="\n")

    # Simple placeholder extractions:
    disease_match = re.findall(r"(cold|pneumonia|bronchitis|influenza|herpes|covid|hepatitis b|chlamydia|chicken pox)", raw_text, re.IGNORECASE)
    symptom_match = re.findall(r"(cough|fever|fatigue|headache|rash|sore throat)", raw_text, re.IGNORECASE)
    medication_match = re.findall(r"(acetaminophen|ibuprofen|antiviral|vaccine|antibiotic)", raw_text, re.IGNORECASE)

    # For demonstration, we'll just convert them to comma-separated strings
    disease_text = ", ".join(set([d.lower() for d in disease_match])) if disease_match else ""
    symptom_text = ", ".join(set([s.lower() for s in symptom_match])) if symptom_match else ""
    medication_text = ", ".join(set([m.lower() for m in medication_match])) if medication_match else ""

    return {
        "disease": disease_text,
        "symptoms": symptom_text,
        "medication": medication_text,
        "content": raw_text[:10000],  # limit size for demonstration
        "title": title_text
    }
