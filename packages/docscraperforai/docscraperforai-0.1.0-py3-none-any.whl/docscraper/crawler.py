import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from .scraper import PageScraper, save_to_file
from .utils import allowed_by_robots

class DomainCrawler:
    def __init__(self, base_url, max_depth=2, delay=1, user_agent=None, proxy=None):
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited = set()
        self.user_agent = user_agent or 'docscraper/0.1.0'
        self.proxy = proxy
        self.scraper = PageScraper(user_agent=self.user_agent, proxy=self.proxy)
        self.domain = urlparse(base_url).netloc

    def is_internal_link(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''

    def crawl(self, url=None, depth=0):
        if depth > self.max_depth:
            return []
        url = url or self.base_url
        if url in self.visited:
            return []
        if not allowed_by_robots(url, user_agent=self.user_agent):
            print(f"Skipping {url} as it is disallowed by robots.txt")
            return []
        try:
            print(f"Crawling: {url} at depth {depth}")
            self.visited.add(url)
            data = self.scraper.scrape_page(url)
            results = [(url, data)]
            soup = BeautifulSoup(data.get('html', ''), 'html.parser')
            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(url, link['href'])
                if self.is_internal_link(absolute_link) and absolute_link not in self.visited:
                    time.sleep(self.delay)
                    results.extend(self.crawl(absolute_link, depth+1))
            return results
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return []

    def run(self, output_dir='output', fmt='txt'):
        import os
        os.makedirs(output_dir, exist_ok=True)
        results = self.crawl()
        for i, (url, data) in enumerate(results):
            filename = os.path.join(output_dir, f"page_{i}.{fmt}")
            save_to_file(data, filename, fmt=fmt)
            print(f"Saved {url} to {filename}")
