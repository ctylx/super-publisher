from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options


def init_driver():
    # 设置 Selenium 无头模式
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # 配置 Selenium Wire 来捕获请求
    return webdriver.Chrome(
        options=chrome_options,
        seleniumwire_options={"verify_ssl": False},
    )
