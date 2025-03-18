import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Setup Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Set to False if debugging
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Automatically manage Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# eBay search results URL
url = "https://www.ebay.com/sch/i.html?_nkw=chinese+antique+bronze+ware&_ipg=240&_pgn=9"
driver.get(url)

# Scroll down to load dynamic content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # Wait for JavaScript to load content

# Save the full HTML page
html_filename = "ebay_page.html"
with open(html_filename, "w", encoding="utf-8") as file:
    file.write(driver.page_source)

print(f"Saved HTML file: {html_filename}")

# Close the Selenium driver (no longer needed)
driver.quit()

# Load the saved HTML file and parse with BeautifulSoup
with open(html_filename, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Create a folder for images
image_folder = "Ebay_Images"
os.makedirs(image_folder, exist_ok=True)

# Find all product images
images = soup.find_all("img", class_="s-card__image--final")

# User-Agent headers to avoid request blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}

# Download images
for index, img in enumerate(images):
    img_url = img.get("src")
    if img_url:
        try:
            response = requests.get(img_url, headers=headers, stream=True)
            image_filename = os.path.join(image_folder, f"product_{index + 1}.jpg")
            
            with open(image_filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
                    
            print(f"Downloaded: {image_filename}")

        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

print("Image scraping complete.")

