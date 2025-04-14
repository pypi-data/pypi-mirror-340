import asyncio

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import io

class SeleniumVkParser:
    def __init__(self, driver, min_wait_time, max_wait_time):
        self.driver = driver
        self.minimal_wait_time = min_wait_time
        self.max_wait_time = max_wait_time

    async def __click_element_when_clickable(self, element: str):
        await asyncio.sleep(self.minimal_wait_time)
        WebDriverWait(self.driver, self.max_wait_time).until(EC.element_to_be_clickable((By.XPATH, element))).click()

    async def __click_element_when_clickable_by_class_name(self, class_name: str):
        await asyncio.sleep(self.minimal_wait_time)
        WebDriverWait(self.driver, self.max_wait_time).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name))).click()

    async def __get_element_when_located(self, element: str):
        await asyncio.sleep(self.minimal_wait_time)
        return WebDriverWait(self.driver, self.max_wait_time).until(EC.presence_of_element_located((By.XPATH, element)))

    async def __get_elements_when_located(self, element: str):
        await asyncio.sleep(self.minimal_wait_time)
        return self.driver.find_elements(By.XPATH, element)

    async def __get_element_when_located_by_class_name(self, class_name: str):
        await asyncio.sleep(self.minimal_wait_time)
        return WebDriverWait(self.driver, self.max_wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

    async def __wait_element_when_located(self, element: str):
        await asyncio.sleep(self.minimal_wait_time)
        WebDriverWait(self.driver, self.max_wait_time).until(EC.presence_of_element_located((By.XPATH, element)))

    async def __wait_element_when_located_by_classname(self, class_name: str):
        await asyncio.sleep(self.minimal_wait_time)
        WebDriverWait(self.driver, self.max_wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))

    async def __wait_for_new_elements_located(self, xpath: str, previous_count: int):
        await asyncio.sleep(self.minimal_wait_time)
        def more_elements_loaded(driver):
            elements = driver.find_elements(By.XPATH, xpath)
            return elements if len(elements) > previous_count else False

        return WebDriverWait(self.driver, self.max_wait_time).until(more_elements_loaded)

    async def login_vk(self, phone_number, password):
        self.driver.get("https://vk.com")

        time.sleep(5)
        print('Already on vk.com')
        await self.__click_element_when_clickable("//button[@data-testid='enter-another-way']")

        phone_input = await self.__get_element_when_located("//input[@inputmode='tel' and @name='login']")
        phone_input.send_keys(phone_number)

        await self.__click_element_when_clickable("//button[@data-test-id='submit_btn']")

        password_input = await self.__get_element_when_located("//input[@name='password' and @type='password']")

        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

    async def search_communities(self, query):
        print('Login successful')
        await self.__click_element_when_clickable("//a[@href='/groups']")
        print('Searching communities')
        search_box = await self.__get_element_when_located("//input[@data-testid='search_input']")
        search_box.send_keys(query)

    async def get_community_links(self, max_communities=500):
        links = []

        await self.__wait_element_when_located("//div[@data-testid='list_groups_items']")

        while True:
            communities = await self.__get_elements_when_located("//div[@data-testid='group_item_desktop_list']")
            communities_count = len(communities)
            print('Found ' + str(communities_count) + ' communities')

            if communities_count >= max_communities:
                break
            else:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                try:
                    await self.__wait_element_when_located_by_classname("vkuiSpinner__host")
                    print('Getting more communities')
                    await self.__wait_for_new_elements_located(
                        "//div[@data-testid='group_item_desktop_list']",
                        communities_count
                    )
                except:
                    communities = await self.__get_elements_when_located("//div[@data-testid='group_item_desktop_list']")
                    communities_count = len(communities)
                    break

        if communities_count >= max_communities:
            communities = communities[:max_communities]

        print('Final communities count is ' + str(len(communities)))

        for community in communities:
            try:
                link_element = community.find_element(By.TAG_NAME, "a")
                link = link_element.get_attribute("href")
                title = community.text.split("\n")[0]
                if link and title:
                    links.append((title, link))
            except:
                continue

        return links

    @classmethod
    def extract_plain_text_and_links(cls, element) -> str:
        if isinstance(element, str):
            return element.strip()

        if element.name in ['script', 'style']:
            return ''

        text_parts = []

        if 'href' in element.attrs:
            href = element.attrs['href']
            if href.startswith('/'):
                href = 'https://vk.com' + href
            text_parts.append(href.strip())

        text_parts.append(' '.join(cls.extract_plain_text_and_links(child) for child in element.contents))

        return ' '.join(filter(None, text_parts))

    @classmethod
    def find_data_in_html(cls, html: str, title: str):
        soup = BeautifulSoup(html, 'html.parser')

        description = ''
        phone = ''
        website = ''
        address = ''
        links = ''
        contacts = ''

        desc_element = soup.find("div", class_="group_info_row info", title="Description")
        if desc_element:
            text_element = desc_element.find("div", class_="line_value")
            if text_element:
                description = text_element.get_text(separator=" ", strip=True)

        phone_element = soup.find("div", class_="group_info_row phone", title="Phone")
        if phone_element:
            phone_link = phone_element.find("a", href=True)
            if phone_link:
                phone = phone_link.get_text(separator=" ", strip=True)

        website_element = soup.find("div", class_="group_info_row site", title="Website")
        if website_element:
            website_link = website_element.find("a", href=True)
            if website_link:
                website = website_link.get_text(separator=" ", strip=True)

        address_element = soup.find("div", class_="group_info_row address")
        if address_element:
            address_link = address_element.find("a", class_="address_link")
            if address_link:
                address = address_link.get_text(separator=" ", strip=True)

        links_section = soup.find("aside", {"aria-label": "Links"})
        if links_section:
            links = cls.extract_plain_text_and_links(links_section)

        contacts_section = soup.find("aside", {"aria-label": "Contacts"})
        if contacts_section:
            contacts = cls.extract_plain_text_and_links(contacts_section)

        return {
            'title': title,
            'description': description,
            'phone': phone,
            'website': website,
            'address': address,
            'links': links,
            'contacts': contacts
        }

    async def parse(self, community_links):
        parsed_data = []

        for title, link in community_links:
            self.driver.get(link)

            await self.__click_element_when_clickable_by_class_name("groups-redesigned-info-more")

            group_info_box = await self.__get_element_when_located_by_class_name("group-info-box")

            group_info_html = group_info_box.get_attribute("outerHTML")
            parsed_data.append(SeleniumVkParser.find_data_in_html(group_info_html, title))
            print(f"HTML сохранен для группы: {title}")
        return parsed_data

    @staticmethod
    def get_csv_result_string(data: list) -> str:
        output = io.StringIO()
        field_names = ['title', 'description', 'phone', 'website', 'address', 'links', 'contacts']

        string_writer = csv.DictWriter(output, fieldnames=field_names)
        string_writer.writeheader()

        for row in data:
            string_writer.writerow(row)

        csv_content = output.getvalue()
        output.close()
        return csv_content