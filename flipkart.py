from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up the driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.flipkart.com/search?q=iphone"

driver.get(url)

# Wait for the page to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_4rR01T")))
except:
    pass

# Find product names and prices
try:
    names = driver.find_elements(By.CLASS_NAME, "_4rR01T")
    prices = driver.find_elements(By.CLASS_NAME, "_30jeq3")
except:
    names = []
    prices = []

print(f"Found {len(names)} names")
print(f"Found {len(prices)} prices")

data = []

for i in range(min(20, len(names), len(prices))):
    data.append({
        "Product Name": names[i].text.strip(),
        "Price": prices[i].text.strip()
    })

driver.quit()

df = pd.DataFrame(data)
df.to_csv("iphone_flipkart.csv", index=False)

print("✅ Successfully scraped", len(data), "iPhone products")
print(df)
