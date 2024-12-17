from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import cookies
import driver
import time

login_url = "https://pan.baidu.com"


def get_share_link(driver, url):
    # right click on element
    td = driver.find_element(
        By.CSS_SELECTOR,
        "[index='0'] [draggable] div:nth-of-type(2)",
    )
    action = ActionChains(driver)
    action.context_click(td).perform()

    # click share button
    share_btn = driver.find_element(
        By.CSS_SELECTOR,
        "body .wp-s-ctx-menu .is-has-icon:nth-of-type(4)",
    )
    share_btn.click()

    # select 7 days for share
    time.sleep(2)
    seven_days = driver.find_element(
        By.XPATH,
        "//div[@id='pane-link']//form//div[@class='wp-s-share-to-link__create-form-radiu']/div[@role='radiogroup']/label[2]/span[@class='u-radio__label']",
    )
    seven_days.click()

    # create link
    create_link = driver.find_element(
        By.CSS_SELECTOR,
        ".is-round.u-button.u-button--medium.u-button--primary.wp-s-dialog-button-hoc.wp-s-share-to-link__create-form-submit--button",
    )
    create_link.click()

    # copy link
    time.sleep(2)
    copy_link = driver.find_element(
        By.XPATH,
        "//div[@id='pane-link']/div[@class='wp-s-share-to-link']/div//div[@class='wp-s-share-to-link__link-copy-wrapper']/button[@type='button']",
    )
    copy_link.click()
    return pyperclip.paste()


if __name__ == "__main__":
    url = "https://pan.baidu.com/disk/main#/index?category=all&path=%2F%E6%88%91%E7%9A%84%E9%9F%B3%E4%B9%90%2FSSS"

    driver = driver.init_driver()
    cookies.add_cookie(driver, login_url, "baidu")
    driver.refresh()
    driver.get(url)

    time.sleep(2)
    print(get_share_link(driver, url))
