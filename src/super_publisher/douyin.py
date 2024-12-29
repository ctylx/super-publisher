import os
import sys
import time
import pyperclip

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait


def read_head(file):
    if os.path.exists(file):
        with open(file, "r", encoding="UTF-8") as file:
            # 读取文件内容
            head = file.readline()
            return head
    else:
        return ""


# 读取第一行之后 添加一个回车，适用于第一行是文章标题的情况
def read_file_with_extra_enter(file):
    with open(file, "r", encoding="UTF-8") as f:
        # 读取文件内容
        content = f.read()
        # 使用splitlines()将内容分割成行列表
        lines = content.splitlines()
        # 检查列表是否为空，并且只处理第一行（如果存在）
        if lines:
            # 在第一行末尾添加换行符（如果它不存在）
            if not lines[0].endswith("\n"):
                lines[0] += "\n"
        # 使用join()将行重新组合成字符串
        cleaned_content = "\n".join(lines)
        return cleaned_content


def get_chrome_driver():
    # 设置 ChromeDriver 路径
    chrome_driver_path = "./driver/chromedriver-mac-arm64/chromedriver"  # 将此路径替换为你的 ChromeDriver 路径

    # 创建 ChromeDriver 服务
    service = Service(chrome_driver_path)

    # 设置 Chrome 选项（例如，无头模式）
    chrome_options = Options()
    chrome_options.page_load_strategy = "normal"
    chrome_options.debugger_address = "127.0.0.1:9222"
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def publish_video(driver, video_file, text_file):
    # 打开新标签页并切common_config换到新标签页
    driver.switch_to.new_window("tab")

    # 浏览器实例现在可以被重用，进行你的自动化操作
    douyin_site = "https://creator.douyin.com/creator-micro/content/upload"
    driver.get(douyin_site)
    time.sleep(2)  # 等待2秒

    # telephone = driver.find_element(By.XPATH, '//input[@type="tel"]')
    # telephone.send_keys("17681808881")
    # sms = driver.find_element(By.XPATH, '//div[@class="douyin-creator-vmock-input-suffix"]//span[text()="发送验证码"]')
    # sms.click()

    # 设置等待
    # wait = WebDriverWait(driver, 10)

    # 发布图文
    # image_tab = driver.find_element(By.XPATH, '//div[@data-placeholder="发布图文"]')
    # image_tab.click()
    # time.sleep(2)

    # 上传视频按钮
    # file_input = driver.find_element(By.NAME,'upload-btn')
    file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    file_input.send_keys(video_file)
    time.sleep(10)  # 等待
    # 等待视频上传完毕
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'semi-input semi-input-default')))

    # 设置标题
    title = driver.find_element(
        By.XPATH, '//input[@class="semi-input semi-input-default"]'
    )
    title_text = read_head(text_file)
    common_title = ""

    # 标题有30字长度限制
    if len(common_title + title_text) <= 30:
        title.send_keys(common_title + title_text)
    else:
        title.send_keys(title_text)
    time.sleep(2)

    # 设置内容
    content = driver.find_element(By.XPATH, '//div[@data-placeholder="添加作品简介"]')
    content.click()
    time.sleep(2)

    # 将要粘贴的文本内容复制到剪贴板
    content_text = read_file_with_extra_enter(text_file)
    pyperclip.copy(content_text)

    # 模拟实际的粘贴操作
    action_chains = webdriver.ActionChains(driver)
    cmd_ctrl = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
    action_chains.key_down(cmd_ctrl).send_keys("v").key_up(cmd_ctrl).perform()
    time.sleep(2)

    # 设置tags
    tags = ["测试", "学习"]
    for tag in tags:
        # firefox没有原x:
        print("tag:", tag)
        content.send_keys(" ")
        content.send_keys(tag)
        time.sleep(2)
        content.send_keys(Keys.ENTER)
        time.sleep(1)
        content.send_keys(" ")
        time.sleep(2)

    # 设置合集
    collection = ""
    if collection:
        collection_tag = driver.find_element(
            By.XPATH, '//div[contains(text(),"选择合集")]'
        )
        collection_tag.click()
        time.sleep(1)
        collection_to_select = driver.find_element(
            By.XPATH,
            f'//div[@class="semi-select-option collection-option"]//span[text()="{collection}"]',
        )
        collection_to_select.click()
        time.sleep(1)

    # 发布
    publish_button = driver.find_element(By.XPATH, '//button[text()="发布"]')
    print("auto publish")
    publish_button.click()


if __name__ == "__main__":
    current_directory = os.path.abspath(os.getcwd())
    video_file = (
        f"{current_directory}/assets/338806611-d96e5e50-cfe7-4f55-a0db-75f3ac28b39f.mp4"
    )
    text_file = f"{current_directory}/assets/test"
    driver = get_chrome_driver()
    publish_video(driver, video_file, text_file)
