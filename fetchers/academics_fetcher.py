import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os


BASE_URL = "https://www.sphoorthyengg.ac.in"

ACADEMIC_COUNCIL_URL = BASE_URL + "/academic-council"
ACADEMIC_CALENDAR_URL = BASE_URL + "/academic-calendars"


def fetch_academic_council():

    response = requests.get(ACADEMIC_COUNCIL_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    section = soup.find("section", {"id": "main-content"})

    if not section:
        return ""

    text = section.get_text(separator="\n").strip()

    return text


def fetch_academic_calendars():

    response = requests.get(ACADEMIC_CALENDAR_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    calendars = []

    table = soup.find("table")

    if not table:
        return calendars

    rows = table.find_all("tr")[1:]

    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 5:
            continue

        academic_year = cols[1].get_text(strip=True)
        date_of_issue = cols[2].get_text(strip=True)
        title = cols[3].get_text(strip=True)

        link_tag = cols[4].find("a")

        if not link_tag:
            continue

        link = urljoin(BASE_URL, link_tag.get("href"))

        calendars.append({
            "academic_year": academic_year,
            "date_of_issue": date_of_issue,
            "title": title,
            "link": link
        })

    return calendars


def save_academics_data():

    council_text = fetch_academic_council()
    calendars = fetch_academic_calendars()

    data = {
        "academic_council": council_text,
        "academic_calendars": calendars
    }

    os.makedirs("data/structured", exist_ok=True)

    with open("data/structured/academics.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("academics.json created successfully")