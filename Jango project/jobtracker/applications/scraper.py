import requests
from bs4 import BeautifulSoup

def fetch_jobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for tag in soup.find_all('a'):
        text = tag.get_text(strip=True)
        if text:
            jobs.append(text)

    return jobs
