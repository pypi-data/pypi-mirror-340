import requests
from bs4 import BeautifulSoup

class PageScraper:
    def __init__(self, user_agent=None, proxy=None):
        self.headers = {'User-Agent': user_agent or 'docscraper/0.1.0'}
        self.proxies = {'http': proxy, 'https': proxy} if proxy else None

    def scrape_page(self, url):
        response = requests.get(url, headers=self.headers, proxies=self.proxies)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        result = {}
        result['title'] = soup.title.string if soup.title else ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        result['description'] = meta_desc['content'] if meta_desc and meta_desc.get('content') else ''
        body = soup.find('body')
        result['text'] = body.get_text(separator='\n', strip=True) if body else ''
        code_blocks = soup.find_all(['pre', 'code'])
        result['code_blocks'] = [block.get_text(strip=True) for block in code_blocks]
        result['html'] = html
        return result

def save_to_file(data, filename, fmt='txt'):
    if fmt == 'json':
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    elif fmt == 'md':
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {data.get('title', '')}\n\n")
            f.write(f"**Description:** {data.get('description', '')}\n\n")
            f.write(data.get('text', ''))
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data.get('text', ''))
