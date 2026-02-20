import requests
from bs4 import BeautifulSoup
import json
import os


class DepartmentsFetcher:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def fetch_page(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}")
        return response.text

    def extract_content(self, html):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        main_content = soup.find("section", id="main-content")

        if not main_content:
            return ""

        content = []

        unwanted_keywords = [
            "Quick Links",
            "Contact Information",
            "Newsletter",
            "Location",
            "Visitors Count",
            "©",
            "Designed and Developed",
            "Sphoorthy",
            "College remains open"
        ]

        # Headings
        for tag in main_content.find_all(["h2", "h3", "h4"]):
            text = tag.get_text(strip=True)
            if text and not any(word in text for word in unwanted_keywords):
                content.append(text)

        # Paragraphs
        for p in main_content.find_all("p"):
            text = p.get_text(strip=True)
            if len(text) > 40 and not any(word in text for word in unwanted_keywords):
                content.append(text)

        # List items
        for li in main_content.find_all("li"):
            text = li.get_text(strip=True)
            if len(text) > 30 and not any(word in text for word in unwanted_keywords):
                content.append(text)

        # 🔥 TABLE EXTRACTION (NEW PART)
        for row in main_content.find_all("tr"):
            cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            row_text = " | ".join(cells)

            if len(row_text) > 20 and not any(word in row_text for word in unwanted_keywords):
                content.append(row_text)

        # Remove duplicates
        seen = set()
        clean = []
        for item in content:
            if item not in seen:
                clean.append(item)
                seen.add(item)

        return "\n".join(clean)





    # LEVEL 1 — Extract department links
    def extract_department_links(self, html):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        links = {}

        for a in soup.find_all("a", href=True):
            href = a["href"]

            # Correct pattern
            if "/department/" in href or "/school-of-computing" in href:

                if not href.startswith("http"):
                    href = self.base_url + href

                # Use last part of URL as key
                key = href.rstrip("/").split("/")[-1]
                links[key] = href

        print("Found department links:", links)

        return links


    # LEVEL 2 — Extract sub-section links inside department

    def extract_sub_links(self, html, dept_slug):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        links = {}

        for a in soup.find_all("a", href=True):
            href = a["href"]

            if not href.startswith("http"):
                href = self.base_url + href

            # If department slug appears at end of URL
            if href.endswith(dept_slug) and "/department/" not in href:

                section = href.rstrip("/").split("/")[-2]
                links[section] = href

        return links



    def scrape_departments(self):

        departments = {
            "computer_science_and_engineering":
                "computer-science-and-engineering",

            "cse_ai_ml":
                "cse---artificial-intelligence-and-machine-learning",

            "cse_cyber_security":
                "cse---cyber-security",

            "cse_data_science":
                "cse---data-science",

            "freshman_engineering":
                "freshman-engineering",

            "school_of_computing":
                "school-of-computing"
        }

        sections = [
            "hod-message",
            "vision-mission",
            "teaching-staff",
            "achivements",
            "research-and-consultancy"
        ]

        departments_data = {}

        for dept_name, slug in departments.items():

            print(f"Scraping department: {dept_name}")

            departments_data[dept_name] = {}

            # MAIN ABOUT PAGE
            main_url = f"https://www.sphoorthyengg.ac.in/department/{slug}"
            main_html = self.fetch_page(main_url)
            departments_data[dept_name]["about"] = self.extract_content(main_html)

            # SUB SECTIONS
            for section in sections:
                url = f"https://www.sphoorthyengg.ac.in/{section}/{slug}"

                print(f"   -> Scraping {section}")

                try:
                    html = self.fetch_page(url)
                    content = self.extract_content(html)
                    departments_data[dept_name][section] = content
                except:
                    continue

        return departments_data


    def update_knowledge_base(self, departments_data):

        base_path = os.path.dirname(os.path.dirname(__file__))
        kb_path = os.path.join(base_path, "data", "structured", "knowledge_base.json")

        # Load existing data safely
        try:
            with open(kb_path, "r", encoding="utf-8") as f:
                kb = json.load(f)
        except:
            kb = {}

        # Update only departments section
        kb["departments"] = departments_data

        # Write back full structure
        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)

        print("Departments updated successfully.")
