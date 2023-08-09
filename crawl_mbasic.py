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



chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
chrome_options.add_argument("--disable-notification")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}') 
driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)

driver.get('https://www.facebook.com/')
sleep(3)
cookies = pickle.load(open("my_cookie_2.pkl" , "rb"))
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
    xpath_img = '//div[@data-ft=\'{"tn":"H"}\']//a[contains(@href, \'photo\')]//img'    
    img_elements = driver.find_elements(By.XPATH , xpath_img)
    xpath_href_img = '//div[@data-ft=\'{"tn":"H"}\']//a[contains(@href, \'photo\')]'
    href_img_elements = driver.find_elements(By.XPATH , xpath_href_img)
    # Lưu trữ các liên kết hình ảnh
    image_links = [img_element.get_attribute("src") for img_element in img_elements]
    image_links_a = [href_img_element.get_attribute("href") for href_img_element in href_img_elements]
    ids_hrefs = [re.search(r'fbid=(\d+)', link).group(1) for\
        link in image_links_a if re.search(r'fbid=(\d+)', link)]
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
                sleep(2)
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
#comment


def extract_info_from_divs(div_comment_elements):
    auth_links = []
    auth_names = []
    div_texts = []
    for div_element in div_comment_elements:
        first_nested_div = div_element.find_element(By.XPATH, ".//div[1]")
        h3_element = first_nested_div.find_element(By.TAG_NAME, "h3")
        a_element = h3_element.find_element(By.TAG_NAME, "a")
        auth_links.append(a_element.get_attribute("href"))
        auth_names.append(a_element.text)
        adjacent_div = h3_element.find_element(By.XPATH, "following-sibling::div[1]")
        div_texts.append(adjacent_div.text)
    return auth_links, auth_names, div_texts

def crawl_comments(driver):
    auth_links_comments = []
    auth_names_comments = []
    comments = []
    
    div_prev_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
    div_more_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
    
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            div_comment_elements = driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
            auth_links, auth_names, div_texts = extract_info_from_divs(div_comment_elements)
            auth_links_comments.extend(auth_links)
            auth_names_comments.extend(auth_names)
            comments.extend(div_texts)

            if len(div_more_elements) - len(div_prev_elements) < 0:
                div_prev_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
                a_element = div_prev_elements[0].find_element(By.TAG_NAME, "a")
            elif len(div_more_elements) - len(div_prev_elements) > 0:
                div_more_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
                a_element = div_more_elements[0].find_element(By.TAG_NAME, "a")
            else:
                break

            link = a_element.get_attribute('href')
            sleep(1.5)
            driver.get(link)
            sleep(1.5)
        except Exception as e:
            print(e)
            break

    return auth_links_comments, auth_names_comments, comments

        
# for link in p_link:
link = 'https://mbasic.facebook.com/story.php?story_fbid=pfbid0JSA8NSBFCuspeMyu7sDPqcPQ7u54mvMiHVqh1zrsGzhhSRNnYhHoXqLRMaXbHE9Al&id=100008201472116&eav=AfagrhY_TtRM6p4oOt2uw30T6em7k41vxIv4to8CCNrzJL866oln_R3rxu6i-SIBkgY&refid=17&_ft_=qid.-3659520491964999945%3Amf_story_key.3590340067916007%3Atop_level_post_id.3590340067916007%3Atl_objid.3590340067916007%3Acontent_owner_id_new.100008201472116%3Athrowback_story_fbid.3590340067916007%3Aphoto_id.3590340044582676%3Astory_location.4%3Astory_attachment_style.photo%3Asty.22%3Aent_attachement_type.MediaAttachment%3Aprofile_id.100008201472116%3Aprofile_relationship_type.6%3Aactrs.100008201472116%3Athid.100008201472116%3A306061129499414%3A2%3A1688733425%3A1688733425%3A1087282784837977145%3A%3A3590340067916007%3Aftmd_400706.111111l&__tn__=%2AW-R&paipv=0#footer_action_list'
driver.get(link)
sleep(2)
# auth_link , auth_text = find_author(driver)
# content = find_content(driver)+find_content_background(driver)
# reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu = count_react_item(driver , link)
# link_video = find_link_video(driver)
# link_share , text_share = find_link_share(driver)
# content_share = find_content_share(driver)
# time_text = find_time(driver)
# time_process  , _= getCreatedTime(time_text)
# print('auth_link: ' , auth_link)
# print('auth_text: ' ,  auth_text)    
# print('content: ' ,content)
# print('link_share: ' , link_share)
# print('auth_share: ' , text_share)
# print('content_share: ' , content_share)
# print('all_react: ' , reaction_All)
# print('react_love: ' , reaction_Love)
# print('react_wow: ' , reaction_Wow)
# print('link_video: ' , link_video)
# print('time_post: ' , time_process)
# # In kết quả
# image_links = find_all_images(driver , link)
# print('image_links: ' )
# for image_link in image_links:
#     print(image_link)
auth_links_comments ,auth_names_comments ,  comments = crawl_comments(driver)
print('comments: ' , comments)
