import requests
from bs4 import BeautifulSoup

# learning how to build scrapping tool according to this article
# https://realpython.com/beautiful-soup-web-scraper-python/#scrape-the-fake-python-job-site

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
# print(results.prettify())

job_elements = results.find_all("div", class_="card-content")
python_jobs = results.find_all(
        "h2", string=lambda text: "python" in text.lower()
    )
for job_element in python_jobs:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")

    
    print(title_element.text.strip())
    print(python_jobs)
    print(len(python_jobs))
    print(company_element.text.strip())
    print(location_element.text.strip())
    print()