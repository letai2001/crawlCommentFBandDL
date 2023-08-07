import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import itertools
from selenium.common.exceptions import NoSuchElementException
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
from queue import Queue
import json
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pickle
from selenium.webdriver.common.action_chains import ActionChains
import re



chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
chrome_options.add_argument("--disable-notification")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}') 
driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)

driver.get('https://www.facebook.com/')
sleep(3)
cookies = pickle.load(open("my_cookie_new.pkl" , "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
sleep(3)
driver.get('https://www.facebook.com/')
sleep(2)
data = []
def find_author(driver):

    # Danh sách các cấu trúc XPath có thể chứa tên tác giả
    xpaths = [
        '//div[@id="objects_container"]//table[@role="presentation"]//strong/span/a',
        '//div[@id="objects_container"]//table[@role="presentation"]//span/strong/a',
        '//div[@id="objects_container"]//table[@role="presentation"]//strong/a',
        '//div[@id="objects_container"]//table[@role="presentation"]//span/a'
    ]

    auth_element = None
    for xpath in xpaths:
        try:
            auth_element = driver.find_element(By.XPATH, xpath)
            break
        except:
            continue

    if auth_element:
        link = auth_element.get_attribute('href')
        text = auth_element.get_attribute('text')
        return link, text
    else:
        return None, None
def find_content(driver):
    try:
        div_elem = driver.find_element(By.XPATH, '//div[@data-ft=\'{"tn":"*s"}\']')
        # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
        p_elements = div_elem.find_elements(By.TAG_NAME, 'p')
        texts = [elem.text for elem in p_elements]

        # Gộp tất cả các dòng text thành một văn bản
        full_text = ' '.join(texts)
    except Exception as e:
        full_text = 'no content'
    return full_text
def count_react(driver , react):
    number = 0
    
    try:
        xpath_expression = f"//a[@role='button']/img[@alt='{react}']/following-sibling::span"
        reaction_count = driver.find_element(By.XPATH, xpath_expression).text
        if 'K' in reaction_count:
            number = int(float(reaction_count.replace('K', '')) * 1000)
        else:
            number = int(reaction_count)

    except Exception as e:
        pass
    return number

def count_react_item(driver , link):
    link_element = driver.find_element(By.XPATH, '//div[contains(@id, "sentence_")]//a[contains(@href, "/ufi/reaction/profile/")]')

# Lấy giá trị href từ thẻ a
    link_href = link_element.get_attribute('href')

    driver.get(link_href)
    
    sleep(1.5)
    
    # Duyệt qua từng thẻ div và tìm các thẻ con có arial-label chứa các reaction như "Like", "Haha", ...
    reaction_Like = count_react(driver , "Like")
    reaction_Love = count_react(driver , "Love")
    reaction_Care = count_react(driver , "Care")
    reaction_Wow = count_react(driver , "Wow")
    reaction_Haha = count_react(driver , "Haha")
    reaction_Angry = count_react(driver , "Angry")
    reaction_Huhu = count_react(driver , "Huhu")
    reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
    
    driver.get(link)
    sleep(1)

    return reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu
def find_all_images(driver):
    xpath_img = '//div[@data-ft=\'{"tn":"H"}\']//a[starts-with(@href, \'/photo.php?\')]//img'
    img_elements = driver.find_elements(By.XPATH , xpath_img)
    xpath_href_img = '//div[@data-ft=\'{"tn":"H"}\']//a[starts-with(@href, \'/photo.php?\')]'
    href_img_elements = driver.find_elements(By.XPATH , xpath_href_img)
    # Lưu trữ các liên kết hình ảnh
    image_links = [img_element.get_attribute("src") for img_element in img_elements]
    image_links_a = [href_img_element.get_attribute("href") for href_img_element in href_img_elements]
    ids_hrefs = [re.search(r'fbid=(\d+)', link).group(1) for link in image_links_a if re.search(r'fbid=(\d+)', link)]

    if len(image_links_a) >1:
        driver.get(image_links_a[len(image_links_a)-1])
        while(True):
            xpath_next = '//a[starts-with(@href, \'/photo.php?\') and normalize-space()="Next"]'
            next_element = driver.find_element(By.XPATH, xpath_next)
            next_link = next_element.get_attribute("href")
            id_match = re.search(r'fbid=(\d+)', next_link).group(1)

            if id_match not in ids_hrefs:
                image_links_a.append(next_link)
                ids_hrefs.append(id_match)
                driver.get(next_link)
                sleep(0.5)
                img_element = driver.find_element(By.XPATH, '//div[@style="text-align:center;"]//img')

                image_links.append(img_element.get_attribute("src"))

            else:
                break
    return image_links
def find_link_video(driver):
    video_link = "no video"
    try:
        element = driver.find_element(By.XPATH , "//a[starts-with(@href, '/video_redirect/')]")
        video_link = element.get_attribute("href")
    except Exception as e:
        pass
    return video_link

# for link in p_link:
link = 'https://mbasic.facebook.com/story.php?story_fbid=pfbid035S4MRdNibFUeFUd9jo5irfXwoeJz6vbWEHxuNPmBbhJ5UfTFhmmhTGM9enzLpCeMl&id=100091135001716&eav=AfaAlx4mtvXbQYDVHsGC4TIVCuV8Haf5jOO4VVAYHmrAMxhZ9zG3t8xHVUG_rQulCNU&__xts__%5B0%5D=12.AbouGJp2ikJ1NREfg7ef5L4K0y4Lb9UzsaikaBLXFr6v3UoyvldH68WiqGaudHgl9kpn1BqZB4ujwIgi4u2WnJxi3sW3e0J-wdUL_h4wUOhatU44bS4eAJ1vUdkeInl3CKcjh07bDZa_HtHTLjvvWqpq2YXZqQ2uw2fkGcHXtbyzsfIbUt8FScia-zBjGV3pHRLwDMp5uniMjR_JckKF-0ttMUFQaBepT8MsNvw29ARepX7HVxlQuW8DRMfi9p8CRB655zqinRXEx-0yEGXcUAa3Ge15pnDLIjwvdgu6L99n11-URCxbiAihUMaS_RcCEpgrd8FmqKudo8qL_z99a04OdA26pHKGxQ4sjNrGSRBJ-i-63lzf4qH5RfUOsCHJDwSark8fu7tE6P2DpWWdXBpw8RbQf7ApSa75vrW7_YNDdizb2B6WvGjn1xPr2c0HS0eLgGcQ2q5PRrGAji7vM0_sH5S--nb5ytj98nTVBCopZuBMBUs-uDKDqsEfmNaUhE4-EOoGOkcmne2cJMgnGL6yXQqo0nwnjWaM0Z23p8cCcwGRv6lIGP4cXNUiNeHgSrA7_Lf9t3Lwz758L_DqLNdNwuaMANLQ7MvqEsncR9Nk35eVBQfZWulmJ2N65_I9Iw9Zmt0CI6KK7J6T3h_98TfrtEzFwPGRZ0FLAsx2Tgdp6s6oY9BLowb-xbtvU_AeRMc&__tn__=%2AW&paipv=0'
driver.get(link)
sleep(2)
auth_link , auth_text = find_author(driver)
content = find_content(driver)
reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu = count_react_item(driver , link)
link_video = find_link_video(driver)
print(auth_link , auth_text)    
print(content)
print(reaction_All)
print(reaction_Love)
print(reaction_Wow)
print(link_video)
# In kết quả
image_links = find_all_images(driver)
for image_link in image_links:
    print(image_link)