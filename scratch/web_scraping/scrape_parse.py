# scrape_parse.py
# Scrapes a RMP webpage and dumps the html into a file and the scraped data into a json

# Install prerequisites
# pip install requests beautifulsoup4

# Run in terminal 
# > python scrape_parse.py <URL> 

import sys
import requests
from bs4 import BeautifulSoup
import json

# Function to check if class name starts with a specific prefix
def class_starts_with(tag, class_prefix):
    return any(c.startswith(class_prefix) for c in tag.get('class', []))

# Main function to scrape the webpage
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

        # Array to store scraped data
        scraped_data = []

        # Find the unordered list whose class starts with "RatingsList__RatingsUL"
        ratings_list = soup.find('ul', class_=lambda value: value and value.startswith('RatingsList__RatingsUL'))

        # Check if the list exists
        if ratings_list:
            # Loop through all the list items (li) in the unordered list
            for li in ratings_list.find_all('li'):
                # Skip the list item if it contains an ad
                first_div = li.find('div')
                if first_div and class_starts_with(first_div, 'AdController__StyledPlaceholder'):
                    continue  # Ignore this list item as it's an ad

                # Extract course, timestamp, quality, difficulty, and comments
                course = li.find('div', class_=lambda value: value and value.startswith('RatingHeader__StyledClass')).get_text(strip=True)
                timestamp = li.find('div', class_=lambda value: value and value.startswith('TimeStamp__StyledTimeStamp')).get_text(strip=True)
                quality = li.find('div', class_=lambda value: value and value.startswith('CardNumRating__CardNumRatingNumber')).get_text(strip=True)
                difficulty = li.find_all('div', class_=lambda value: value and value.startswith('CardNumRating__CardNumRatingNumber'))[1].get_text(strip=True)
                comments = li.find('div', class_=lambda value: value and value.startswith('Comments__StyledComments')).get_text(strip=True)

                # Create a dictionary for this list item
                item_data = {
                    'course': course,
                    'timestamp': timestamp,
                    'quality': quality,
                    'difficulty': difficulty,
                    'comments': comments
                }

                # Add the dictionary to the scraped_data array
                scraped_data.append(item_data)

                # Print the data
                print(f'course: {course}')
                print(f'timestamp: {timestamp}')
                print(f'quality: {quality}')
                print(f'difficulty: {difficulty}')
                print(f'comments: {comments}')
                print('------------------------------------')

            # Save scraped data to a JSON file
            filename = f"prof{prof_id}scrape.json"
            with open(filename, 'w') as json_file:
                json.dump(scraped_data, json_file, indent=4)
            print(f"Scraped data saved as {filename}")

        else:
            print('No ratings list found on the page')

    except Exception as e:
        print(f"Error fetching the page: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_dump.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    scrape_and_save(url)
