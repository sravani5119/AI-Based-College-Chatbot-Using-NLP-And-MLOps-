import requests
from bs4 import BeautifulSoup
import json
import os

from sympy import content


class AdmissionsFetcher:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

        self.pages = {
            "procedure": "/admission-procedure",
            "epayments": "/e-payments",
            "courses_offered": "/courses-list",
            "eligibility": "/eligibility-conditions"
        }

    # -----------------------------------
    # Fetch page HTML
    # -----------------------------------
    def fetch_page(self, url):
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}")

        return response.text

    # -----------------------------------
    # Extract main paragraph content
    # -----------------------------------
    def extract_content(self, html, page_key):

        soup = BeautifulSoup(html, "html.parser")

        # Try to locate real content container
        main_section = soup.find("section", id="main-content")

        if not main_section:
            main_section = soup.find("section")

        if not main_section:
            main_section = soup.body


        # SPECIAL: COURSES PAGE

        if page_key == "courses_offered":

            courses_data = {
                "B.Tech": [],
                "M.Tech": []
            }

            content_area = soup.find("div", class_="about-page3-inner")

            if not content_area:
                return courses_data

            current_degree = None

            for tag in content_area.find_all(["h2", "h3", "h4", "a", "li"]):

                text = tag.get_text(strip=True)

                if not text:
                    continue

                # Detect Degree Heading
                if "B.Tech" in text:
                    current_degree = "B.Tech"
                    continue

                if "M.Tech" in text:
                    current_degree = "M.Tech"
                    continue

                # Capture course names
                if current_degree and len(text) > 3:
                    if text not in courses_data[current_degree]:
                        courses_data[current_degree].append(text)

            return courses_data

        # NORMAL EXTRACTION

        content = []

        for tag in main_section.find_all(["h2", "h3", "h4", "p", "li"]):
            text = tag.get_text(strip=True)

            if text and len(text) > 20:
                content.append(text)

        # Remove unwanted words
        unwanted = [
            "Quick Links",
            "Contact Information",
            "Newsletter",
            "Visitors Count"
        ]

        cleaned = []
        seen = set()

        for item in content:
            if any(word in item for word in unwanted):
                continue

            if item not in seen:
                cleaned.append(item)
                seen.add(item)

        return " ".join(cleaned)




    # -----------------------------------
    # Main scraping function
    # -----------------------------------
    def scrape_admissions(self):

        admission_data = {}

        for key, path in self.pages.items():
            url = self.base_url + path
            print(f"Scraping {key} from {url}")

            page_html = self.fetch_page(url)
            content = self.extract_content(page_html, key)


            admission_data[key] = content

        return admission_data

    # -----------------------------------
    # Update knowledge base
    # -----------------------------------
    def update_knowledge_base(self, admission_data):

        base_path = os.path.dirname(os.path.dirname(__file__))
        kb_path = os.path.join(base_path, "data", "structured", "knowledge_base.json")

        try:
            with open(kb_path, "r", encoding="utf-8") as f:
                kb = json.load(f)
        except:
            kb = {}

        kb["admissions"] = admission_data

        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)

        print("Admissions data updated successfully.")
