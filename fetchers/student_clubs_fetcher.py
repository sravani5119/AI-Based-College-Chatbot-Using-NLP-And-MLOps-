import requests
from bs4 import BeautifulSoup
import json
import os


class StudentClubsFetcher:

    def __init__(self):
        self.base_url = "https://www.sphoorthyengg.ac.in"

        self.club_urls = {
            "coders_club": "/student-club/coders-club--code-architects",
            "creators_club": "/student-club/creators-club",
            "cultural_club": "/student-club/cultural-club-prathiba-yogyata",
            "eco_club": "/student-club/eco-club",
            "fitness_club": "/student-club/fitness-club-yogyata-",
            "gamers_club": "/student-club/gamers-club",
            "handlers_club": "/student-club/handlers-club-robo-tech",
            "literary_club": "/student-club/literary-and-fine-arts-club--literati--euphoria",
            "multimedia_club": "/student-club/multimedia-club--trinetra",
            "nss_club": "/student-club/nss-club-devna",
            "radio_club": "/student-club/sphn-radio-club",
            "sports_club": "/student-club/sports-club-sankalp",
            "womens_club": "/student-club/womens-chapter-club--sheinspires"
        }

    # ---------------------------
    # Fetch HTML
    # ---------------------------
    def fetch_html(self, url):
        response = requests.get(url)
        return response.text

    # ---------------------------
    # Clean text (removes header/footer junk)
    # ---------------------------
    def clean_text(self, soup):
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        main_content = soup.find("section", id="main-content")

        if not main_content:
            main_content = soup

        text = main_content.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)

        return cleaned

    # ---------------------------
    # Scrape all clubs
    # ---------------------------
    def scrape_all_clubs(self):

        clubs_data = {}
        clubs_list = []

        for club_key, path in self.club_urls.items():
            print(f"Scraping {club_key}...")

            html = self.fetch_html(self.base_url + path)
            soup = BeautifulSoup(html, "html.parser")

            cleaned_text = self.clean_text(soup)

            # Extract club name from first heading
            title = soup.find("h1")
            if title:
                clubs_list.append(title.get_text(strip=True))

            clubs_data[club_key] = cleaned_text

        return {
            "clubs_list": clubs_list,
            "clubs_data": clubs_data
        }

    # ---------------------------
    # Save JSON
    # ---------------------------
    def update_student_clubs_file(self):

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_path, "data", "structured", "student_clubs.json")

        clubs = self.scrape_all_clubs()

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(clubs, f, indent=2, ensure_ascii=False)

        print("Student Clubs saved successfully.")
