# Import math Library
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Return the base-10 logarithm of different numbers
print(math.log10(2.7183))
print(math.log10(2))
print(math.log10(1))
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

driver.get("https://trends.google.com")

print("Done")

driver.quit()
