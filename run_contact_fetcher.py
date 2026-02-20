from fetchers.contact_fetcher import ContactFetcher

URL = "https://www.sphoorthyengg.ac.in/contact-us"

fetcher = ContactFetcher(URL)

html = fetcher.fetch()
contact_data = fetcher.parse(html)

print("Extracted Data:", contact_data)

fetcher.update_knowledge_base(contact_data)
