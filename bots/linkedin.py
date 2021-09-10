import time, sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

sys.path.append('../utils')
sys.path.append('../services')
from scraper_obj import scraper_obj
from linkedin_service import record_linkedin, record_linkedin_posts
from credentials_service import get_user


def add_post(post):
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get('https://www.linkedin.com/login')
    wait.until(ec.presence_of_element_located((By.ID, 'username'))).send_keys(user['linkedin'])
    wait.until(ec.presence_of_element_located((By.ID, 'password'))).send_keys(user['linkedin_password'])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Sign in"]'))).click()
    time.sleep(5)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button.share-box-feed-entry__trigger'))).click()
    wait.until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[data-placeholder="What do you want to talk about?"]'))).send_keys(post)
    time.sleep(2)
    wait.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'button.share-actions__primary-action.ember-view'))).click()
    record_linkedin(email=user['linkedin'], package=user['pack'], connections='None', requests='None')
    record_linkedin_posts(user=user['username'], email=user['linkedin'], package=user['pack'], post=post)
    time.sleep(5)


def connect(niche):
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.linkedin.com/login')
    wait.until(ec.presence_of_element_located((By.ID, 'username'))).send_keys(user['linkedin'])
    wait.until(ec.presence_of_element_located((By.ID, 'password'))).send_keys(user['linkedin_password'])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Sign in"]'))).click()
    time.sleep(2)
    driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
    time.sleep(5)
    connections = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.mn-connections__header'))).text
    connections = connections.split(' Connections')[0]
    driver.get('https://www.linkedin.com/feed/')
    record_linkedin(email=user['linkedin'], package=user['pack'], connections=int(connections), requests='None')
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search"]'))).send_keys(niche,
                                                                                                           Keys.ENTER)
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.linked-area.cursor-pointer'))).click()
    try:
        wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, '.org-top-card-secondary-content__connections'))).find_elements_by_tag_name('a')[
            1].click()
        time.sleep(2)
        for i in range(50):
            for c in wait.until(ec.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view'))):
                if c.text == 'Connect':
                    c.click()
                    wait.until(
                        ec.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Send now"]'))).click()
                    time.sleep(1)
                    record_linkedin(email=user['linkedin'], package=user['pack'], connections='None',
                                    requests='Requesting')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
            next_btn = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Next"]')))
            if next_btn.get_attribute('disabled') is None:
                next_btn.click()
                time.sleep(3)
            else:
                break
    except Exception as e:
        print(e)
        print('This profile is private!')


if __name__ == "__main__":
    print('----- Welcome to Lindedin Promotion -----')
    print("1) Add a Post")
    print("2) Make Connections")
    try:
        choice = int(input('Select your choice: '))
        if choice == 1:
            add_post(post="Thats another post!!!!")
        if choice == 2:
            connect(niche='s&p global')
        else:
            print('Invalid choice!')
    except:
        print('Invalid input, please try again.')
