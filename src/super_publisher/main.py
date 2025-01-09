import atexit
import logging
import asyncio

from super_publisher.driver import load_config, init_driver
from super_publisher.goofish import login_to_im, start_auto_deliver


async def async_task():
    logging.info("Starting async task")
    config_file = "./locator.yml"
    load_config(config_file)
    driver = init_driver(True)
    atexit.register(lambda: driver.quit())

    try:
        login_to_im(driver)
        task = asyncio.create_task(start_auto_deliver(driver))
        await asyncio.gather(task)
    finally:
        driver.quit()


def main():
    asyncio.run(async_task())
