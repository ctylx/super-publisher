import time
import yaml

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException

from super_publisher.message import send_notify

locator_dict = dict()
locator_order = [By.ID, By.XPATH, By.CSS_SELECTOR]


class LocatorKey:
    # goofish
    GF_JOIN_BUTTON = "gf_join_button"
    GF_CONVERSATION = "gf_conversation"
    GF_TAG_TO_BE_SENT = "gf_tag_to_be_sent"
    GF_MESSAGE_BOX = "gf_message_box"
    GF_MESSAGE_LIST = "gf_message_list"
    GF_CARD_MSG_TITLE = "gf_card_msg_title"
    GF_TEXT_MSG_RECV = "gf_text_msg_recv"
    GF_TEXT_MSG_SEND = "gf_text_msg_send"
    GF_TEXTAREA = "gf_textarea"
    GF_SEND_BUTTON = "gf_send_button"

    # baidu
    BD_HOME_AD = "bd_home_ad"
    BD_RESOURCE_ROW = "bd_resource_row"
    BD_SHARE_BUTTON = "bd_share_button"
    BD_SHARE_SEVEN_DAYS = "bd_share_seven_days"
    BD_SHARE_CREATE_LINK = "bd_share_create_link"
    BD_SHARE_COPY_LINK = "bd_share_copy_link"
    BD_SHARE_LINK_INPUT = "bd_share_link_input"
    BD_SHARE_CODE_INPUT = "bd_share_code_input"


class NoElementException(Exception):
    def __init__(self, key, message):
        super().__init__(message)
        self.message = message
        self.key = key


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


def init_driver(headless: bool = False):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")

    # 设置 Selenium 无头模式
    if headless:
        chrome_options.add_argument("--headless")

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
    by = by.replace("_", " ")
    return driver.find_elements(by, value)


def find_element(driver, key, raise_excpetion=True):
    try:
        if key not in locator_dict:
            if raise_excpetion:
                raise NoElementException(key, f"Element of '{key}' not in locator_dict")
            else:
                return None

        locators = locator_dict[key]
        by = list(locators.keys())[0]
        value = locators[by]
        by = by.replace("_", " ")
        return driver.find_element(by, value)

    except (NoSuchElementException, InvalidSelectorException):
        if raise_excpetion:
            send_notify(f"【告警】未找到对应页面元素：{key}")
            raise NoElementException(key, f"Element of '{key}' not found")
        else:
            return None


def click_element(driver, key, sleep_time=0):
    element = find_element(driver, key)
    assert element is not None
    element.click()

    time.sleep(sleep_time)
    return element


def get_attribute(driver, key, attribute):
    element = find_element(driver, key)
    assert element is not None
    return element.get_attribute(attribute)


def execute_with_new_tab(driver, func, *args, **kwargs):
    main_window = driver.current_window_handle
    try:
        # ActionChains(driver).key_down(Keys.COMMAND).send_keys("t").key_up(Keys.COMMAND).perform()
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        result = func(driver, *args, **kwargs)
        return result
    finally:
        driver.close()
        driver.switch_to.window(main_window)


if __name__ == "__main__":
    load_config("./locator.yml")
    msg_list = locator_dict["message_list"]
    print(list(msg_list.keys())[0])
    print(next(iter(msg_list)))
