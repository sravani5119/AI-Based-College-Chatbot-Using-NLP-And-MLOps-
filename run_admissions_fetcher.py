from fetchers.admissions_fetcher import AdmissionsFetcher
import json

BASE_URL = "https://www.sphoorthyengg.ac.in"

fetcher = AdmissionsFetcher(BASE_URL)

# Scrape data
admission_data = fetcher.scrape_admissions()

print("\nExtracted Admissions Data:")

for key, value in admission_data.items():
    print(f"\n--- {key.upper()} ---")

    # If value is dictionary (like courses_offered)
    if isinstance(value, dict):
        print(json.dumps(value, indent=2, ensure_ascii=False))
    else:
        print(value[:300], "...")  # print first 300 characters only

# Update knowledge base
fetcher.update_knowledge_base(admission_data)
