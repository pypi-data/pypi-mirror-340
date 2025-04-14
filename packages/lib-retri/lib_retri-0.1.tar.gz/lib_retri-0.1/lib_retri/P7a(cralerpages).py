#Crawling Web PAges

import requests
from bs4 import BeautifulSoup

class WebCrawler:
    def __init__(self):
        self.visited_urls = set()

    def crawl(self, url, depth=3):
        if depth == 0 or url in self.visited_urls:
            return

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.index_page(url, soup)
                self.visited_urls.add(url)

                for link in soup.find_all('a', href=True):
                    new_url = link.get('href')
                    if new_url.startswith('http'):  # Ensure it's a valid URL
                        print(f"Crawling: {new_url}")
                        self.crawl(new_url, depth - 1)
        
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def index_page(self, url, soup):
        """Extracts and indexes the page title and first paragraph."""
        title = soup.title.string if soup.title else "No title"
        paragraph = soup.find('p').get_text() if soup.find('p') else "No paragraph found"

        print(f"\nIndexing: {url}")
        print(f"Title: {title}")
        print(f"First Paragraph: {paragraph}\n")
if __name__ == "__main__":
    start_url = "https://example.com"  
    crawler = WebCrawler()
    crawler.crawl(start_url, depth=2)
