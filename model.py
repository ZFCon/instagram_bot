from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from time import sleep
from decouple import config

from utils import save_list_as_file


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramVisitor:
    url = "https://www.instagram.com"

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)

    def close(self):
        sleep(30)
        self.driver.close()

        logger.info('browser closed.')

    def login(self, username, password):
        self.driver.get(self.url)
        username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name,'username')]")))
        username_field.send_keys(username)
        password_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password_field.send_keys(password)

        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Log In')]")))
        login_btn.click()

        logger.info('logged in.')



    def go_profile(self):
        picture_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//nav[contains(@class,'')]//div[5]")))
        picture_btn.click()

        profile_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Profile')]")))
        profile_btn.click()

        logger.info('visited profile.')
    

    def go_followings(self):
        self.go_profile()

        # click following button.
        followers_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li/a[contains(.,'following')]")))
        followers_btn.click()

        reached_bottom = False
        usernames = []
        counter = 1
        while not reached_bottom:
            try:
                follower_pattern = f"//div[contains(@aria-label,'Following')]//ul//li[{counter}]//span/a"
                follower_element = self.wait.until(EC.presence_of_element_located((By.XPATH, follower_pattern)))
                username = follower_element.text
                counter +=1

                # add username to the list.
                usernames.append(username)
                logger.info(f"{counter} - {username} appended.")

                # scroll to the element.
                follower_element.location_once_scrolled_into_view
            except TimeoutException as e:
                reached_bottom = True
                save_list_as_file(usernames, 'graviit_followings')

        logger.info('opend followings list.')



visitor = InstagramVisitor()
USERNAME = config("INSTAGRAM_USERNAME", cast=str)
PASSWORD = config("INSTAGRAM_PASSWORD", cast=str)
visitor.login(username=USERNAME, password=PASSWORD)
visitor.go_followings()
visitor.close()