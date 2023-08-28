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
from datetime import datetime, timedelta, date
import time
from time import gmtime, strftime
import calendar
import os
import csv
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

latestchromedriver = ChromeDriverManager().install()

from post import Post

new_post = Post()
comment_post = Post()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notification")
# chrome_options.add_argument("--incognito")
# chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);

# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
# chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled') 
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument("--start-maximized")
# options.add_argument('--disable-infobars')
# options.add_argument('--disable-notifications')
# options.add_argument('--disable-popup-blocking')
# options.add_argument('--disable-save-password-bubble')
# options.add_argument('--disable-translate')
# options.add_argument('--disable-web-security')
# options.add_argument('--disable-extensions')
driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver-win64\\chromedriver.exe" , options=chrome_options)
link_get_story = 0
# driver = uc.Chrome(driver_executable_path=latestchromedriver , options = chrome_options)



def logout(driver):
    driver.get('https://mbasic.facebook.com/home.php?')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    xpath_expression = "//a[contains(text(), 'Logout')]"
    logout_button = driver.find_element(By.XPATH , xpath_expression)
    sleep(3)
    # Thực hiện các hành động trên thẻ (ví dụ: nhấp chuột để đăng xuất)
    logout_button.click()
    try:
        sleep(3)
        value_contain = "Don't save"

        # Tìm phần tử <input> dựa trên giá trị thuộc tính 'value' chứa chuỗi
        xpath_expression = f"//input[contains(@value, \"{value_contain}\") and @type='submit']"
        input_element = driver.find_element(By.XPATH, xpath_expression)
        sleep(3)
        # Thực hiện hành động nhấp chuột vào phần tử
        input_element.click()
    except:
        pass
def login(driver):
    driver.get('https://www.facebook.com//')

    txtUser = driver.find_element(By.ID , "email")
    txtUser.send_keys('lee_tai12@yahoo.com.vn')
    sleep(2)    
    txtPassword = driver.find_element(By.ID , "pass")
    txtPassword.send_keys('thanhnam4321')
    sleep(2)
    txtPassword.send_keys(Keys.ENTER)
    sleep(10)

# driver = uc.Chrome(options = chrome_options)
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
        link_share_element = divs_with_table.find_element(By.TAG_NAME , 'a')
        link_share = link_share_element.get_attribute('href')
        table_element = divs_with_table.find_element(By.XPATH , './/table')
        table_text = table_element.text
    except Exception as e:
        table_text = ''
        link_share = ''
    return link_share , table_text
        
def find_content_share(driver):
    try:
        outer_div = driver.find_elements(By.XPATH, '//div[@data-ft=\'{"tn":"H"}\']')
        inner_div_s = outer_div[0].find_element(By.XPATH, './/div[@data-ft=\'{"tn":"*s"}\']')
        p_elements = inner_div_s.find_elements(By.TAG_NAME, 'p')
        texts = [elem.text for elem in p_elements]

        # Gộp tất cả các dòng text thành một văn bản
        full_text = ' '.join(texts)
    except:
        full_text = ''
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

def count_react_item(driver):
    reaction_All = reaction_Like = reaction_Love = reaction_Care = reaction_Wow = reaction_Haha = reaction_Angry = reaction_Huhu = 0
    try:
        link_element = driver.find_element(By.XPATH, '//div[contains(@id, "sentence_")]//a[contains(@href, "/ufi/reaction/profile/")]')

    # Lấy giá trị href từ thẻ a
        link_href = link_element.get_attribute('href')
        
        sleep(random.uniform(2.25, 5.5) )
        # driver.get(link_href)
        link_element.click()
        sleep(random.uniform(2.25, 5.5) )
        
        # Duyệt qua từng thẻ div và tìm các thẻ con có arial-label chứa các reaction như "Like", "Haha", ...
        reaction_Like = count_react(driver , "Like")
        reaction_Love = count_react(driver , "Love")
        reaction_Care = count_react(driver , "Care")
        reaction_Wow = count_react(driver , "Wow")
        reaction_Haha = count_react(driver , "Haha")
        reaction_Angry = count_react(driver , "Angry")
        reaction_Huhu = count_react(driver , "Sad")
        reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
        sleep(random.uniform(2.25, 5.5) )
        driver.back()
    except Exception as e:
        print(e)
        pass
    # sleep(random.uniform(2.25, 5.5) )
    

    return reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu
def find_all_images(driver , link):
    xpath_img = '//div[@data-ft=\'{"tn":"H"}\']//a[contains(@href, \'photo\')]//img'    
    img_elements = driver.find_elements(By.XPATH , xpath_img)
    xpath_href_img = '//div[@data-ft=\'{"tn":"H"}\']//a[contains(@href, \'photo\')]'
    href_img_elements = driver.find_elements(By.XPATH , xpath_href_img)
    # Lưu trữ các liên kết hình ảnh
    image_links = [img_element.get_attribute("src") for img_element in img_elements]
    image_links_a = [href_img_element.get_attribute("href") for href_img_element in href_img_elements]
    ids_hrefs = [re.search(r'fbid=(\d+)', link).group(1) for link in image_links_a if re.search(r'fbid=(\d+)', link)]
    start_meet_video = 0
    if len(image_links_a) >1:
        driver.get(image_links_a[len(image_links_a)-1])
        abbr_element  = driver.find_elements(By.XPATH, '//div[@data-ft=\'{"tn":",g"}\']//abbr')
        time_image = abbr_element[0].text

        while(True):
            xpath_next = '//a[starts-with(@href, \'/photo.php?\') and normalize-space()="Next"]'
            next_element = driver.find_elements(By.XPATH, xpath_next)
            next_link = next_element[0].get_attribute("href")

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
                sleep(random.uniform(2.25, 5.5) )

                driver.get(next_link)
                sleep(random.uniform(2.25, 5.5) )
                abbr_element_next  = driver.find_element(By.XPATH, '//div[@data-ft=\'{"tn":",g"}\']//abbr')
        # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
                time_image_next = abbr_element_next.text
                if time_image_next!=time_image:
                    break
                img_element = driver.find_element(By.XPATH, '//div[@style="text-align:center;"]//img')

                image_links.append(img_element.get_attribute("src"))

            else:
                break
        sleep(random.uniform(2.25, 5.5) )
        driver.get(link)
        sleep(random.uniform(2.25, 5.5) )
    
    return image_links
def find_link_video(driver):
    video_link = "no video"
    try:
        outer_div = driver.find_elements(By.XPATH, '//div[@data-ft=\'{"tn":"H"}\']')

        element = outer_div[0].find_element(By.XPATH , "//a[starts-with(@href, '/video_redirect/')]")
        video_link = element.get_attribute("href")
    except Exception as e:
        pass
    return video_link

def find_time(driver):
    try:
        abbr_element  = driver.find_element(By.XPATH, '//footer[@data-ft=\'{"tn":"*W"}\']//abbr')
        # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
        time_text = abbr_element.text

        # Gộp tất cả các dòng text thành một văn bả
    except Exception as e:
        time_text = ''
    return time_text


#time process 
def GetOldTime(distance_milis_time):
    time_now = strftime("%m/%d/%Y %H:%M:%S", gmtime())
    timestamp_now = calendar.timegm(
        time.strptime(time_now, "%m/%d/%Y %H:%M:%S"))
    dt_object = datetime.fromtimestamp(timestamp_now - distance_milis_time)
    return dt_object.strftime("%m/%d/%Y %H:%M:%S")


def normalizationDateTime(text):
    if(text.find("January") != -1):
        text = text.replace("January", "Jan")
    if(text.find("February") != -1):
        text = text.replace("February", "Feb")
    if(text.find("") != -1):
        text = text.replace("March", "Mar")
    if(text.find("April") != -1):
        text = text.replace("April", "Apr")
    if(text.find("May") != -1):
        text = text.replace("May", "May")
    if(text.find("June") != -1):
        text = text.replace("June", "Jun")
    if(text.find("July") != -1):
        text = text.replace("July", "Jul")
    if(text.find("August") != -1):
        text = text.replace("August", "Aug")
    if(text.find("September") != -1):
        text = text.replace("September", "Sep")
    if(text.find("October") != -1):
        text = text.replace("October", "Oct")
    if(text.find("November") != -1):
        text = text.replace("November", "Nov")
    if(text.find("December") != -1):
        text = text.replace("December", "Dec")
    if len(text) <= 3:
        text = text.replace("m", " min")
        text = text.replace("h", " hour")
        text = text.replace("d", " day")
    return text


def getCreatedTime(text):
    # x hrs | x mins | hr | min | h | m
    # August 13, 2018 at 3:24 PM | August 13 at 12:23 AM | February 14, 2017 at 12:35 PM
    # July 27, 2018 at 1:19 AM  | October 24, 2016 at 12:39 PM | 9 hrs · Public
    # August 15 at 11:35 PM · Public | Yesterday at 8:39 AM · Public | August 15 · Public
    # 4 minutes ago | Just now |x hrs | x mins | hr | min
    text = normalizationDateTime(text)
    time_now = GetOldTime(0)
    dateTimeNow = datetime.now()
    # July 10
    if text.find("at") == -1 and text.find("hour") == -1 and text.find("hr") == -1 and text.find("min") == -1 and text.find("Just now") == -1 and text.find("day") == -1:
        month = '00'
        if(text.find("Jan") != -1):
            month = '01'
        if(text.find("Feb") != -1):
            month = '02'
        if(text.find("Mar") != -1):
            month = '03'
        if(text.find("Apr") != -1):
            month = '04'
        if(text.find("May") != -1):
            month = '05'
        if(text.find("Jun") != -1):
            month = '06'
        if(text.find("Jul") != -1):
            month = '07'
        if(text.find("Aug") != -1):
            month = '08'
        if(text.find("Sep") != -1):
            month = '09'
        if(text.find("Oct") != -1):
            month = '10'
        if(text.find("Nov") != -1):
            month = '11'
        if(text.find("Dec") != -1):
            month = '12'
        #
        if month != '00':
            day = text.split(" ")[1]
            if day.isdecimal():
                if int(day) <= 9:
                    day = '0' + day
                #
                created_time = month + "/" + day + \
                    "/2023 " + strftime("%H:%M:%S", gmtime())
                return created_time, 30
    if(text.find("Just now") != -1):
        created_time = time_now
        return created_time, 0
    if(text.find("min") != -1):
        minutes = text.split(" min")[0]
        if(minutes.isdecimal()):
            created_time = GetOldTime(60 * int(minutes))
            return created_time, 0
        else:
            return time_now, 0
    if(text.find("hr") != -1):
        hr = text.split(" hr")[0]
        if(hr.isdecimal()):
            created_time = GetOldTime(60 * 60 * int(hr))
            return created_time, 0
        else:
            return time_now, 0
    if(text.find("hour") != -1):
        hr = text.split(" hour")[0]
        if(hr.isdecimal()):
            created_time = GetOldTime(60 * 60 * int(hr))
            return created_time, 0
        else:
            return time_now, 0
    if(text.find("day") != -1):
        day = text.split(" day")[0]
        if(day.isdecimal()):
            created_time = GetOldTime(60 * 60 * 24 * int(day))
            return created_time, int(day)
        else:
            return time_now, 0
    # Yesterday at 8:39 AM
    if(text.find("Yesterday") != -1 and text.find("at") != -1):
        hr = text.split("at ")[1].split(":")[0]
        mins = text.split("at ")[1].split(":")[1].split(" ")[0]
        if text.find("PM") != -1:
            hr = int(hr) + 12
            hr = str(hr)
        if int(hr) <= 9:
            hr = "0" + hr
        #
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        created_time = f'{yesterday:%m/%d/%Y}'
        created_time += " " + hr + ":" + mins + ":01"
        return created_time, 1
     # Today at 8:39 AM
    if(text.find("Today") != -1 and text.find("at") != -1):
        hr = text.split("at ")[1].split(":")[0]
        mins = text.split("at ")[1].split(":")[1].split(" ")[0]
        if text.find("PM") != -1:
            hr = int(hr) + 11
            hr = str(hr)
        if int(hr) <= 9:
            hr = "0" + hr
        #
        now = datetime.now()
        created_time = f'{now:%m/%d/%Y}'
        created_time += " " + hr + ":" + mins + ":01"
        return created_time, 1
     # Saturday at 8:39 AM
    if(text.find("at") != -1):
        if(text.find("Mon") != -1 or text.find("Tue") != -1 or text.find("Wed") != -1 or text.find("Thu") != -1 or text.find("Fri") != -1 or text.find("Sat") != -1 or text.find("Sun") != -1):
            hr = text.split("at ")[1].split(":")[0]
            mins = text.split("at ")[1].split(":")[1].split(" ")[0]
            if text.find("PM") != -1:
                hr = int(hr) + 11
                hr = str(hr)
            if int(hr) <= 9:
                hr = "0" + hr
            #
            now = datetime.now()
            yesterday = now - timedelta(days=4)
            created_time = f'{yesterday:%m/%d/%Y}'
            created_time += " " + hr + ":" + mins + ":01"
            return created_time, 3
    # July 27, 2018 at 1:19 AM | July 27 at 1:19 AM
    if ((text.find("AM") != -1 or text.find("PM") != -1) and text.find("at") != -1):
        if text.find(",") != -1:
            date = text.split(' ')[1].split(',')[0]
            year = text.split(' ')[2]
        else:
            date = text.split(' ')[1].split(' ')[0]
            year = '2023'
        #
        month = '01'
        if(text.find("Jan") != -1):
            month = '01'
        if(text.find("Feb") != -1):
            month = '02'
        if(text.find("Mar") != -1):
            month = '03'
        if(text.find("Apr") != -1):
            month = '04'
        if(text.find("May") != -1):
            month = '05'
        if(text.find("Jun") != -1):
            month = '06'
        if(text.find("Jul") != -1):
            month = '07'
        if(text.find("Aug") != -1):
            month = '08'
        if(text.find("Sep") != -1):
            month = '09'
        if(text.find("Oct") != -1):
            month = '10'
        if(text.find("Nov") != -1):
            month = '11'
        if(text.find("Dec") != -1):
            month = '12'
        #
        if text.find("at") != -1:
            hr = text.split("at ")[1].split(":")[0]
            mins = text.split("at ")[1].split(":")[1].split(" ")[0]
            if text.find("PM") != -1:
                hr = int(hr) + 11
                hr = str(hr)
            if int(hr) <= 9:
                hr = "0" + hr
            if int(date) <= 9:
                date = "0" + date
            created_time = month + "/" + date + "/" + year + " " + hr + ":" + mins + ":01"
            dateTimePost = datetime.strptime(
                created_time, "%m/%d/%Y %H:%M:%S")
            dateTimeDifference = dateTimeNow - dateTimePost
            distance_time = dateTimeDifference.total_seconds() / (3600 * 24)
            return created_time, distance_time
        else:
            if int(month) <= 9:
                month = "0" + month
            if int(date) <= 9:
                date = "0" + date
            created_time = month + "/" + date + "/" + year + " " + "09:43:23"
            dateTimePost = datetime.strptime(
                created_time, "%m/%d/%Y %H:%M:%S")
            dateTimeDifference = dateTimeNow - dateTimePost
            distance_time = dateTimeDifference.total_seconds() / (3600 * 24)
            return created_time, distance_time
    # July 27, 2018
    if text.find(",") != -1:
        date = text.split(' ')[1].split(',')[0]
        year = text.split(' ')[2]
        #
        month = '01'
        if(text.find("Jan") != -1):
            month = '01'
        if(text.find("Feb") != -1):
            month = '02'
        if(text.find("Mar") != -1):
            month = '03'
        if(text.find("Apr") != -1):
            month = '04'
        if(text.find("May") != -1):
            month = '05'
        if(text.find("Jun") != -1):
            month = '06'
        if(text.find("Jul") != -1):
            month = '07'
        if(text.find("Aug") != -1):
            month = '08'
        if(text.find("Sep") != -1):
            month = '09'
        if(text.find("Oct") != -1):
            month = '10'
        if(text.find("Nov") != -1):
            month = '11'
        if(text.find("Dec") != -1):
            month = '12'
        if int(month) <= 9 and len(month) == 1:
            month = "0" + month
        if int(date) <= 9 and len(date) == 1:
            date = "0" + date
        created_time = month + "/" + date + "/" + year + " " + "09:43:23"
        dateTimePost = datetime.strptime(created_time, "%m/%d/%Y %H:%M:%S")
        dateTimeDifference = dateTimeNow - dateTimePost
        distance_time = dateTimeDifference.total_seconds() / (3600 * 24)
        return created_time, distance_time
    return time_now, 0




def get_data_from_comment(driver , comment_element):
        comment_post = Post()
        comment_id = comment_element.get_attribute("id")
        comment_post.id = comment_id
        
        first_nested_div = comment_element.find_element(By.XPATH, ".//div[1]")
        h3_element = first_nested_div.find_element(By.TAG_NAME, "h3")
        a_element = h3_element.find_element(By.TAG_NAME, "a")
        comment_post.author_link = a_element.get_attribute("href")
        comment_post.author = a_element.text
        
        adjacent_div = h3_element.find_element(By.XPATH, "following-sibling::div[1]")
        comment_post.content = adjacent_div.text
        time_element = comment_element.find_element(By.TAG_NAME, "abbr")
        time_text = time_element.text
        time_process  , _= getCreatedTime(time_text)
        comment_post.created_time = time_process
        
        try:
            xpath_img = f"//div[@id='{comment_id}']//a[contains(@href, 'photo')]//img"

                
            img_element = driver.find_element(By.XPATH , xpath_img)
            img_link = img_element.get_attribute('src')
            comment_post.image_url = img_link
        except Exception as e:
            comment_post.image_url = ''
        
        try:  
            
            video_element = driver.find_element(By.XPATH , f"//div[@id='{comment_id}']//a[starts-with(@href, '/video_redirect/')]")
            video_href  = video_element.get_attribute('href')
            comment_post.video = video_href
        except Exception as e:
            comment_post.video = ''
        try: 
            link_element = comment_element.find_element(By.XPATH  , f"//span[contains(@id, 'like') and contains(@id, '_{comment_id}')]//a[contains(@href, '/ufi/reaction/profile/')]")  
            link_href = link_element.get_attribute('href')
            
            sleep(random.uniform(2.25, 5.5) )
    # driver.get(link_href)
            driver.get(link_href)
            # link_element.click()
            
            sleep(random.uniform(2.25, 5.5) )
            
            reaction_Like = count_react(driver , "Like")
            reaction_Love = count_react(driver , "Love")
            reaction_Care = count_react(driver , "Care")
            reaction_Wow = count_react(driver , "Wow")
            reaction_Haha = count_react(driver , "Haha")
            reaction_Angry = count_react(driver , "Angry")
            reaction_Huhu = count_react(driver , "Sad")
            reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
            comment_post.like = reaction_Like
            comment_post.love = reaction_Love
            comment_post.wow = reaction_Wow
            comment_post.haha = reaction_Haha
            comment_post.angry = reaction_Angry
            comment_post.sad = reaction_Huhu
            driver.back()
        except Exception as e:
            comment_post.like = 0
            comment_post.love = 0
            comment_post.wow = 0
            comment_post.haha = 0
            comment_post.angry = 0
            comment_post.sad = 0
        return comment_post

def extract_info_from_divs(driver):
    comments = {}
    div_comment_elements = driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
    for i in range(0 ,len(div_comment_elements)):
        try:
            comment_post = Post()

            comment_post = get_data_from_comment(driver , div_comment_elements[i])
            comments[comment_post.id] = comment_post
            div_comment_elements = driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
            try:
                xpath_rep =f"//div[contains(@id, 'comment_replies_more') and contains(@id, '_{comment_post.id}')]//a[starts-with(@href, '/comment/replies/')]"
                # xpath_rep = "//a[starts-with(@href, '/comment/replies/')]"
                rep_element =  div_comment_elements[i].find_element(By.XPATH , xpath_rep)
                rep_href = rep_element.get_attribute("href")
                driver.get(rep_href)
                div_comment_reps = driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
                for i in range(1 ,len(div_comment_reps)):
                    comment_post_rep = get_data_from_comment(driver , div_comment_reps[i])
                    comments[comment_post_rep.id] = comment_post_rep
                    div_comment_reps = driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
                driver.back()
                div_comment_elements = driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
            except Exception as e:
                print(e)
                pass
           
        except Exception as e:
            print(e)
            pass
    return comments
def crawl_comments(driver ):
    global link_get_story
    comments = {}    
    div_prev_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
    div_more_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
    link_count = 1
    while len(comments)<=100:
        try:
            # for i in range(3):
            #     scroll_delay = random.uniform(1.5, 3.5)  # Tạo thời gian ngẫu nhiên trong khoảng từ 1.5 đến 3.5 giây
            #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     sleep(scroll_delay)

            #     scroll_delay = random.uniform(1.5, 3.5)  # Tạo thời gian ngẫu nhiên trong khoảng từ 1.5 đến 3.5 giây
            #     driver.execute_script("window.scrollTo(0, 0);")
            #     sleep(scroll_delay)

            #     scroll_delay = random.uniform(1.5, 3.5)  # Tạo thời gian ngẫu nhiên trong khoảng từ 1.5 đến 3.5 giây
            #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     sleep(scroll_delay)
            comment_per_page = extract_info_from_divs(driver)
            comments.update(comment_per_page)
            print(len(comments)) 
            print(comments) 
            
            if len(div_more_elements) - len(div_prev_elements) < 0:
                div_prev_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
                a_element = div_prev_elements[0].find_element(By.TAG_NAME, "a")
            elif len(div_more_elements) - len(div_prev_elements) > 0:
                div_more_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
                a_element = div_more_elements[0].find_element(By.TAG_NAME, "a")
            else:
                break
            driver.execute_script("arguments[0].scrollIntoView();", a_element)

            link = a_element.get_attribute('href')
            sleep(random.uniform(2.25, 5.5) )
            a_element.click()
            link_get_story +=1  
            print('link_get_story = ' , link_get_story)
            # driver = fake(driver , link_get_story ,link)
            

            # fake(driver , link_count , link)
        except Exception as e:
            print(e)
            break

    return  comments 

# driver.get('https://www.facebook.com//')

# txtUser = driver.find_element(By.ID , "email")
# txtUser.send_keys('yco17417@omeie.com')
# # txtUser.send_keys('qms42009@zbock.com')

# sleep(2)    
# txtPassword = driver.find_element(By.ID , "pass")
# txtPassword.send_keys('thanhnam4321')
# sleep(2)
# txtPassword.send_keys(Keys.ENTER)
# sleep(10)
# pickle.dump(driver.get_cookies() , open("my_cookie_3.pkl" , "wb"))

# driver.get('https://mbasic.facebook.com/search/posts?q=b%E1%BA%A1o%20l%E1%BB%B1c&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D')

def extract_id(link):
    try:
        id_match = re.search(r'story_fbid=([^&]+)', link)
        if id_match:
            id_value = id_match.group(1)
        else:
            group_id_match = re.search(r'/groups/(\d+)/', link)
            if group_id_match:
                id_value = group_id_match.group(1)
            else:
                id_value = None
    except Exception as e:
        print(f"Error: {e}")
    return id_value
# def get_data_from_link(driver , link , number_comment):
#         link_count = 0
#         unique_key = link
#         if unique_key not in data:
#             sleep(random.uniform(2.25, 5.5) )
#             link_count +=1
#             print(link_count)
#             # fake(driver , link_count , link)

#             sleep(random.uniform(2.25, 5.5) )
#             auth_link , auth_text = find_author(driver)
#             content = find_content(driver)+find_content_background(driver)
#             reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu = count_react_item(driver)
#             link_video = find_link_video(driver)
#             link_author_share , text_share = find_link_share(driver)
#             content_share = find_content_share(driver)
#             time_text = find_time(driver)
#             time_process  , _= getCreatedTime(time_text)
#             # In kết quả
#             image_links = find_all_images(driver , link)
#             auth_links_comments ,auth_names_comments ,  comments  = crawl_comments(driver)
#             data_line = {"Link_post": link, 
#                             "author":{ 'author_link': auth_link ,  
#                                     'auth_name': auth_text
#                                 } 
#                         ,"time":time_process , "content": content , 
#                         "share_post":{
#                             'link_author_share: ' : link_author_share ,
#                             'author_share: ' : text_share ,
#                             'content_share: ' : content_share,
                            
#                         } ,
#                         "video_only": link_video , 
#                         "image_post_list":   image_links ,
                    
#                         "number_reaction": {"Like": reaction_Like, "Love": reaction_Love , 
#                                     "Care": reaction_Care , "Wow": reaction_Wow , 
#                                     "Haha": reaction_Haha , "Angry": reaction_Angry,
#                                     "Huhu": reaction_Huhu,
#                                     "All_react": reaction_All , 
#                             },
#                         "comment":{
#                             "number_of_comments":number_comment , 
#                             "account_links_comment": auth_links_comments,
#                             "name_comment_list" : auth_names_comments ,
#                             "comment_list": comments  , 
#                         } }

#             # crawl commen
        
#             data[unique_key] = data_line
#             print(f"Đã thêm mới phần tử với key: {unique_key}")
#             print(json.dumps(data_line, ensure_ascii=False, indent=4))
#         else:
#             print(f"Phần tử với key: {unique_key} đã tồn tại!")

            
#         with open('data_new.json', 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)
#             f.write('\n')

# if os.path.exists('data_new.json'):
#     if os.path.getsize('data_new.json') == 0:
#         data = {}
#     else:
#         with open('data_new.json', 'r', encoding='utf-8') as f:
#             data = json.load(f)
# else:
#     data = {}
# def fake(driver , link_get , link):
#     new_driver = driver
#     if(link_get%82==0):
#         logout(driver)
#         driver.quit()
#         print("đang thực hiện fake lần :" ,(link_get % 82) + 1)
#         sleep(random.uniform(5400.5, 7200.7) )
#         new_driver  = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver-win64\\chromedriver.exe" , options=chrome_options)
#         login(new_driver )
#         sleep(5)
#         new_driver.get(link)
#     return new_driver

# see_more_href = 'https://mbasic.facebook.com/groups/1212236082236816?bacr=1692714416%3A6360204930773213%3A6360204930773213%2C0%2C4%3A7%3AKw%3D%3D&multi_permalinks&eav=Afbyu4hHkDQxvvhYL4t7oDwNyDCf3uUtITndD4wAZ310hpeFOdiESdlNrbQDNINfXYM&paipv=0&refid=18'
# login(driver)
# driver.get(see_more_href)
# sleep(2)
# while True:

#     try:
#         div_elements = driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')

#         full_story_links = []
#         number_comments = []
        
#         for i in range(0 ,len(div_elements)+1):
#             try:
#                 driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", div_elements[i+1])
#                 full_story_element = div_elements[i+1].find_element(By.XPATH, ".//a[text()='Full Story']")
#                 driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", full_story_element)
#                 full_story_link = full_story_element.get_attribute('href')
#                 try:
#                     comment_element = div_elements[i+1].find_element(By.XPATH, ".//a[contains(text(),'Comment')]")
#                     comment_text = comment_element.get_attribute('text')
#                     comment_number = re.search(r'(\d+(?:,\d+)?)\s+Comment', comment_text).group(1)

#                 except Exception as e:
#                     comment_number = 0

#                 sleep(random.uniform(2.25, 3) )
#                 full_story_element.click()
#                 link_get_story = link_get_story+ 1 
#                 print('link_get_story = ' , link_get_story)
#                 # driver = fake(driver , link_get_story , full_story_link)
#                 sleep(random.uniform(3.5, 5.5) )
#                 print("Adding new link to list:", full_story_link)
                
#                 get_data_from_link(driver , full_story_link , comment_number)
#                 sleep(random.uniform(3,4.5) )
#                 driver.get(see_more_href)

#                 div_elements = driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')

#             except Exception as e:
#                 pass
                
#         sleep(random.uniform(2.25, 5.5) )
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         see_more_link = driver.find_element(By.XPATH, '//a[span[text()="See more posts"]]')
#         see_more_href = see_more_link.get_attribute("href")

#         sleep(random.uniform(2.25, 5.5) )
#         driver.get(see_more_href)
#         sleep(random.uniform(2.25, 5.5) )

#         # Tiếp tục xử lý và ghi dữ liệu vào file CSV nếu cần

#     except Exception as e:
#         print(e)
#         break
# *Command to open Chrome Browser as debugger Browser*
# chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\chromedriver_win32\data 
# full_story_link = 'https://mbasic.facebook.com/groups/mixigaming/permalink/4252769561516771/?refid=18&_ft_=encrypted_tracking_data.0AY-UV7zEpipBYNPw8MvFKp4rTHnZwNTatx5J0QUDVj28mM-pch0fmP2bit4Ak9uDjihkI8K3uEty0mbpyJGD5VxShwzXOn16wckOc01r4fAJNr5D1YXsKiU_tmmA9SLv_lZcLKtThp3v-sU4AmF6zZn_Tl4-ZL1Y2bjVOoXh_0Kh02wkpI5f0Y62md90X45FwPF0jRSWaRN2Q_Uymtrj2dq6Pf93cwNvLDUpjmEGoFiXRRIjCPYgq6kf1ACLdEUCNyY0Tkox_yUsyPXLCbBJ96C_qjqerANXToSCFJdCHju7j30HfZudKeYShaBQsMsrzyrtYZJSVLecKlqlpTWIvlty38Mt6mxB4rXXIZeer85uYXIghs1SoaB0kFaMtL5MoxoGXlS7Boez7M-RNDmRKx7bvuvRV8Qvn0AwQr1hrUG4SJScuFbgkFLn1jeNVi-8kxD_f-AybtQiJtF0etubkFw2qnhrOZN_z6w9kXPHy3cS1i8UVqhi1j5zPH-_Jl9lR17L5KS7OEsU_C7C6O3tIRQDY5tq4EYE7KiIT1LOEP2VqipQu55kM0J3b3Ntb2hH-f03WB1sL4i2Yuc61MdwdjXMAU9cqcDez9KjAFKEO3B2h_-Entlbk8awzwV3PT2RqmKqAHntwtFhMsDa0Xwn7LtgRoQjVYd2jReqI86A4FKvXS8uEX-WBsEeYFtk2UrcgDH7K0FdkbtP60i9jAnSnn2GPaOlvXTImOyX_Lxh2BVyoZmn6J7EU5dARs4dG_11Q7EaH_9U7YnZXxLrF-CpFRFYYfJ5uLVyqqv-O2s1hLhXv-kOnsZ75iWdonEVBUz9NTigK70AXUdDQ5yw8wYfFfWfE7ajELTcTIVJbFu4bgs79LGM7G-1OSK_ayDsfw1wFPLtOBat83mpjy5pGBzG5j7yh513h3J1m82vBkG0u0fxDBepptqlAd5RDk7wTKjhkbbxTSk0vFK7oBzpSXzv_topzUd-bq02YnJJsRpVnQfxwQPqb3LJa7gPIVYw2jsLU5j1bdpOgCspUVh2IzUEdwNqy7NgdWGaKusIfEpEP4oiWtZtNCKqu8BCoy9-QE2WMFHCCtR-nQ1FunJ-2ocQl0XFeJI0NPjYu6uPilDLcEd2PerWtejXxZBdXSK1rFBUfd_JAFghI18vdA&__tn__=%2AW-R&paipv=0&eav=AfZTzgyyZMk4FLKBeTeG-ATBuXyXyJ-TRhTSh5Yl8dc4ECPFGPBqw63IfaQ_F-vV_1w#footer_action_list'
# get_data_from_link(driver , full_story_link , 15)
comments  = crawl_comments(driver)
print(comments)
