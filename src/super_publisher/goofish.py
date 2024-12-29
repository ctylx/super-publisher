import time
import logging
from enum import Enum

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from super_publisher.logger import logger
from super_publisher.cookies import add_cookie
from super_publisher.baidu import is_share_text
from super_publisher.driver import (
    init_driver,
    load_config,
    LocatorKey,
    find_element,
    find_elements,
)


class SenderType(Enum):
    BUYER = "buyer"
    SELLER = "seller"


class MessageType(Enum):
    CARD = "card"
    TEXT = "text"


class ChatMessage:
    def __init__(self, sender_type: SenderType, msg_type: MessageType, content: str):
        self.sender_type = sender_type
        self.msg_type = msg_type
        self.content = content

    def __repr__(self) -> str:
        return f"ChatMessage[sender: {self.sender_type.value}, type: {self.msg_type.value}, content: {self.content}]"


def login_to_im(driver):
    add_cookie(driver, "https://www.goofish.com/im", "goofish")
    driver.refresh()

    try:
        # wait for login box
        login_box_id = "alibaba-login-box"
        driver_wait = WebDriverWait(driver, 10)
        driver_wait.until(EC.visibility_of_element_located((By.ID, login_box_id)))

        # click join button
        driver.switch_to.frame(login_box_id)
        join_buttion = find_element(driver, LocatorKey.GF_JOIN_BUTTON)
        if join_buttion:
            join_buttion.click()
            driver.switch_to.default_content()
            logger.info("Login to goofish im page success")
            time.sleep(3)
    except TimeoutException:
        logger.warning("Waiting for login box timeout")
        pass


def is_wating_deliver(msg_list):
    for msg in reversed(msg_list):
        if msg.sender_type == SenderType.SELLER and is_share_text(msg.content):
            return False
        elif (
            msg.sender_type == SenderType.BUYER
            and "我已付款，等待你发货" in msg.content
        ):
            return True
    return False


def get_chat_message(driver):
    message_box = find_element(driver, LocatorKey.GF_MESSAGE_BOX, False)
    if message_box is None:
        logger.warning("message_box is None")
        return []

    # scroll to top
    last_top = driver.execute_script("return arguments[0].scrollTop", message_box)
    for _ in range(10):
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].clientHeight",
            message_box,
        )

        new_top = driver.execute_script("return arguments[0].scrollTop", message_box)
        if new_top == last_top:
            break

        last_top = new_top

    # return messages
    time.sleep(1)
    recent_messages = []
    for element in find_elements(driver, LocatorKey.GF_MESSAGE_LIST):
        title = find_element(element, LocatorKey.GF_CARD_MSG_TITLE, False)
        if title:
            msg = ChatMessage(SenderType.BUYER, MessageType.CARD, title.text)
            recent_messages.append(msg)
            continue

        text_recv = find_element(element, LocatorKey.GF_TEXT_MSG_RECV, False)
        if text_recv:
            msg = ChatMessage(SenderType.BUYER, MessageType.TEXT, text_recv.text)
            recent_messages.append(msg)
            continue

        text_send = find_element(element, LocatorKey.GF_TEXT_MSG_SEND, False)
        if text_send:
            msg = ChatMessage(SenderType.SELLER, MessageType.TEXT, text_send.text)
            recent_messages.append(msg)
            continue

    return recent_messages


def send_message(driver, text):
    # input text
    textarea = find_element(driver, LocatorKey.GF_TEXTAREA, False)
    if textarea:
        textarea.send_keys(Keys.TAB)
        textarea.clear()
        textarea.send_keys(text)

        # click send
        send_button = find_element(driver, LocatorKey.GF_SEND_BUTTON, False)
        if send_button:
            send_button.click()


def start_auto_deliver(driver):
    while True:
        time.sleep(5)
        for conversation in find_elements(driver, LocatorKey.GF_CONVERSATION):
            tag = find_element(conversation, LocatorKey.GF_TAG_TO_BE_SENT, False)
            if tag and tag.text == "等待卖家发货":
                conversation.click()
                time.sleep(1)

                logging.info("Found conversation to deliver")
                msg_list = get_chat_message(driver)
                for msg in msg_list:
                    print(msg)
                # if is_wating_deliver(msg_list):
                #     send_message(driver, "hello")


if __name__ == "__main__":
    config_file = "./locator.yml"
    load_config(config_file)

    driver = init_driver(True)
    login_to_im(driver)
    start_auto_deliver(driver)