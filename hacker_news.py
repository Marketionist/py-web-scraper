#!/usr/bin/python

# python hacker_news.py 2 700

# python -m venv py-web-scraper/
# source py-web-scraper/bin/activate

# pip install -r requirements.txt

# pip install beautifulsoup4 requests && pip freeze > requirements.txt
# OR
# pip install beautifulsoup4 aiohttp[speedups] && pip freeze > requirements.txt
# (https://docs.aiohttp.org/en/stable/client_quickstart.html)
# OR
# pip install scrapy && pip freeze > requirements.txt
# (https://scrapy.org/)

import sys
import requests
from bs4 import BeautifulSoup
import pprint

def scrape_hacker_news (number_of_pages: int):
    """
    Scrape Hacker News website with BeautifulSoup and return an array of
    objects with 'title', 'link' and 'votes' sorted by votes
    """
    all_responses = ''
    response_page_1 = requests.get('https://news.ycombinator.com/news')
    all_responses += response_page_1.text
    

    if number_of_pages > 1:
        for page_number in range(2, number_of_pages + 1):
            response_page = requests.get(f'https://news.ycombinator.com/news?p={page_number}')
            all_responses += response_page.text

    soup = BeautifulSoup(all_responses, 'html.parser')

    links = soup.select('.storylink')
    subtext = soup.select('.subtext')

    return { 'links': links, 'subtext': subtext }

def sort_stories_by_votes (hkr_news_array: list) -> list:
    return sorted(hkr_news_array, key=lambda keyy: keyy['votes'], reverse=True)

def create_custom_hacker_news (
    number_of_pages: int=1,
    treshold: int=400
) -> list:
    hacker_news_array = []
    links_and_subtext = scrape_hacker_news(
        number_of_pages=number_of_pages
    )
    for index, item in enumerate(links_and_subtext['links']):
        title = item.getText()
        href = item.get('href', None)
        vote = links_and_subtext['subtext'][index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))

            if points > treshold:
                hacker_news_array.append({
                    'title': title,
                    'link': href,
                    'votes': points
                })
    return sort_stories_by_votes(hacker_news_array)

pprint.pprint(create_custom_hacker_news(
    number_of_pages=int(sys.argv[1]),
    treshold=int(sys.argv[2])
))
