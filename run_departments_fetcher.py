from fetchers.departments_fetcher import DepartmentsFetcher

BASE_URL = "https://www.sphoorthyengg.ac.in"

fetcher = DepartmentsFetcher(BASE_URL)

data = fetcher.scrape_departments()
fetcher.update_knowledge_base(data)

