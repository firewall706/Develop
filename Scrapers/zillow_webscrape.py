from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def zillow_scraper():
    # Set up the ChromeDriver and options
    options = Options()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    base_url = "https://www.zillow.com/"
    search_location = "Luzerne County, PA"

    # Navigate to Zillow
    driver.get(base_url)
    time.sleep(3)

    # Input search location
    search_box = driver.find_element_by_id("search-box-input")
    search_box.send_keys(search_location)
    search_box.submit()
    time.sleep(3)

    # Set minimum bedrooms to 3
    bedroom_filter = driver.find_element_by_css_selector('button[data-value="3,"]')
    bedroom_filter.click()
    time.sleep(3)

    # Initialize list to store all the data
    property_data = []

    # Set a limit on max pages to scrape, or until no more pages
    max_pages = 20
    for i in range(max_pages):
        print(f"Scraping page {i + 1}...")

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        properties = soup.find_all("div", class_="list-card-info")

        for property in properties:
            details = {}
            details["link"] = property.find("a")["href"]
            details["price"] = property.find("div", class_="list-card-price").text
            details["address"] = property.find("address").text

            # You can expand this to include other details like bedroom count, bathroom count, etc.
            property_data.append(details)

        # Navigate to the next page
        try:
            next_button = driver.find_element_by_css_selector('a[title="Next page"]')
            next_button.click()
            time.sleep(3)
        except:
            print("No more pages to scrape!")
            break

    driver.quit()
    return property_data

if __name__ == "__main__":
    data = zillow_scraper()
    for item in data:
        print(item)

