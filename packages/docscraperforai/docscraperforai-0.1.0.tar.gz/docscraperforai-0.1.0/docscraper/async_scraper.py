import asyncio
import aiohttp
from bs4 import BeautifulSoup

class AsyncPageScraper:
    def __init__(self, user_agent=None, delay=0.5, proxy=None):
        self.headers = {'User-Agent': user_agent or 'docscraper/async/0.1.0'}
        self.delay = delay
        self.proxy = proxy

    async def fetch(self, session, url):
        async with session.get(url, headers=self.headers, proxy=self.proxy) as response:
            response.raise_for_status()
            html = await response.text()
            return html

    async def scrape_page(self, session, url):
        html = await self.fetch(session, url)
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

    async def scrape_pages(self, urls):
        results = {}
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.scrape_page(session, url)) for url in urls]
            pages = await asyncio.gather(*tasks, return_exceptions=True)
            for url, content in zip(urls, pages):
                results[url] = content
                await asyncio.sleep(self.delay)
        return results
