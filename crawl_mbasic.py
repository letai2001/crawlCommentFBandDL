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
        full_text = ''
    return full_text
def find_content_background(driver):
    try:
        divs_with_style = driver.find_element(By.XPATH , '//div[@data-ft=\'{"tn":"*s"}\']//div[contains(@style, "background-image")]')

    # Duyệt qua từng thẻ div và lấy các văn bản trong thẻ span có style chứa chuỗi "background-image"
        
        all_text = ' '.join(span.text  for span in divs_with_style.find_elements(By.XPATH , './/span'))
    except Exception as e:
        all_text = ''
    return all_text
def find_link_share(driver):
    try:
        divs_with_table = driver.find_element(By.XPATH , '//div[@data-ft=\'{"tn":"H"}\'][.//table]')
        table_element = divs_with_table.find_element(By.XPATH , './/table')
        table_text = table_element.text
    except Exception as e:
        table_text = ''
    return table_text
        


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
    
    sleep(3)
    
    # Duyệt qua từng thẻ div và tìm các thẻ con có arial-label chứa các reaction như "Like", "Haha", ...
    reaction_Like = count_react(driver , "Like")
    reaction_Love = count_react(driver , "Love")
    reaction_Care = count_react(driver , "Care")
    reaction_Wow = count_react(driver , "Wow")
    reaction_Haha = count_react(driver , "Haha")
    reaction_Angry = count_react(driver , "Angry")
    reaction_Huhu = count_react(driver , "Huhu")
    reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
    sleep(3)
    driver.get(link)
    sleep(3)

    return reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu
def find_all_images(driver , link):
    xpath_img = '//div[@data-ft=\'{"tn":"H"}\']//a[starts-with(@href, \'/photo.php?\')]//img'
    img_elements = driver.find_elements(By.XPATH , xpath_img)
    xpath_href_img = '//div[@data-ft=\'{"tn":"H"}\']//a[starts-with(@href, \'/photo.php?\')]'
    href_img_elements = driver.find_elements(By.XPATH , xpath_href_img)
    # Lưu trữ các liên kết hình ảnh
    image_links = [img_element.get_attribute("src") for img_element in img_elements]
    image_links_a = [href_img_element.get_attribute("href") for href_img_element in href_img_elements]
    ids_hrefs = [re.search(r'fbid=(\d+)', link).group(1) for link in image_links_a if re.search(r'fbid=(\d+)', link)]
    start_meet_video = 0
    if len(image_links_a) >1:
        driver.get(image_links_a[len(image_links_a)-1])
        while(True):
            xpath_next = '//a[starts-with(@href, \'/photo.php?\') and normalize-space()="Next"]'
            next_element = driver.find_element(By.XPATH, xpath_next)
            next_link = next_element.get_attribute("href")

            if(start_meet_video != 0):
                next_link = 'Previous'
                
            try:
                id_match = re.search(r'fbid=(\d+)', next_link).group(1)
            except:
                try:
                    if(start_meet_video ==0):
                        driver.get(image_links_a[0])
                        start_meet_video = start_meet_video+1
                    xpath_next = '//a[starts-with(@href, \'/photo.php?\') and normalize-space()="Previous"]'
                    next_element = driver.find_element(By.XPATH, xpath_next)
                    next_link = next_element.get_attribute("href")
                    id_match = re.search(r'fbid=(\d+)', next_link).group(1)
                except:
                    break
            if id_match not in ids_hrefs:
                image_links_a.append(next_link)
                ids_hrefs.append(id_match)
                driver.get(next_link)
                sleep(0.5)
                img_element = driver.find_element(By.XPATH, '//div[@style="text-align:center;"]//img')

                image_links.append(img_element.get_attribute("src"))

            else:
                break
        sleep(1)
        driver.get(link)
        sleep(1)
    
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
link = 'https://mbasic.facebook.com/story.php?story_fbid=pfbid02CuqshZ112QWgWEPdCY9U1qm6NuaDgLnfstae4CtcvbojGeGZsYapkt9hGf1aAjPLl&id=100064656432658&eav=AfZaoQyQHRGedNCHuUmllkxPAEMOFeEQpT2Zh7T7y1G6ylRde1FQpCO75kFm1xgb0D8&__xts__%5B0%5D=12.Abrh5W-Jzwgz_mIxOV__tP7j73FiS4UU_uLN8Pn41ffbKgHwvdfmynCJz7B9O__Wv67puOkUc61epJ2PAnOWL8V_z66V1BCegF5_2ec9EztiiCngAWYuSRDBBBVIkGIxwjjIO_kuUqRmqpP9uA4lOnUQkjOr_biIRPGFAgJlQwDwTlDx_XJArAbFPOdWqbQfPxeGDLG9diZFvOnmcNp8Da-FLrdfchtXLSlyjocPCz731WqQ6P_YLQPUYyAMmb7lgkraKKciYrx9eb5IJl_B0n2XNhMFfSorj8rEKvHK_Y4Y3sTUkPnKc2aNsIkiumtLBPMdRiUipwE8bkhjtYGIZW7C2839jr_c7iUVR3K1okw3oe73yiESal7JECMc-1Aaav4q5QwArk7Hoh-A_O0-J9T4GmzMMI6LrDQBJjvbC-arFF9iPTyDonWR0m268tGu9wlS7g2s3FZIW0lLQ56cx7ga0JSgQltbt8e03eyrzmrSkkV6CqEKhAp9zxXT2SSLEL9o0qpmRpd1YX7fyXIf0YUn6XGGmtnGOp2VZfCb1rEur-G_MzWGz235WcmnnCUNfMcztdqOGMiGibO2Q4ZcBC90fuqZZHP71Yvbasqi6fa-E7i9k3xoonatqQx4z7yflNx3Shg4EoPeAwcFoZvLWzer6Cu54gY1LBpGt5p-Go4hFx78bKj9KqcSJg6ZboBxV00&__tn__=%2AW&paipv=0#footer_action_list'
driver.get(link)
sleep(2)
auth_link , auth_text = find_author(driver)
content = find_content(driver)+find_content_background(driver)
reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu = count_react_item(driver , link)
link_video = find_link_video(driver)
text_share = find_link_share(driver)
print(auth_link , auth_text)    
print(content)
print(text_share)
print(reaction_All)
print(reaction_Love)
print(reaction_Wow)
print(link_video)
# In kết quả
image_links = find_all_images(driver , link)
for image_link in image_links:
    print(image_link)