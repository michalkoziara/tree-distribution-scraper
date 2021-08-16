from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class DriverGenerator:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument('log-level=2')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        print('The driver was just created.')

    def __del__(self):
        self.driver.quit()
        print('The driver has terminated.')
