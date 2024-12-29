from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Go to the Google home page
driver.get("https://www.google.com")

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers["Content-Type"],
        )
