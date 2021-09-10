import time, sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

sys.path.append('../utils')
sys.path.append('../services')
sys.path.append('../uploads')
from scraper_obj import scraper_obj
from credentials_service import get_user
from twitter_service import record_twitter, record_twitter_posts
from niches import twitter_niche_accounts, twitter_niche_posts


def followers():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.twitter.com/login')
    wait.until(ec.presence_of_element_located((By.NAME, 'session[username_or_email]'))).send_keys(user['twitter'])
    wait.until(ec.presence_of_element_located((By.NAME, 'session[password]'))).send_keys(user['twitter_password'])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))).click()
    time.sleep(3)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search query"]'))).send_keys(
        '@' + twitter_niche_accounts[user['niche']])
    time.sleep(1)
    driver.get('https://twitter.com/' + twitter_niche_accounts[user['niche']])
    driver.get('https://twitter.com/' + twitter_niche_accounts[user['niche']] + '/followers')
    time.sleep(3)
    for follow in wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.css-1dbjc4n.r-19u6a5r'))):
        if follow.text == "Follow":
            follow.click()
            record_twitter(username=user['twitter'], package=user['pack'], followers=None, post=None, follow_requests=1)
            time.sleep(2)


def add_post():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.twitter.com/login')
    wait.until(ec.presence_of_element_located((By.NAME, 'session[username_or_email]'))).send_keys(user['twitter'])
    wait.until(ec.presence_of_element_located((By.NAME, 'session[password]'))).send_keys(user['twitter_password'])
    wait.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))).click()
    time.sleep(3)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Tweet text"]'))).click()
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Tweet text"]'))).send_keys(
        twitter_niche_posts[user['niche']])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]'))).click()
    time.sleep(5)
    record_twitter(username=user['twitter'], package=user['pack'], followers=None, post=1, follow_requests=None)
    record_twitter_posts(user=user['username'], username=user['twitter'], package=user['pack'],
                         post=twitter_niche_posts[user['niche']])


def add_image_with_caption():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.twitter.com/login')
    wait.until(ec.presence_of_element_located((By.NAME, 'session[username_or_email]'))).send_keys(user['twitter'])
    wait.until(ec.presence_of_element_located((By.NAME, 'session[password]'))).send_keys(user['twitter_password'])
    wait.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))).click()
    time.sleep(3)
    os.chdir('../uploads')
    match = 'input[accept="image/jpeg,image/png,image/webp,image/gif,video/mp4,video/quicktime,video/webm"]'
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, match))).send_keys(os.getcwd() + '/' + 'sports.jpg')
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Tweet text"]'))).send_keys(
        twitter_niche_posts[user['niche']])
    time.sleep(1)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="tweetButtonInline"]'))).click()
    time.sleep(5)
    record_twitter(username=user['twitter'], package=user['pack'], followers=None, post=1, follow_requests=None)
    record_twitter_posts(user=user['username'], username=user['twitter'], package=user['pack'],
                         post=twitter_niche_posts[user['niche']])


def record_stats():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.twitter.com/login')
    wait.until(ec.presence_of_element_located((By.NAME, 'session[username_or_email]'))).send_keys(user['twitter'])
    wait.until(ec.presence_of_element_located((By.NAME, 'session[password]'))).send_keys(user['twitter_password'])
    wait.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="LoginForm_Login_Button"]'))).click()
    time.sleep(2)
    driver.get('https://www.twitter.com/' + user['twitter'])
    time.sleep(2)
    total_followers = wait.until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, 'a[href="/stonesncave/followers"]'))).text
    record_twitter(username=user['twitter'], package=user['pack'], followers=int(total_followers.split(' ')[0]),
                   post=None, follow_requests=None)


if __name__ == "__main__":
    print('----- Welcome to Twitter Promotion -----')
    print("1) Add a Post")
    print("2) Upload an Image")
    print("3) Increase followers")
    print("4) Record Stats")
    try:
        choice = int(input('Select your choice: '))
        if choice == 1:
            add_post()
        elif choice == 2:
            add_image_with_caption()
        elif choice == 3:
            followers()
        elif choice == 4:
            record_stats()
    except Exception as e:
        print(e)
        print('Invalid input, please try again.')
