from selenium.common.exceptions import NoSuchElementException
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yaml


locator_dict = dict()
locator_order = [By.ID, By.XPATH, By.CSS_SELECTOR]


class LocatorKey:
    # login
    JOIN_BUTTON = "join_button"

    # conversation
    CONVERSATION = "conversation"
    TAG_TO_BE_SENT = "tag_to_be_sent"

    # message
    MESSAGE_BOX = "message_box"
    MESSAGE_LIST = "message_list"
    CARD_MSG_TITLE = "card_msg_title"
    TEXT_MSG_RECV = "text_msg_recv"
    TEXT_MSG_SEND = "text_msg_send"

    # input
    TEXTAREA = "textarea"
    SEND_BUTTON = "send_button"


def load_config(file_path):
    try:
        with open(file_path, "r") as file:
            global locator_dict
            config = yaml.safe_load(file)
            for key, value in config.items():
                keys = key.split(".")
                d = locator_dict
                for k in keys[:-1]:
                    d = d.setdefault(k, {})
                d[keys[-1]] = value

    except FileNotFoundError:
        print("Configuration file not found")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")


def init_driver():
    # 设置 Selenium 无头模式
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=x1080")

    # 配置 Selenium Wire 来捕获请求
    return webdriver.Chrome(
        options=chrome_options,
        seleniumwire_options={"verify_ssl": False},
    )


def find_elements(driver, key):
    if key not in locator_dict:
        return []

    locators = locator_dict[key]
    by = list(locators.keys())[0]
    value = locators[by]
    return driver.find_elements(by, value)


def find_element(driver, key):
    try:
        if key not in locator_dict:
            return None

        locators = locator_dict[key]
        by = list(locators.keys())[0]
        value = locators[by]
        return driver.find_element(by, value)

    except NoSuchElementException:
        return None


if __name__ == "__main__":
    load_config("./locator.yml")
    msg_list = locator_dict["message_list"]
    print(list(msg_list.keys())[0])
    print(next(iter(msg_list)))
