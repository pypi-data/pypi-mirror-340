from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from novikovtv_parser_vk.parser.selenium_vk_parser.SeleniumVkParser import SeleniumVkParser


async def make_csv_text(web_driver_path, chrome_path, phone_number, password, search_query, max_communities=500):
    chrome_options = Options()

    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')

    # нужно запустить хром командой linux "google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug"
    # chrome_options.debugger_address = "127.0.0.1:9222"

    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.binary_location = chrome_path
    service = Service(web_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        selenium_vk_parser = SeleniumVkParser(driver, 0.1, 30)
        await selenium_vk_parser.login_vk(phone_number, password)
        await selenium_vk_parser.search_communities(search_query)
        community_links = await selenium_vk_parser.get_community_links(max_communities)
        parsed_data = await selenium_vk_parser.parse(community_links)

        return SeleniumVkParser.get_csv_result_string(parsed_data)
    finally:
        driver.quit()