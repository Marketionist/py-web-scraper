#!/usr/bin/python

import os
import asyncio
import pprint
import csv
from playwright.async_api import async_playwright

def parse_int (string: str) -> int:
    return ''.join((filter(lambda x: x.isdigit(), string)))

def sort_list_by (sorting_key: str, array_to_sort: list) -> list:
    return sorted(array_to_sort, key=lambda keyy: keyy[sorting_key], reverse=True)

incoming_data_source = os.getenv('INCOMING_DATA_SOURCE') or 'data-to-scrape.csv'
processed_data_source = 'data-processed.csv'

with open(incoming_data_source, mode = 'r', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)
    lines_number = len(data)

with open(processed_data_source, mode = 'r', newline='') as file:
    reader_processed = csv.reader(file)
    # Read data into the list and turn it to string for easy searching
    data_processed = str(list(reader_processed))

async def scrape_website (
    url: str,
    first_param_selector: str,
    second_param_selector: str,
    third_param_selector: str,
    processed_data: list
) -> list:
    async with async_playwright() as p:
        iphone_11 = p.devices['iPhone 11 Pro']
        browser = await p.chromium.launch(
            headless=not os.getenv('HEADED', False),
            slow_mo=0
        )
        context = await browser.new_context(
            **iphone_11,
            locale='de-DE',
            geolocation={ 'longitude': 12.492507, 'latitude': 41.889938 },
            permissions=['geolocation'],
            color_scheme='dark',
        )

        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector(first_param_selector)

        resulting_param_elements = await asyncio.gather(
            page.query_selector_all(first_param_selector),
            page.query_selector_all(second_param_selector),
            page.query_selector_all(third_param_selector)
        )

        resulting_list = []

        for index, value in enumerate(resulting_param_elements[0]):
            resulting_texts = await asyncio.gather(
                value.text_content(),
                resulting_param_elements[1][index].text_content(),
                resulting_param_elements[2][index].text_content()
            )

            # Remove empty spaces from the beginning and the end of the string
            first_param_text = resulting_texts[0].strip()

            print(f'{first_param_text} is already in "{processed_data_source}' +
                f'": {first_param_text in data_processed}')

            if first_param_text not in data_processed:
                resulting_list.append({
                    'url': url,
                    'first_param_text': parse_int(first_param_text),
                    'second_param_text': resulting_texts[1].strip(),
                    'third_param_text': resulting_texts[2].strip()
                })

        await context.close()
        await browser.close()

        return sort_list_by('first_param_text', resulting_list)

async def main ():
    scraped_output = await asyncio.gather(*[scrape_website(
        data[line][0],
        data[line][1],
        data[line][2],
        data[line][3],
        data_processed
    ) for line in range(lines_number)])

    # Remove empty lists
    pprint.pprint(list(filter(None, scraped_output)))

    # print('scraped_output: {}'.format(scraped_output))

    # # Fill an input
    # await page.fill('#search', 'query')

    # # Navigate implicitly by clicking a link
    # await page.click('#submit')

    # # Wait for #search to appear in the DOM.
    # await page.wait_for_selector('#search', state='attached')
    # # Wait for #promo to become visible, for example with `visibility:visible`.
    # await page.wait_for_selector('#promo')

    # # Evaluate JavaScript code on the browser side
    # status = await page.evaluate("""async () => {
    #     response = await fetch(location.href)
    #     return response.status
    # }""")

    # # Pass data as a parameter
    # data = { 'text': 'some data', 'value': 1 }
    # result = await page.evaluate("""data => {
    #     window.myApp.use(data)
    # }""", data)

    # print(await page.title())

    # Wait for 3 seconds
    # await page.wait_for_timeout(3000)


asyncio.run(main())
