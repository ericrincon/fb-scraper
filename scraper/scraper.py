import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

import os
import urllib
import urllib2
from bs4 import BeautifulSoup

url = "http://icecat.biz/p/toshiba/pscbxe-01t00een/satellite-pro-notebooks-4051528049077-Satellite+Pro+C8501GR-17732197.html"
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

imgs = soup.findAll("div", {"class":"thumb-pic"})
for img in imgs:
        imgUrl = img.a['href'].split("imgurl=")[1]
        urllib.urlretrieve(imgUrl, os.path.basename(imgUrl + '.png'))



def screpe_friends(browser, friend_urls, number_of_pictures):
    for friend_url in friend_urls:
        browser.get(friend_url)
        name = browser.find_element_by_xpath('//span[@id="fb-timeline-cover-name"]').text
        print('Scraping {}\'s profile...'.format(name.encode('utf-8', 'ignore')))

        photos_link = browser.find_element_by_xpath('//a[@data-tab-key="photos"]')

        photos_link.click()
        profile_picture = browser.find_element_by_xpath('//a[@class="profilePicThumb"]')

        profile_picture.click()

        for i in range(number_of_pictures):
            time.sleep(1)

            try:
                image_element = browser.find_element_by_xpath('//img[@class="spotlight"]')
            except NoSuchElementException as e:
                print(e)

                time.sleep(1)
                image_element = browser.find_element_by_xpath('//img[@class="spotlight"]')

            image_url = image_element.get_attribute('src')

            if 'Image may contain' in image_element.get_attribute('alt'):
                print('Image may have more than on person!')


            if not os.path.exists('images/' + name):
                os.makedirs('images/' + name)
            else:
                urllib.urlretrieve(image_url, 'images/' + name + '/' + name + '_' + str(i))

            next_button = browser.find_element_by_xpath('//a[@title="Next"]')
            next_button.click()




def scrape(username, password):
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
       # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        friends = browser.find_elements_by_xpath('//div[@class="fsl fwb fcb"]')
        elem = browser.find_element_by_css_selector('body')
        elem.send_keys(Keys.PAGE_DOWN)

        all_friends = browser.find_element_by_name('All Friends')
        number_of_friends = int(all_friends.text.replace('All Friends', ''))

        if len(friends) == number_of_friends:
           break
    print('Found {} friends!'.format(len(friends)))
    print('Getting friend URLs....')
    friend_urls = [friend_url.find_element_by_tag_name('a').get_attribute('href') for friend_url in friends]

    screpe_friends(browser, friend_urls, 5)
