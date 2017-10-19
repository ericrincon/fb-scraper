import time
import concurrent.futures

from scraper import utils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

import os
import urllib
from bs4 import BeautifulSoup

def scrape_profile_pictures(browser, friend_url, number_of_pictures, number_of_trys=3):
    """

    :param friend_url:
    :param number_of_pictures:
    :return:
    """
   # browser = webdriver.Firefox()
    browser.get(friend_url)

    name = browser.find_element_by_xpath('//span[@id="fb-timeline-cover-name"]').text
    print('Scraping {}\'s profile...'.format(name.encode('utf-8', 'ignore')))

    photos_link = browser.find_element_by_xpath('//a[@data-tab-key="photos"]')

    photos_link.click()
    profile_picture = browser.find_element_by_xpath('//a[@class="profilePicThumb"]')

    profile_picture.click()

    pictures_downloaded = 0

    image_trys = 0
    next_trys = 0

    if not os.path.exists('images/' + name):
        os.makedirs('images/' + name)
    else:
        return "{} pictures already downloaded for {}!".format(pictures_downloaded, name)

    with open('images/' + name + '/info.txt', 'w') as profile_info:
        profile_info.write(friend_url)

    for i in range(number_of_pictures):
        time.sleep(1)

        try:
            image_element = browser.find_element_by_xpath('//img[@class="spotlight"]')
        except NoSuchElementException as e:
            print(e)

            if number_of_trys == image_trys:
                break

            image_trys += 1
            time.sleep(1)

            continue

        image_url = image_element.get_attribute('src')

        if 'Image may contain' in image_element.get_attribute('alt'):
            print('Image may have more than on person!')

        if not os.path.exists('images/' + name):
            os.makedirs('images/' + name)
        else:
            image_path =  'images/' + name + '/' + name + '_' + str(i)

            if not os.path.exists(image_path):
                urllib.request.urlretrieve(image_url,image_path)
                pictures_downloaded += 1
        try:
            next_button = browser.find_element_by_xpath('//a[@title="Next"]')
            next_button.click()
        except Exception as e:
            print(e)

            if number_of_trys == next_trys:
                break

            next_trys += 1




    return "{} pictures downloaded for {}".format(pictures_downloaded, name)


def start(username, password, number_of_pictures=10, max_workers=5):
    """

    :param username:
    :param password:
    :param number_of_pictures:
    :param max_workers:
    :return:
    """
    browser = webdriver.Firefox()
    browser.get('https://www.facebook.com/')

    username_element = browser.find_element_by_id('email')
    password_element = browser.find_element_by_id('pass')

    username_element.send_keys(username)
    password_element.send_keys(password)

    login_button = browser.find_element_by_id('loginbutton')
    login_button.click()


    browser.implicitly_wait(3)

    profile_link = browser.find_element_by_xpath('//a[@title="Profile"]').get_attribute('href')
    browser.get(profile_link)

    friends_link = browser.find_element_by_xpath('//a[@data-tab-key="friends"]').get_attribute('href')
    browser.get(friends_link)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    while True:
        friends = browser.find_elements_by_xpath('//div[@class="fsl fwb fcb"]')
        elem = browser.find_element_by_css_selector('body')
        elem.send_keys(Keys.PAGE_DOWN)

        all_friends = browser.find_element_by_name('All Friends')
        number_of_friends = int(all_friends.text.replace('All Friends', ''))

        if len(friends) == number_of_friends:
           break

    print('Found {} friends!'.format(len(friends)))
    print('Creating friend URLs....')
    friend_urls = [friend_url.find_element_by_tag_name('a').get_attribute('href') for friend_url in friends]

    user_dirs = utils.get_subdirs('images')
    user_urls = []

    for dir in user_dirs:
        with open(dir + '/info.txt', 'r') as info_file:
            url = info_file.readline(1)
            print(url)


    print(user_urls)




    for friend_url in friend_urls:

        scrape_profile_pictures(browser, friend_url, number_of_pictures=number_of_pictures)


    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     executor.map(scrape_profile_pictures, friend_urls, [5 for _ in range(len(friend_urls))])
        # scraper_map = {executor.submit(scrape_profile_pictures, fb_profile_url, number_of_pictures)
        #                for fb_profile_url in friend_urls}
        #
        # executor.s
        # for future in concurrent.futures.as_completed(scraper_map):
        #     something = scraper_map[future]
        #
        #     try:
        #         result_message = future.result()
        #         print(result_message)
        #     except Exception as e:
        #         print(e)


