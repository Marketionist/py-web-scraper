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
https://www.bbc.com/news/technology,[class*="gel-3/5@xxl"] .qa-status-date-output,[class*="gel-3/5@xxl"] .gs-c-promo-heading__title,[class*="gel-3/5@xxl"] .gs-c-section-link
https://news.ycombinator.com/,.rank,.storylink,.age
```
Or if you just want to get the first 3 article titles:
```
https://www.cnn.com/business/tech,(//*[ancestor::*[ul[descendant::*[contains(@data-analytics, "Top stories _list-xs_")]]] and contains(@class, "cd__headline-text")])[1],(//*[ancestor::*[ul[descendant::*[contains(@data-analytics, "Top stories _list-xs_")]]] and contains(@class, "cd__headline-text")])[2],(//*[ancestor::*[ul[descendant::*[contains(@data-analytics, "Top stories _list-xs_")]]] and contains(@class, "cd__headline-text")])[3]
```
6. Create a `data-processed.csv` file with any data that you do not want to be
displayed in the scraper output (if it's several items you can put one
item/string per line)

## Running
To run the script just execute:
```bash
python web_scraper.py
```

## Bonus
Alternatively instead of creating `data-to-scrape.csv` you can set a path to
the file with links and selectors by specifying the `INCOMING_DATA_SOURCE`
environment variabale like this:
```bash
INCOMING_DATA_SOURCE=my-file-with-data-to-scrape.csv python web_scraper.py
```
In addition to that, if you want to see the browser while the script is running,
you can enable it by setting the `HEADED` environment variabale to `True` like
this:
```bash
INCOMING_DATA_SOURCE=my-file-with-data-to-scrape.csv HEADED=True python web_scraper.py
```

## Optional
In case if you would like to install any additional dependencies (for example
scrapy) - run:
```bash
pip install scrapy && pip freeze > requirements.txt
```

## Thanks
If this script was helpful to you, please give it a **★ Star** on
[GitHub](https://github.com/Marketionist/py-web-scraper)
