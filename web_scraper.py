#!/usr/bin/python

import asyncio
import pprint
import csv
from playwright.async_api import async_playwright

def parse_int (string: str) -> int:
    return ''.join((filter(lambda x: x.isdigit(), string)))

def sort_list_by (sorting_key: str, array_to_sort: list) -> list:
    return sorted(array_to_sort, key=lambda keyy: keyy[sorting_key], reverse=True)

with open('data-to-scrape.csv', mode = 'r', newline='') as file:
    reader = csv.reader(file)
    data = list(reader)
    lines_number = len(data)

async def scrape_website (
    url: str,
    first_param_selector: str,
    second_param_selector: str,
    third_param_selector: str
) -> list:
    async with async_playwright() as p:
        iphone_11 = p.devices['iPhone 11 Pro']
        browser = await p.chromium.launch(headless=True, slow_mo=0)
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

            resulting_list.append({
                'url': url,
                'first_param_text': resulting_texts[0].replace('\n', ''),
                'second_param_text': resulting_texts[1].replace('\n', ''),
                'third_param_text': resulting_texts[2].replace('\n', '')
            })        

        await context.close()
        await browser.close()

        return sort_list_by('first_param_text', resulting_list)

async def main ():
    scraped_output = await asyncio.gather(*[scrape_website(
        data[line][0],
        data[line][1],
        data[line][2],
        data[line][3]
    ) for line in range(lines_number)])

    pprint.pprint(scraped_output)

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
