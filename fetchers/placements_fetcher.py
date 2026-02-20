import requests
from bs4 import BeautifulSoup
import json
import os


class PlacementsFetcher:

    def __init__(self):
        self.base_url = "https://www.sphoorthyengg.ac.in"

        self.urls = {
            "about": "/placement",
            "year_wise": "/year-wise-placement",
            "recruiters": "/recruiting-companies",
            "contacts": "/placement-contacts"
        }

    # -------------------------------
    # Fetch HTML
    # -------------------------------
    def fetch_html(self, url):
        response = requests.get(url)
        return response.text

    # -------------------------------
    # Extract only main content area
    # -------------------------------
    def get_main_section(self, soup):
        main_section = soup.find("section", id="main-content")
        return main_section if main_section else soup

    # -------------------------------
    # Clean text utility
    # -------------------------------
    def clean_text(self, soup):
        for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)

        return cleaned

    # -------------------------------
    # About Placements
    # -------------------------------
    def scrape_about(self):
        print("Scraping About Placements...")
        html = self.fetch_html(self.base_url + self.urls["about"])
        soup = BeautifulSoup(html, "html.parser")

        main_section = self.get_main_section(soup)

        return self.clean_text(main_section)

    # -------------------------------
    # Year Wise Placements
    # -------------------------------
    def scrape_year_wise(self):
        print("Scraping Year Wise Placement...")
        html = self.fetch_html(self.base_url + self.urls["year_wise"])
        soup = BeautifulSoup(html, "html.parser")

        main_section = self.get_main_section(soup)

        data = {}

        tables = main_section.find_all("table")

        for idx, table in enumerate(tables):
            headers = [th.get_text(strip=True) for th in table.find_all("th")]
            rows = []

            for tr in table.find_all("tr")[1:]:
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    rows.append(cols)

            data[f"table_{idx+1}"] = {
                "headers": headers,
                "rows": rows
            }

        return data

    # -------------------------------
    # Recruiters
    # -------------------------------
    def scrape_recruiters(self):
        print("Scraping Recruiters...")
        html = self.fetch_html(self.base_url + self.urls["recruiters"])
        soup = BeautifulSoup(html, "html.parser")

        recruiters = []

        logo_divs = soup.find_all("img")

        for img in logo_divs:
            src = img.get("src")
            if src and "uploads" in src:
                full_url = self.base_url + src if not src.startswith("http") else src
                recruiters.append(full_url)

        return list(set(recruiters))



    # -------------------------------
    # Placement Contacts
    # -------------------------------
    def scrape_contacts(self):
        print("Scraping Placement Contacts...")
        html = self.fetch_html(self.base_url + self.urls["contacts"])
        soup = BeautifulSoup(html, "html.parser")

        main_section = self.get_main_section(soup)

        return self.clean_text(main_section)

    # -------------------------------
    # Scrape All
    # -------------------------------
    def scrape_all(self):
        return {
            "about": self.scrape_about(),
            "year_wise": self.scrape_year_wise(),
            "recruiters": self.scrape_recruiters(),
            "contacts": self.scrape_contacts()
        }

    # -------------------------------
    # Save to Separate File
    # -------------------------------
    def update_placements_file(self):

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        placements_path = os.path.join(base_path, "data", "structured", "placements.json")

        placements_data = self.scrape_all()

        with open(placements_path, "w", encoding="utf-8") as f:
            json.dump(placements_data, f, indent=2, ensure_ascii=False)

        print("Placements saved to placements.json successfully.")
