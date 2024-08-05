"""
This script is used to scrape and save HTML content from multiple pages of the Hacker News website.

Functions:
- fetch_page(url): Fetches the HTML content of a given URL using the requests library.
- save_html(content, directory, filename): Saves the HTML content to a file in the specified directory.

Usage:
1. Set the base_url variable to the desired URL of the Hacker News website.
2. Modify the urls list to include the specific pages you want to scrape.
3. Run the script to fetch and save the HTML content of each page.

Note: The saved HTML files will be stored in a 'data' directory relative to the script file.
"""

import requests
import concurrent.futures

from datetime import datetime
from pathlib import Path

def fetch_page(url):
    """Fetches the HTML content of a given URL using the requests library."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error accessing page {url}: {e}")
        return None

def save_html(content, directory, filename):
    """Saves the HTML content to a file in the specified directory."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        file_path = directory / filename
        file_path.write_text(content, encoding='utf-8')
        print(f"HTML content downloaded and saved to '{file_path}'.")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")

def main():
    base_url = 'https://news.ycombinator.com/news'
    urls = [base_url, f"{base_url}?p=2", f"{base_url}?p=3"]
    
    now = datetime.now()
    date_today = now.strftime("%Y%m%d")
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    data_dir = Path(__file__).resolve().parent.parent / 'data'
    
    # Save date_today to a temporary file
    temp_file = Path(__file__).resolve().parent / 'date_today.txt'
    with temp_file.open('w') as f:
        f.write(date_today)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_page, url): url for url in urls}
        for i, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            url = futures[future]
            html_content = future.result()
            if html_content:
                file_name = f'hacker_news_page_{i}_{timestamp}.html'
                save_html(html_content, data_dir, file_name)

if __name__ == "__main__":
    main()
