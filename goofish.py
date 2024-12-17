import pickle
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def init_driver():
    # 设置 Selenium 无头模式
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # 配置 Selenium Wire 来捕获请求
    return webdriver.Chrome(
        options=chrome_options,
        seleniumwire_options={"verify_ssl": False},
    )


def login_to_im(driver, cookie_file):
    driver.get("https://www.goofish.com/im")
    with open(cookie_file, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # refresh page
    driver.refresh()

    # wait for login box
    login_box_id = "alibaba-login-box"
    driver_wait = WebDriverWait(driver, 10)
    driver_wait.until(EC.visibility_of_element_located((By.ID, login_box_id)))

    # click join button
    driver.switch_to.frame(login_box_id)
    join_buttion = driver.find_element(By.XPATH, "//button[text()='快速进入']")
    join_buttion.click()
    driver.switch_to.default_content()
    time.sleep(3)


def switch_conversation(driver):
    item = driver.find_element(
        By.XPATH,
        "/html//div[@id='conv-list-scrollable']/div[@class='rc-virtual-list']/div[@class='rc-virtual-list-holder']//div[@class='rc-virtual-list-holder-inner']/div/div//div[@class='ant-dropdown-trigger']/div/div",
    )
    item.click()
    time.sleep(2)


def get_chat_message(driver):
    chat_box = driver.find_element(By.ID, "message-list-scrollable")
    last_top = driver.execute_script("return arguments[0].scrollTop", chat_box)

    # scroll to top
    for _ in range(10):
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].clientHeight",
            chat_box,
        )

        new_top = driver.execute_script("return arguments[0].scrollTop", chat_box)
        if new_top == last_top:
            break

        last_top = new_top

    # return messages
    return driver.find_elements(
        By.XPATH,
        "//div[contains(@class, 'message-text--zV88pB7N')]",
    )


def start_loop(driver):
    pass


if __name__ == "__main__":
    driver = init_driver()
    login_to_im(driver, "./cookies/cookies.pkl")
    switch_conversation(driver)
    messages = get_chat_message(driver)
    for msg in messages:
        print(msg.text)

    time.sleep(100)
