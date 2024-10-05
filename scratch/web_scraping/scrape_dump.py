# scrape_dump.py
# Scrapes a RMP webpage and dumps the html in a file

# Install prerequisites
# pip install requests beautifulsoup4

# Run in terminal 
# > python scrape_dump.py <URL> 

import sys
import requests
from bs4 import BeautifulSoup

def scrape_and_save(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the professor ID from the URL (for file naming)
        prof_id = url.split('/')[-1]

        # Save the HTML content to a file
        filename = f"prof{prof_id}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))

        print(f"Page saved as {filename}")

    except Exception as e:
        print(f"Error fetching the page: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_dump.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    scrape_and_save(url)
