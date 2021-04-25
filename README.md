# py-web-scraper

A scraper to collect data from the websites

## Installation
1. Clone this repository:
```bash
git clone git@github.com:Marketionist/py-web-scraper.git
```
2. Create virtual environment and activate it:
```bash
python -m venv web-scraper/
source web-scraper/bin/activate
```
3. Install all dependencies:
```bash
pip install -r requirements.txt
```
4. Download Playwright browsers:
```bash
playwright install
```
5. Create a `data-to-scrape.csv` file with 2 rows and 4 cells in each row:
    1 - URL of the page that you want to scrape
    2 - selector (CSS or XPath) for the first parameter that you want to scrape
    3 - selector (CSS or XPath) for the second parameter that you want to scrape
    4 - selector (CSS or XPath) for the third parameter that you want to scrape
As it is a .csv file, each value (cell) is separated by comma. For example:
```
https://www.bbc.com/,.module--news .media-list__item:nth-child(1) .media__link,.module--news .media-list__item:nth-child(2) .media__link,.module--news .media-list__item:nth-child(3) .media__link
https://www.cnn.com/business/tech,(//*[ancestor::*[ul[descendant::*[contains(@data-analytics, "Top stories _list-xs_")]]] and contains(@class, "cd__headline-text")])[1],(//*[ancestor::*[ul[descendant::*[contains(@data-analytics, "Top stories _list-xs_")]]] and contains(@class, "cd__headline-text")])[2],(//*[ancestor::*[ul[descendant::*[contains(@data-analytics, "Top stories _list-xs_")]]] and contains(@class, "cd__headline-text")])[3]
```

## Running
To run the script just execute:
```bash
python web_scraper.py
```

## Bonus
In case if you would like to install any additional dependencies like scrapy - run:
```bash
pip install scrapy && pip freeze > requirements.txt
```

## Thanks
If this script was helpful to you, please give it a **★ Star** on
[GitHub](https://github.com/Marketionist/py-web-scraper).
