from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

# ChromeDriver path

chrome_driver_path ="/Users/christinewei/Downloads/chromedriver-mac-x64/chromedriver"

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def setup_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_press_releases(url):
    driver = setup_driver()
    try:
        driver.get(url)
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cassie-pre-banner--button.cassie-accept-all"))
            )
            cookie_button.click()
        except:
            print("Cookie banner not found or already accepted")

        wait = WebDriverWait(driver, 30)
        press_releases = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.article-headline-link")))
        
        results = []
        for release in press_releases:
            try:
                link = release.find_element(By.TAG_NAME, "a")
                title = link.get_attribute("aria-label")
                date = release.find_element(By.CSS_SELECTOR, "p.source-date").text.strip()
                
                tag_element = release.find_element(By.CSS_SELECTOR, "span.lds-badge.outlined")
                tag = tag_element.text if tag_element else "N/A"
                
                results.append({"title": title, "date": date, "tag": tag})
            except Exception as e:
                print(f"Error extracting press release: {e}")
        
        return results
    finally:
        driver.quit()

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

url = "https://www.lilly.com/news/press-releases"

try:
    press_releases = scrape_press_releases(url)
    for idx, release in enumerate(press_releases, 1):
        print(f"{idx}. Title: {release['title']}")
        print(f"   Date: {release['date']}")
        print(f"   Tag: {release['tag']}")
        print("---")
    
    # Save to Excel
    save_to_excel(press_releases, "lilly_press_releases.xlsx")
except Exception as e:
    print(f"An error occurred: {e}")
