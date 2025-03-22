# data_scraping/webmd_scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_webmd():
    url = "https://www.webmd.com/a-to-z-guides/condition-landing"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    content = " ".join(paragraphs)

    record = {
        "source": "WebMD",
        "disease": "",
        "symptoms": "",
        "medication": "",
        "title": title,
        "content": content,
        "tags": "webmd, consumer health"
    }

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/webmd.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        writer.writeheader()
        writer.writerow(record)

if __name__ == "__main__":
    scrape_webmd()


# data_scraping/medlineplus_scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_medlineplus():
    url = "https://medlineplus.gov/healthtopics.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    content = " ".join(paragraphs)

    record = {
        "source": "MedlinePlus",
        "disease": "",
        "symptoms": "",
        "medication": "",
        "title": title,
        "content": content,
        "tags": "medlineplus, patient education"
    }

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/medlineplus.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        writer.writeheader()
        writer.writerow(record)

if __name__ == "__main__":
    scrape_medlineplus()


# data_scraping/dailymed_scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_dailymed():
    url = "https://dailymed.nlm.nih.gov/dailymed/index.cfm"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    content = " ".join(paragraphs)

    record = {
        "source": "DailyMed",
        "disease": "",
        "symptoms": "",
        "medication": "",
        "title": title,
        "content": content,
        "tags": "dailymed, drug label, dosage"
    }

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/dailymed.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        writer.writeheader()
        writer.writerow(record)

if __name__ == "__main__":
    scrape_dailymed()


# data_scraping/openfda_scraper.py
import requests
import csv
import os

def scrape_openfda():
    url = "https://api.fda.gov/drug/event.json?limit=5"
    response = requests.get(url)
    data = response.json()
    records = []

    for result in data.get("results", []):
        record = {
            "source": "OpenFDA",
            "disease": result.get("patient", {}).get("reaction", [{}])[0].get("reactionmeddrapt", ""),
            "symptoms": "",
            "medication": result.get("patient", {}).get("drug", [{}])[0].get("medicinalproduct", ""),
            "title": "FDA Adverse Event Report",
            "content": str(result),
            "tags": "openfda, adverse events"
        }
        records.append(record)

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/openfda.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    scrape_openfda()


# data_scraping/healthline_scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_healthline():
    url = "https://www.healthline.com/health"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    content = " ".join(paragraphs)

    record = {
        "source": "Healthline",
        "disease": "",
        "symptoms": "",
        "medication": "",
        "title": title,
        "content": content,
        "tags": "healthline, condition info"
    }

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/healthline.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        writer.writeheader()
        writer.writerow(record)

if __name__ == "__main__":
    scrape_healthline()


# data_scraping/ema_scraper.py
import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_ema():
    url = "https://www.ema.europa.eu/en/medicines"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("title").get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    content = " ".join(paragraphs)

    record = {
        "source": "EMA",
        "disease": "",
        "symptoms": "",
        "medication": "",
        "title": title,
        "content": content,
        "tags": "ema, european medicine"
    }

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/ema.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        writer.writeheader()
        writer.writerow(record)

if __name__ == "__main__":
    scrape_ema()


# data_scraping/scp.nih_scraper.py
import csv
import os

def scrape_scpd():
    # Simulated data entry from SCPD/NIH dataset
    records = [
        {
            "source": "NIH SCPD",
            "disease": "bronchitis",
            "symptoms": "cough, mucus, chest pain",
            "medication": "albuterol",
            "title": "Bronchitis Dataset Record",
            "content": "Sample dataset row from SCPD NIH.",
            "tags": "scp.nih, dataset, symptoms"
        }
    ]

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/scp.nih.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    scrape_scpd()
