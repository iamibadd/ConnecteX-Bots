import time, os, sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

sys.path.append('../utils')
sys.path.append('../services')
sys.path.append('../uploads')
from scraper_obj import scraper_obj
from facebook_service import record_facebook, record_facebook_posts
from credentials_service import get_user
from niches import facebook_niche_posts


def add_post():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    post = facebook_niche_posts[user['niche']]
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.facebook.com/login')
    wait.until(ec.presence_of_element_located((By.ID, 'email'))).send_keys(user['facebook'])
    wait.until(ec.presence_of_element_located((By.ID, 'pass'))).send_keys(user['facebook_password'])
    wait.until(ec.presence_of_element_located((By.ID, 'loginbutton'))).click()
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Account"]'))).click()
    time.sleep(1)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.ow4ym5g4.scb9dxdr'))).click()
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.XPATH, '//span[contains(text(),"What\'s on your mind?")]'))).click()
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="What\'s on your mind?"]'))).send_keys(
        post)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Post"]'))).click()
    record_facebook(email=user['facebook'], package=user['pack'], friends=None)
    record_facebook_posts(user=user['username'], email=user['facebook'], package=user['pack'], post=post)
    time.sleep(2)
    path = '/friends'
    if driver.current_url[-1] == '/':
        path = 'friends'
    driver.get(driver.current_url + path)
    friends = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.d2edcug0.knj5qynh.q66pz984'))).text
    record_facebook(email=user['facebook'], package=user['pack'], friends=friends)


def add_post_to_page():
    try:
        username = input("Enter customer's username: ")
        user = get_user(username=username)
        post = facebook_niche_posts[user['niche']]
        driver = scraper_obj()
        wait = WebDriverWait(driver=driver, timeout=15)
        driver.get('https://www.facebook.com/login')
        wait.until(ec.presence_of_element_located((By.ID, 'email'))).send_keys(user['facebook'])
        wait.until(ec.presence_of_element_located((By.ID, 'pass'))).send_keys(user['facebook_password'])
        wait.until(ec.presence_of_element_located((By.ID, 'loginbutton'))).click()
        time.sleep(2)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Menu"]'))).click()
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search menu"]'))).send_keys(
            'Page')
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'ul[aria-label="1 suggested search"]'))).click()
        time.sleep(2)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.fdg1wqfs.j83agx80'))).find_element_by_tag_name(
            'a').click()
        time.sleep(2)
        text = wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[data-visualcompletion="ignore"][style="border-radius: 20px;"]')))
        ActionChains(driver).move_to_element(text).click(text).perform()
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.notranslate._5rpu'))).send_keys(post)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))).click()
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Post"]'))).click()
        record_facebook(email=user['facebook'], package=user['pack'], friends=None)
        record_facebook_posts(user=user['username'], email=user['facebook'], package=user['pack'], post=post)
    except Exception as e:
        print(e)


def add_image_with_caption():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    caption = facebook_niche_posts[user['niche']]
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.facebook.com/login')
    wait.until(ec.presence_of_element_located((By.ID, 'email'))).send_keys(user['facebook'])
    wait.until(ec.presence_of_element_located((By.ID, 'pass'))).send_keys(user['facebook_password'])
    wait.until(ec.presence_of_element_located((By.ID, 'loginbutton'))).click()
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Account"]'))).click()
    time.sleep(1)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.ow4ym5g4.scb9dxdr'))).click()
    time.sleep(5)
    os.chdir('../uploads')
    match = "image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv"
    if user['niche'] == 'sports' or user['niche'] == 'Sports' or user['niche'] == 'SPORTS':
        wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input.mkhogb32[accept="' + match + '"]'))).send_keys(
            os.getcwd() + '/' + 'sports.jpg')
    elif user['niche'] == 'motivation' or user['niche'] == 'Motivation' or user['niche'] == 'MOTIVATION':
        wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input.mkhogb32[accept="' + match + '"]'))).send_keys(
            os.getcwd() + '/' + 'motivation.jpg')
    time.sleep(3)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="What\'s on your mind?"]'))).send_keys(
        caption)
    time.sleep(1.5)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Post"]'))).click()
    record_facebook(email=user['facebook'], package=user['pack'], friends=None)
    record_facebook_posts(user=user['username'], email=user['facebook'], package=user['pack'], post=caption)


def add_image_with_caption_to_page():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    caption = facebook_niche_posts[user['niche']]
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.get('https://www.facebook.com/login')
    wait.until(ec.presence_of_element_located((By.ID, 'email'))).send_keys(user['facebook'])
    wait.until(ec.presence_of_element_located((By.ID, 'pass'))).send_keys(user['facebook_password'])
    wait.until(ec.presence_of_element_located((By.ID, 'loginbutton'))).click()
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Menu"]'))).click()
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search menu"]'))).send_keys(
        'Page')
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'ul[aria-label="1 suggested search"]'))).click()
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.fdg1wqfs.j83agx80'))).find_element_by_tag_name(
        'a').click()
    time.sleep(2)
    os.chdir('../uploads')
    match = "image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv"
    if user['niche'] == 'sports' or user['niche'] == 'Sports' or user['niche'] == 'SPORTS':
        wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input.mkhogb32[accept="' + match + '"]'))).send_keys(
            os.getcwd() + '/' + 'sports.jpg')
    elif user['niche'] == 'motivation' or user['niche'] == 'Motivation' or user['niche'] == 'MOTIVATION':
        wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input.mkhogb32[accept="' + match + '"]'))).send_keys(
            os.getcwd() + '/' + 'motivation.jpg')
    time.sleep(3)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.notranslate._5rpu'))).send_keys(caption)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))).click()
    time.sleep(2)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Post"]'))).click()
    record_facebook(email=user['facebook'], package=user['pack'], friends=None)
    record_facebook_posts(user=user['username'], email=user['facebook'], package=user['pack'], post=caption)


if __name__ == "__main__":
    print('----- Welcome to Facebook Promotion -----')
    print("1) Add a Post (Profile)")
    print("2) Upload an Image (Profile)")
    print("3) Add a Post (Page)")
    print("4) Upload an Image (Page)")
    try:
        choice = int(input('Select your choice: '))
        if choice == 1:
            add_post()
        elif choice == 2:
            add_image_with_caption()
        elif choice == 3:
            add_post_to_page()
        elif choice == 4:
            add_image_with_caption_to_page()
    except Exception as e:
        print(e)
        print('Invalid input, please try again.')
