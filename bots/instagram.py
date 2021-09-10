import time, sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

sys.path.append('../utils')
sys.path.append('../services')
sys.path.append('../uploads')
from scraper_obj import scraper_obj
from instagram_service import record_instagram
from credentials_service import get_user
from niches import instagram_niche_accounts


def bot_for_liking():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    niche = instagram_niche_accounts[user['niche']]
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get('https://instagram.com')
    wait.until(ec.presence_of_element_located((By.NAME, 'username'))).send_keys(user['instagram'])
    wait.until(ec.presence_of_element_located((By.NAME, 'password'))).send_keys(user['instagram_password'])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.sqdOP.L3NKy.y3zKF'))).click()
    search = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@placeholder="Search"]')))
    search.send_keys(niche)
    accountfound = False
    posts = 0
    try:
        time.sleep(2)
        account = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.Igw0E.HVWg4')))
        accountfound = True
        account.click()
    except Exception as e:
        print(e, 'Account not found!')
        driver.close()
    # If account exists or not
    if accountfound:
        try:
            posts = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'g47SY '))).text
            if ',' in posts:
                posts = posts.replace(',', '')
            elif '.' in posts:
                posts = posts.replace('.', '')
            posts = int(posts)
        except Exception as e:
            print(e, 'This account has no posts!')
            driver.close()
    # If account has any posts or not
    if posts > 0:
        image = wait.until(ec.presence_of_element_located((By.CLASS_NAME, '_9AhH0')))
        time.sleep(2)
        image.click()
        for i in range(posts - 1):
            # If post is already liked or not
            try:
                likebtn = wait.until(ec.presence_of_element_located(
                    (By.XPATH, "//*[name()='svg'][@aria-label='Like']")))
                likebtn.click()
            except:
                wait.until(ec.presence_of_element_located(
                    (By.XPATH, "//*[name()='svg'][@aria-label='Unlike']")))
                pass
            finally:
                time.sleep(2)
                nextpost = wait.until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, '._65Bje.coreSpriteRightPaginationArrow')))
                nextpost.click()
        # Image window closed
        close = wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/button')))
        close.click()
        driver.close()


def bot_for_following():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    niche = instagram_niche_accounts[user['niche']]
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get('https://instagram.com')
    wait.until(ec.presence_of_element_located((By.NAME, 'username'))).send_keys(user['instagram'])
    wait.until(ec.presence_of_element_located((By.NAME, 'password'))).send_keys(user['instagram_password'])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.sqdOP.L3NKy.y3zKF'))).click()
    search = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@placeholder="Search"]')))
    search.send_keys(niche)
    accountfound = False
    followers = 0
    try:
        time.sleep(2)
        account = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.Igw0E.HVWg4')))
        accountfound = True
        account.click()
    except Exception as e:
        print(e, 'Account not found!')
    # If account exists or not
    if accountfound:
        try:
            followers = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'g47SY  ')))
            # If followers are 1,234, change the number to 1234
            if ',' in followers[1].text:
                followers = int((followers[1].text.replace(',', '')))
            # If followers are 123k, change the number to 123000
            elif 'k' in followers[1].text:
                k = followers[1].text.replace('k', '000')
                # If followers are 1.2k, change the number to 12000
                if '.' in k:
                    followers = int(k.replace('.', ''))
                else:
                    followers = int(k)
            # If followers are 123m, change the number to 12000000
            elif 'm' in followers[1].text:
                m = followers[1].text.replace('m', '000000')
                # If followers are 1.2m, change the number to 12000000
                if '.' in m:
                    followers = int(m.replace('.', ''))
                else:
                    followers = int(m)
            else:
                followers = int(followers[1].text)
        except Exception as e:
            print(e, 'This account has no followers!')
            driver.close()
    # If account has any follower or not
    if followers > 0:
        f = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, '-nal3 ')))
        time.sleep(2)
        f[1].click()
        # The loop paramter is used for number of accounts to be followed if no account is previously followed
        # or it is used to loop through all the previously followed accounts and search for new accounts to follow
        for i in range(50):
            # If first followers page accounts are not followed
            try:
                followbtn = wait.until(
                    ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.sqdOP.L3NKy.y3zKF     ')))
                # Click on the very first account of the list that is not followed
                if followbtn[0].text == 'Follow':
                    followbtn[0].click()
                    record_instagram(username=user['instagram'], package=user['pack'], followers=None,
                                     follow_requests=1)
                    time.sleep(2)
            # If first followers page accounts are already followed then scroll down
            except:
                print('No new accounts on this page, scrolling down...')
                followers_list = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'isgrP')))
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_list)
    driver.close()


def record_stats():
    username = input("Enter customer's username: ")
    user = get_user(username=username)
    driver = scraper_obj()
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get('https://instagram.com')
    wait.until(ec.presence_of_element_located((By.NAME, 'username'))).send_keys(user['instagram'])
    wait.until(ec.presence_of_element_located((By.NAME, 'password'))).send_keys(user['instagram_password'])
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.sqdOP.L3NKy.y3zKF'))).click()
    time.sleep(3)
    driver.get('https://instagram.com/' + user['instagram'])
    followers = wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'g47SY  ')))[1].text
    record_instagram(username=user['instagram'], package=user['pack'], followers=int(followers), follow_requests=None)
    driver.close()


if __name__ == "__main__":
    print('----- Welcome to Instagram Promotion -----')
    print("1) Like other's Instagram Photos")
    print("2) Follow others on Instagram")
    print("3) Record users's profile stats")
    try:
        choice = int(input('Select your choice: '))
        if choice == 1:
            bot_for_liking()
        elif choice == 2:
            bot_for_following()
        elif choice == 3:
            record_stats()
        else:
            print('Invalid choice!')
    except Exception as e:
        print(e)
        print('Invalid input, please try again.')
