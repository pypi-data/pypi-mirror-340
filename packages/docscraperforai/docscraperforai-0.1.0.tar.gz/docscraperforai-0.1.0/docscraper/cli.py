import argparse
import asyncio
import aiohttp
from .scraper import PageScraper, save_to_file
from .crawler import DomainCrawler
from .async_scraper import AsyncPageScraper

def main():
    parser = argparse.ArgumentParser(description='Documentation Scraper')
    parser.add_argument('url', help='The URL to scrape from')
    parser.add_argument('--domain', action='store_true', help='Enable domain-wide crawling')
    parser.add_argument('--async', dest='async_mode', action='store_true', help='Use asynchronous scraping for a single page')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawl depth for domain crawling')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (in seconds)')
    parser.add_argument('--output', '-o', default='output', help='Output directory or filename prefix')
    parser.add_argument('--format', '-f', choices=['txt', 'md', 'json'], default='txt', help='Output file format')
    parser.add_argument('--proxy', type=str, help='Proxy URL (e.g., http://proxy.example.com:8080)')
    args = parser.parse_args()

    if args.domain:
        crawler = DomainCrawler(args.url, max_depth=args.depth, delay=args.delay, proxy=args.proxy)
        crawler.run(output_dir=args.output, fmt=args.format)
    else:
        if args.async_mode:
            async def run_async():
                scraper = AsyncPageScraper(delay=args.delay, proxy=args.proxy)
                async with aiohttp.ClientSession() as session:
                    data = await scraper.scrape_page(session, args.url)
                    save_to_file(data, f"{args.output}.{args.format}", fmt=args.format)
                    print(f"Saved content from {args.url} to {args.output}.{args.format}")
            asyncio.run(run_async())
        else:
            scraper = PageScraper(proxy=args.proxy)
            data = scraper.scrape_page(args.url)
            save_to_file(data, f"{args.output}.{args.format}", fmt=args.format)
            print(f"Saved content from {args.url} to {args.output}.{args.format}")

if __name__ == '__main__':
    main()
