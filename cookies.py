from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time


def save_cookie(driver, url, name):
    driver.get(url)
    input("Press Enter to continue after logging in...")

    # save cookies
    time.sleep(5)
    cookie_file = f"./cookies/{name}_cookies.pkl"
    with open(cookie_file, "wb") as file:
        cookies = driver.get_cookies()
        pickle.dump(cookies, file)


def add_cookie(driver, url, name):
    driver.get(url)
    cookie_file = f"./cookies/{name}_cookies.pkl"
    with open(cookie_file, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    save_cookie(driver, "https://pan.baidu.com", "baidu")
