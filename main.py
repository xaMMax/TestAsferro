import string
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import chromedriver_binary

from test_data import username, password, url


class TestEmail:
    def __init__(self, username_email, user_password, url_address=None):
        self.driver = None
        self.username = username_email
        self.password = user_password
        self.url = url_address
        self.random_string = ''
        self.session = ''

    def randomString(self):
        self.random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return self.random_string

    def build_driver(self):
        options = chrome_options()
        options.add_argument('chrome')  # use headless if you do not need a browser UI
        options.add_argument('--start-maximised')
        options.add_argument('--window-size=1600,900')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        stealth(self.driver,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=False,
                run_on_insecure_origins=False
                )

        return self.driver

    def login(self, url_address):
        try:
            self.driver.get(url_address)

            self.session = self.driver.session_id
            print(f'session = {self.session}')

            sleep(1.4)
            self.driver.switch_to.frame(1)
            sleep(2)
            self.driver.switch_to.frame(0)
            self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
            print('Successfully Accepted')
        except print('Cant do anything'):
            pass
            print('Could not click')
        sleep(5)
        try:
            self.driver.find_element(By.XPATH, '//*[@id="login-email"]').send_keys(username)
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login-password"]').send_keys(password)
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="header-login-box"]/form/button/span').click()
            print('Logged is Successfully')
            sleep(5)
        except print('Cant do anything'):
            pass
        return self.driver, self.session

    def send_mail(self):
        try:
            self.driver.switch_to.parent_frame()
            self.driver.find_element(By.XPATH, '//*[@id="actions-menu-primary"]/a[2]').click()
            print('Clicked on mail button')
            sleep(3)

            self.driver.switch_to.frame(4)
            self.driver.find_element(By.XPATH, "//a[contains(text(),'Compose E-mail')]").click()
            print('Clicked on NEW mail button')
            sleep(3)

            send_to_user = self.driver.find_element(By.XPATH, "(//input[@type='text'])[2]")
            send_to_user.send_keys(self.username)
            send_to_user.send_keys(Keys.ENTER)
            print('Clicked on send to username button')
            sleep(2)

            typing_theme = self.driver.find_element(By.CLASS_NAME, 'mailobjectpanel-textfield_input')
            typing_theme.send_keys(self.randomString())
            print('typed  theme')
            sleep(1)

            self.driver.switch_to.frame(1)
            print('Was switched to frame')
            self.driver.find_element(By.XPATH, '//*[@id="body"]/div')
            print('Was found')
            body_click = self.driver.find_element(By.XPATH, '//*[@id="body"]/div')
            print('Was found')
            self.driver.execute_script(f"arguments[0].innerText = '{self.randomString()}'", body_click)
            print('typed body ')
            sleep(2)

            self.driver.switch_to.parent_frame()
            self.driver.find_element(By.ID, 'compose-send-button').click()
            sleep(2)

            self.driver.switch_to.parent_frame()
            self.driver.find_element(By.XPATH, "//span[contains(.,'Home')]").click()
            print('return home')
        except print('Cant do anything'):
            pass

    def check_mail(self):
        self.driver.switch_to.parent_frame()
        self.driver.find_element(By.XPATH, '//*[@id="actions-menu-primary"]/a[2]').click()
        print('Clicked on mail button AGAIN from chack mail')
        sleep(2)
        self.driver.switch_to.frame(5)
        # to_print = self.driver.find_elements(By.TAG_NAME, 'div')
        # print(to_print)


def main():
    new = TestEmail(username, password)
    new.build_driver()
    new.login(url_address=url)
    new.send_mail()
    new.check_mail()


if __name__ == '__main__':
    main()
