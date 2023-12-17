import requests
from bs4 import BeautifulSoup
import re

def extract_text_from_webpage(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and clean all text from the parsed HTML
        all_text = soup.get_text(separator=' ')
        
        # Remove extra whitespaces and newlines
        cleaned_text = re.sub(r'\s+', ' ', all_text).strip()

        return cleaned_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def save_text_to_file(text, filename='script.txt'):
    try:
        # Save the cleaned and formatted text to a file
        with open(filename, 'w+', encoding='utf-8') as file:
            file.write(text)
        print(f"Cleaned and formatted text saved to {filename}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

if __name__=='__main__':
    # Example usage:
    webpage_url = 'https://en.wikipedia.org/wiki/Medium_(website)'
    text_content = extract_text_from_webpage(webpage_url)

    if text_content:
        save_text_to_file(text_content)

