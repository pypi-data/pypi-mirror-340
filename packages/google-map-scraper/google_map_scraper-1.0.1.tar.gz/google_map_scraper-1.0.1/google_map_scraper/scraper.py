import json
import csv
import re
import time
from typing import List, Dict, Tuple

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class GoogleMapsScraper:
    def __init__(self, headless: bool = True):
        """
        Initialize the Google Maps Scraper with Selenium WebDriver options.

        :param headless: If True, runs the browser in headless mode (no GUI).
        """
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def scrape(self, keyword: str) -> List[Dict]:
        """
        Perform Google Maps scraping for a given search keyword.

        :param keyword: Business or search query (e.g., 'CA in Hyderabad India')
        :return: List of dictionaries containing business details
        """
        results = []

        try:
            self.driver.get(f'https://www.google.com/maps/search/{keyword}/')

            # Try to accept cookies or click form if appears
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))
                ).click()
            except Exception:
                pass

            # Scroll through results feed
            scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
            self.driver.execute_script(self._scroll_script(), scrollable_div)

            # Parse all found items
            items = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction]')

            for item in items:
                data = self._extract_data(item)
                if data.get('title'):
                    results.append(data)

            # Save to JSON and CSV
            self._save_to_json(results, 'results.json')
            self._save_to_csv(results, 'results.csv')

            return results

        finally:
            time.sleep(3)
            self.driver.quit()

    def _scroll_script(self) -> str:
        """
        JavaScript for scrolling within the feed to load more business listings.
        """
        return """
        var scrollableDiv = arguments[0];
        function scrollWithinElement(scrollableDiv) {
            return new Promise((resolve, reject) => {
                var totalHeight = 0;
                var distance = 1000;
                var scrollDelay = 3000;

                var timer = setInterval(() => {
                    var scrollHeightBefore = scrollableDiv.scrollHeight;
                    scrollableDiv.scrollBy(0, distance);
                    totalHeight += distance;

                    if (totalHeight >= scrollHeightBefore) {
                        totalHeight = 0;
                        setTimeout(() => {
                            var scrollHeightAfter = scrollableDiv.scrollHeight;
                            if (scrollHeightAfter > scrollHeightBefore) {
                                return;
                            } else {
                                clearInterval(timer);
                                resolve();
                            }
                        }, scrollDelay);
                    }
                }, 200);
            });
        }
        return scrollWithinElement(scrollableDiv);
        """

    def _extract_data(self, item) -> Dict:
        """
        Extract business information from a single result item element.

        :param item: Selenium WebElement representing a business listing
        :return: Dictionary with extracted details
        """
        data = {}

        try:
            data['title'] = item.find_element(By.CSS_SELECTOR, ".fontHeadlineSmall").text
        except:
            pass

        try:
            data['link'] = item.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        except:
            pass

        try:
            data['website'] = item.find_element(By.CSS_SELECTOR, 'div[role="feed"] > div > div[jsaction] div > a').get_attribute('href')
        except:
            pass

        try:
            rating_text = item.find_element(By.CSS_SELECTOR, '.fontBodyMedium > span[role="img"]').get_attribute('aria-label')
            rating_numbers = [float(piece.replace(",", ".")) for piece in rating_text.split(" ") if piece.replace(",", ".").replace(".", "", 1).isdigit()]
            if rating_numbers:
                data['stars'] = rating_numbers[0]
                data['reviews'] = int(rating_numbers[1]) if len(rating_numbers) > 1 else 0
        except:
            pass

        try:
            text_content = item.text
            phone_pattern = r'((\+?\d{1,2}[ -]?)?(\(?\d{3}\)?[ -]?\d{3,4}[ -]?\d{4}|\(?\d{2,3}\)?[ -]?\d{2,3}[ -]?\d{2,3}[ -]?\d{2,3}))'
            matches = re.findall(phone_pattern, text_content)
            phone_numbers = [match[0] for match in matches]
            unique_phone_numbers = list(set(phone_numbers))
            data['phone'] = unique_phone_numbers[0] if unique_phone_numbers else None
        except:
            pass

        return data

    def _save_to_json(self, data: List[Dict], filename: str):
        """
        Save the extracted data to a JSON file.

        :param data: List of business dictionaries
        :param filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_to_csv(self, data: List[Dict], filename: str):
        """
        Save the extracted data to a CSV file.

        :param data: List of business dictionaries
        :param filename: Output CSV file
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "link", "website", "stars", "reviews", "phone"])
            writer.writeheader()
            for row in data:
                writer.writerow(row)