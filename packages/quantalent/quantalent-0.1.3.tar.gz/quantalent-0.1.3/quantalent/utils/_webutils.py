import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # If the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all paragraph texts or other relevant content
        paragraphs = soup.find_all(['p','div'])
        content = ' '.join([para.get_text() for para in paragraphs])

        return content
    else:
        print(f"Failed to retrieve the URL. Status code: {response.status_code}")
        return None

class WebUtils:
    def __init__(self):
        pass

    def scrape_url(self, url) -> str:
        response = requests.get(url)

        # If the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the page content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all paragraph texts or other relevant content
            paragraphs = soup.find_all(['p', 'div'])
            content = ' '.join([para.get_text() for para in paragraphs])

            return content
        else:
            print(f"Failed to retrieve the URL. Status code: {response.status_code}")
            return None


if __name__ == "__main__":
    url = "https://beautifulsouponline.com"
    scraped_content = scrape_url(url)
    if scraped_content:
        print(scraped_content)