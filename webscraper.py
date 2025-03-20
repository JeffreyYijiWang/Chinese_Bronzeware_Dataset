import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Automatically download and manage ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# eBay search URL (Modify query if needed)
url = "https://www.ebay.com/sch/i.html?_nkw=chinese+antique+bronze+ware&_ipg=240&_pgn=2"
driver.get(url)

# Allow dynamic content to load
time.sleep(5)  # Adjust as needed

# Get full page HTML after JavaScript has loaded content
page_source = driver.page_source

# Save the HTML to a file
html_file_path = "ebay_page_dynamic.html"
with open(html_file_path, "w", encoding="utf-8") as file:
    file.write(page_source)

# Close the browser
driver.quit()

print(f"HTML saved to {html_file_path}")

