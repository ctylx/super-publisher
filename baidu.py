import time
import pyperclip
from cookies import add_cookie

from driver import (
    NoElementException,
    click_element,
    init_driver,
    LocatorKey,
    find_element,
)
from selenium.webdriver.common.action_chains import ActionChains

login_url = "https://pan.baidu.com"
resource_url = "https://pan.baidu.com/disk/main#/index?category=all&path=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FSSS"


def get_share_link(driver, url):
    driver.get(url)
    time.sleep(3)
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
        click_element(driver, LocatorKey.BD_SHARE_BUTTON, 2)
        click_element(driver, LocatorKey.BD_SHARE_SEVEN_DAYS)
        click_element(driver, LocatorKey.BD_SHARE_CREATE_LINK, 2)
        click_element(driver, LocatorKey.BD_SHARE_COPY_LINK)
        return pyperclip.paste()

    except NoElementException as e:
        print(e.message)


if __name__ == "__main__":
    driver = init_driver()
    add_cookie(driver, login_url, "baidu")
    driver.refresh()
    time.sleep(2)

    print(get_share_link(driver, resource_url))
