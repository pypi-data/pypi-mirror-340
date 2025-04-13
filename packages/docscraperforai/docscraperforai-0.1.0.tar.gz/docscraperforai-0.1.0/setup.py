from setuptools import setup, find_packages

setup(
    name='docscraperforai',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'aiohttp',
    ],
    author='kash.me',
    author_email='diinoprakash@gmail.com',
    description='A powerful library to scrape documentation pages (or entire domains) into text, Markdown, or JSON files.',
    url='https://github.com/Prakashmaheshwaran/docscraperforai',
)
