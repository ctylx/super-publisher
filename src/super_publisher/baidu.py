import time
import logging
from selenium.webdriver.common.action_chains import ActionChains

from super_publisher.logger import logger
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
from super_publisher.message import send_notify


login_url = "https://pan.baidu.com"
test_res_url = "https://pan.baidu.com/disk/main#/index?category=all&path=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FSSS"
xyj_res_url = "https://pan.baidu.com/disk/main?_at_=1736091609313#/index?category=all&path=%2F%E8%B5%84%E6%BA%90%E5%88%86%E4%BA%AB%2F%E7%BB%98%E6%9C%AC%E9%9F%B3%E9%A2%91-%E7%8B%90%E7%8B%B8%E5%AE%B6%E8%A5%BF%E6%B8%B8%E8%AE%B0"


def is_share_text(text):
    return "https://pan.baidu.com" in text and "提取码" in text


def get_share_link(driver, url, retry_time=1):
    driver.get(url)
    time.sleep(1)
    driver.execute_script("document.elementFromPoint(0, 0).click();")
    if find_element(driver, LocatorKey.BD_HOME_AD, False):
        driver.execute_script("document.elementFromPoint(10, 10).click();")

    try:
        # 1. right click on element
        td = find_element(driver, LocatorKey.BD_RESOURCE_ROW)
        assert td is not None
        action = ActionChains(driver)
        action.context_click(td).perform()

        # 2. click share button
        # 3. select 7 days for share
        # 4. create share link
        click_element(driver, LocatorKey.BD_SHARE_BUTTON, 1)
        click_element(driver, LocatorKey.BD_SHARE_SEVEN_DAYS, 1)
        click_element(driver, LocatorKey.BD_SHARE_CREATE_LINK, 1)

        # get share link and share code
        share_link = get_attribute(driver, LocatorKey.BD_SHARE_LINK_INPUT, "value")
        share_code = get_attribute(driver, LocatorKey.BD_SHARE_CODE_INPUT, "value")
        return f"链接: {share_link} 提取码: {share_code} 复制这段内容后打开百度网盘手机App，操作更方便哦"

    except NoElementException as e:
        if retry_time > 0:
            logging.info(f"Retry get_share_link, retry time={retry_time}")
            return get_share_link(driver, url, retry_time - 1)

        message = f"获取百度云盘分享链接失败: {e.message}"
        send_notify(f"【告警】{message}")
        logger.error(message)
        return None


def login_get_share_link(driver, url):
    add_cookie(driver, login_url, "baidu")
    driver.refresh()
    time.sleep(2)
    return get_share_link(driver, url)


if __name__ == "__main__":
    config_file = "./locator.yml"
    load_config(config_file)

    driver = init_driver(True)
    add_cookie(driver, login_url, "baidu")
    driver.refresh()
    time.sleep(2)

    print(get_share_link(driver, xyj_res_url))
