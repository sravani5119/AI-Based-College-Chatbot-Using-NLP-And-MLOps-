import requests
from bs4 import BeautifulSoup
import json
import os


class RNDFetcher:

    def __init__(self):
        self.base_url = "https://www.sphoorthyengg.ac.in"

        self.urls = {
            "rd_cell": "/research",
            "newgen_iedc": "/newgen-iedc",
            "centre_of_excellence": "/centre-for-excellence",
            "aicte_idea_lab": "/aicte-idea-lab"
        }

    # ----------------------------------
    # Fetch HTML
    # ----------------------------------
    def fetch_html(self, url):
        response = requests.get(url)
        return response.text

    # ----------------------------------
    # Clean and extract full content
    # ----------------------------------
    def extract_full_content(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted sections
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)

        return cleaned

    # ----------------------------------
    # Scrape All R&D Pages
    # ----------------------------------
    def scrape_all(self):

        rnd_data = {}

        for key, endpoint in self.urls.items():
            print(f"Scraping {key}...")
            html = self.fetch_html(self.base_url + endpoint)
            content = self.extract_full_content(html)
            rnd_data[key] = content

        return rnd_data

    # ----------------------------------
    # Save to Single JSON File
    # ----------------------------------
    def update_rnd_file(self):

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rnd_path = os.path.join(base_path, "data", "structured", "rnd.json")

        rnd_data = self.scrape_all()

        with open(rnd_path, "w", encoding="utf-8") as f:
            json.dump(rnd_data, f, indent=2, ensure_ascii=False)

        print("R&D data saved to rnd.json successfully.")
