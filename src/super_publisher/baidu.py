import time
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains

from super_publisher.cookies import add_cookie
from super_publisher.driver import (
    NoElementException,
    click_element,
    get_attribute,
    load_config,
    init_driver,
    LocatorKey,
    find_element,
)


login_url = "https://pan.baidu.com"
resource_url = "https://pan.baidu.com/disk/main#/index?category=all&path=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FSSS"


def is_share_text(text):
    return "https://pan.baidu.com" in text and "提取码" in text


def get_share_link(driver, url):
    driver.get(url)
    time.sleep(1)
    if find_element(driver, LocatorKey.BD_HOME_AD, False):
        driver.execute_script("document.elementFromPoint(10, 10).click();")

    try:
        # 1. right click on element
        td = find_element(driver, LocatorKey.BD_RESOURCE_ROW)
        assert td is not None
        action = ActionChains(driver)
        action.context_click(td).perform()
        pyperclip.copy("")

        # 2. click share button
        # 3. select 7 days for share
        # 4. create share link
        # 5. copy share link
        click_element(driver, LocatorKey.BD_SHARE_BUTTON, 1)
        click_element(driver, LocatorKey.BD_SHARE_SEVEN_DAYS, 1)
        click_element(driver, LocatorKey.BD_SHARE_CREATE_LINK, 1)
        click_element(driver, LocatorKey.BD_SHARE_COPY_LINK)

        # get from clipboard
        share_text = pyperclip.paste()
        if is_share_text(share_text):
            return share_text

        # get share link and share code
        share_link = get_attribute(driver, LocatorKey.BD_SHARE_LINK_INPUT, "value")
        share_code = get_attribute(driver, LocatorKey.BD_SHARE_CODE_INPUT, "value")
        return f"链接: {share_link} 提取码: {share_code} 复制这段内容后打开百度网盘手机App，操作更方便哦"

    except NoElementException as e:
        print(e.message)


if __name__ == "__main__":
    config_file = "./locator.yml"
    load_config(config_file)

    driver = init_driver(True)
    add_cookie(driver, login_url, "baidu")
    driver.refresh()
    time.sleep(2)

    print(get_share_link(driver, resource_url))
