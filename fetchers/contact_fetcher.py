import requests
from bs4 import BeautifulSoup
import json
import os
import re


class ContactFetcher:

    def __init__(self, url):
        self.url = url

    def fetch(self):
        response = requests.get(self.url)

        if response.status_code != 200:
            raise Exception("Failed to fetch webpage")

        return response.text

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n")

        # Extract Emails
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_pattern, text)

        # Remove duplicates
        emails = list(set(emails))

        # Extract Indian Phone Numbers
        phone_pattern = r"\+91[\s\d]+"
        phones = re.findall(phone_pattern, text)

        # Clean phone numbers
        cleaned_phones = []
        for phone in phones:
            phone = phone.strip()
            phone = re.sub(r"\s+", " ", phone)  # normalize spaces
            cleaned_phones.append(phone)

        # Remove duplicates
        cleaned_phones = list(set(cleaned_phones))

        # Extract Address Block
        address_pattern = r"Sphoorthy Engineering College.*?India"
        address_match = re.search(address_pattern, text, re.DOTALL)

        address = None
        if address_match:
            address = address_match.group(0)
            address = re.sub(r"\s+", " ", address).strip()

        return {
            "phone": cleaned_phones,
            "email": emails,
            "address": address
        }


    def update_knowledge_base(self, contact_data):

        base_path = os.path.dirname(os.path.dirname(__file__))
        kb_path = os.path.join(base_path, "data", "structured", "knowledge_base.json")

        try:
            with open(kb_path, "r", encoding="utf-8") as f:
                kb = json.load(f)
        except:
            kb = {}

        kb["contact"] = contact_data

        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)

        print("Knowledge base updated successfully.")
