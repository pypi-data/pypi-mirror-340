# DocScraper

**DocScraper** is a Python library that allows you to scrape documentation pages — either a single page or an entire domain — and export the content to various formats like plain text, Markdown, or JSON.

## Features

- Scrape single pages or crawl entire documentation sites
- Export to `.txt`, `.md`, or `.json`
- Supports proxies
- Async or sync scraping modes
- Respects `robots.txt`

## Installation

Once zipped and downloaded, you can install it locally:

```bash
pip install docscraper.zip
```

Or clone and install in editable mode:

```bash
pip install -e .
```

## Usage

```bash
python -m docscraper.cli https://example.com/docs --output output.md --format md
```

## License

MIT License
