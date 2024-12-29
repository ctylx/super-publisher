from super_publisher.driver import load_config, init_driver
from super_publisher.goofish import login_to_im, start_auto_deliver


def main():
    config_file = "./locator.yml"
    load_config(config_file)

    driver = init_driver(True)
    login_to_im(driver)
    start_auto_deliver(driver)
