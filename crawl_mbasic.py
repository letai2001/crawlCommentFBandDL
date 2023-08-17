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

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notification")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')

def login(driver):
    driver.get('https://www.facebook.com//')

    txtUser = driver.find_element(By.ID , "email")
    txtUser.send_keys('wasantha.lifel.o.gy@gmail.com')
    sleep(2)    
    txtPassword = driver.find_element(By.ID , "pass")
    txtPassword.send_keys('thanhnam4321')
    sleep(2)
    txtPassword.send_keys(Keys.ENTER)
    sleep(10)
def logout(driver):
    driver.get('https://mbasic.facebook.com/')
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
def fake(driver , link_count , link):
    if(link_count % 4 == 0 or link_count % 9 == 0 ) and link_count != 0:
        comment_strings = ["Hài", "Ngu nó vừa thôi", "Chả ra cái gì", "Đừng chặn bố nữa dcm mấy thằng chúng m" , "web như cc bày đặt chặn" , "hài hước vl" ]
        for i in range(random.randint(1, 3)):
            random_comment = random.choice(comment_strings)
            xpath_expression = "//textarea[@id='composerInput' and @name='comment_text']"
            try:
                textarea_element = driver.find_element(By.XPATH , xpath_expression)
                driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", textarea_element)

                textarea_element.send_keys(random_comment)
                xpath_expression = "//input[@value='Comment' and @type='submit']"
                comment_button = driver.find_element(By.XPATH , xpath_expression)

                # Thực hiện click vào nút Comment
                comment_button.click()
            except Exception as e:
                sleep(10)
                pass

    if (link_count % 3 == 0 or link_count % 5 == 0 ) and link_count != 0:
        sleep(random.uniform(20.5, 50.3))
        xpath_home = "//a[contains(@href, 'home')]"
        home_element = driver.find_element(By.XPATH , xpath_home)
        href_home = home_element.get_attribute("href")
        driver.get(href_home)
        sleep(6)
        logout(driver)
        
        sleep(random.uniform(20.5, 34.3))
        login(driver)
        sleep(6)
        driver.get(link)
        
        sleep(10)


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
def get_link(driver , link , csv_filename):
    sleep(1.75)
    driver.get(link)
    sleep(2)
    if not os.path.exists(csv_filename) or os.path.getsize(csv_filename) == 0:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Full_Story_Links", "Number_comments"])
    existing_links = set()
                # Đọc nội dung hiện tại của file CSV để xác định những link đã ghi vào trước đó
    if os.path.isfile(csv_filename):
        with open(csv_filename, mode="r", newline="", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Đọc tiêu đề cột
            if header != ["Full_Story_Links", "Number_comments"]:
                # Thêm tiêu đề cột nếu không tồn tại
                with open(csv_filename, mode="w", newline="", encoding="utf-8") as new_csv_file:
                    csv_writer = csv.writer(new_csv_file)
                    csv_writer.writerow(["Full_Story_Links", "Number_comments"])
            else:
                for row in csv_reader:
                        link_row = row[0] 
                        # Truy cập cột "Full_Story_Links" (cột thứ 0)
                        existing_links.add(extract_id(link_row))

    while True:
        try:
            div_elements = driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')
            full_story_links = []
            number_comments = []


            for div in div_elements:
                full_story_element = div.find_element(By.XPATH, ".//a[text()='Full Story']")
                full_story_link = full_story_element.get_attribute('href')
                
                if extract_id(full_story_link) not in existing_links:  # Kiểm tra xem link đã tồn tại hay chưa
                    print("Adding new link to list:", full_story_link)
                    full_story_links.append(full_story_link)
                    existing_links.add(extract_id(full_story_link))
                    try:
                        comment_element = div.find_element(By.XPATH, ".//a[contains(text(),'Comment')]")
                        comment_text = comment_element.get_attribute('text')
                        comment_number = re.search(r'(\d+(?:,\d+)?)\s+Comment', comment_text).group(1)

                    except Exception as e:
                        comment_number = 0
                    number_comments.append(comment_number)

            # Ghi dữ liệu vào file CSV chỉ cho những link mới
            with open(csv_filename, mode="a" if os.path.exists(csv_filename) else "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                for link, comment_number in zip(full_story_links, number_comments):
                    csv_writer.writerow([link, comment_number])

            # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
            sleep(random.uniform(2.25, 5.5) )
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            see_more_link = driver.find_element(By.XPATH, "//div[contains(@id, 'see_more')]//a")
            see_more_href = see_more_link.get_attribute("href")
            sleep(random.uniform(2.25, 5.5) )
            driver.get(see_more_href)
            sleep(random.uniform(2.25, 5.5) )

            # Tiếp tục xử lý và ghi dữ liệu vào file CSV nếu cần

        except Exception as e:
            print(e)
            break


# Đóng trình duyệt khi hoàn thành

# Đóng trình duyệt

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
    reaction_All = reaction_Like = reaction_Love = reaction_Care = reaction_Wow = reaction_Haha = reaction_Angry = reaction_Huhu = 0
    try:
        link_element = driver.find_element(By.XPATH, '//div[contains(@id, "sentence_")]//a[contains(@href, "/ufi/reaction/profile/")]')

    # Lấy giá trị href từ thẻ a
        link_href = link_element.get_attribute('href')
        # sleep(random.uniform(2.25, 5.5) )
        driver.get(link_href)
        
        # sleep(random.uniform(2.25, 5.5) )
        
        # Duyệt qua từng thẻ div và tìm các thẻ con có arial-label chứa các reaction như "Like", "Haha", ...
        reaction_Like = count_react(driver , "Like")
        reaction_Love = count_react(driver , "Love")
        reaction_Care = count_react(driver , "Care")
        reaction_Wow = count_react(driver , "Wow")
        reaction_Haha = count_react(driver , "Haha")
        reaction_Angry = count_react(driver , "Angry")
        reaction_Huhu = count_react(driver , "Huhu")
        reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
        # sleep(random.uniform(2.25, 5.5) )
        driver.get(link)
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
                # sleep(random.uniform(2.25, 5.5) )

                driver.get(next_link)
                # sleep(random.uniform(2.25, 5.5) )
                abbr_element_next  = driver.find_element(By.XPATH, '//div[@data-ft=\'{"tn":",g"}\']//abbr')
        # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
                time_image_next = abbr_element_next.text
                if time_image_next!=time_image:
                    break
                img_element = driver.find_element(By.XPATH, '//div[@style="text-align:center;"]//img')

                image_links.append(img_element.get_attribute("src"))

            else:
                break
        # sleep(random.uniform(2.25, 5.5) )
        driver.get(link)
        # sleep(random.uniform(2.25, 5.5) )
    
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
        try:
            first_nested_div = div_element.find_element(By.XPATH, ".//div[1]")
            h3_element = first_nested_div.find_element(By.TAG_NAME, "h3")
            a_element = h3_element.find_element(By.TAG_NAME, "a")
            auth_links.append(a_element.get_attribute("href"))
            auth_names.append(a_element.text)
            adjacent_div = h3_element.find_element(By.XPATH, "following-sibling::div[1]")
            div_texts.append(adjacent_div.text)
        except Exception as e:
            pass
    return auth_links, auth_names, div_texts

def crawl_comments(driver):
    auth_links_comments = []
    auth_names_comments = []
    comments = []
    
    div_prev_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
    div_more_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
    link_count = 0
    while True:
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
            # sleep(random.uniform(2.25, 5.5) )
            driver.get(link)
            link_count += 1
            # fake(driver , link_count , link)
        except Exception as e:
            print(e)
            break

    return auth_links_comments, auth_names_comments, comments

def main():
    # driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
    driver = uc.Chrome(options = chrome_options)

    login(driver)    
    
# Tạo link dựa trên từ vừa nhập
    while True:
        search_term = input("Nhập từ cần tìm kiếm (nhập 0 để dừng): ")
        
        if search_term == '0':
            print("Chương trình đã dừng.")
            return
        
        # Tạo tên file CSV dựa trên search_term
        csv_filename = f"{search_term}_link.csv"

        # Mã hóa từ cần tìm kiếm
        encoded_search_term = search_term.replace(' ', '%20')

        # Tạo link dựa trên từ vừa mã hóa
        base_url = 'https://mbasic.facebook.com/search/posts?q='
        filters = '&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D'
        link_find = base_url + encoded_search_term + filters
        

        get_link(driver , link_find ,csv_filename )
        df_link = pd.read_csv(csv_filename) 
        p_link = df_link['Full_Story_Links'].to_list()
        comment_numbers = df_link['Number_comments'].to_list()
        if os.path.exists('data.json'):
            if os.path.getsize('data.json') == 0:
                data = {}
            else:
                with open('data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
        else:
            data = {}
        link_count = 8
        for link  , number_comment in zip(p_link ,comment_numbers) :
                unique_key = link
                if unique_key not in data:
                    # sleep(random.uniform(2.25, 5.5) )
                    
                    driver.get(link)
                    link_count +=1
                    print(link_count)
                    # fake(driver , link_count , link)

                    sleep(random.uniform(2.25, 5.5) )
                    auth_link , auth_text = find_author(driver)
                    content = find_content(driver)+find_content_background(driver)
                    reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu = count_react_item(driver , link)
                    link_video = find_link_video(driver)
                    link_author_share , text_share = find_link_share(driver)
                    content_share = find_content_share(driver)
                    time_text = find_time(driver)
                    time_process  , _= getCreatedTime(time_text)
                    # In kết quả
                    image_links = find_all_images(driver , link)
                    auth_links_comments ,auth_names_comments ,  comments = crawl_comments(driver)
                    data_line = {"Link_post": link, 
                                    "author":{ 'author_link': auth_link ,  
                                            'auth_name': auth_text
                                        } 
                                ,"time":time_process , "content": content , 
                                "share_post":{
                                    'link_author_share: ' : link_author_share ,
                                    'author_share: ' : text_share ,
                                    'content_share: ' : content_share,
                                    
                                } ,
                                "video_only": link_video , 
                                "image_post_list":   image_links ,
                            
                                "number_reaction": {"Like": reaction_Like, "Love": reaction_Love , 
                                            "Care": reaction_Care , "Wow": reaction_Wow , 
                                            "Haha": reaction_Haha , "Angry": reaction_Angry,
                                            "Huhu": reaction_Huhu,
                                            "All_react": reaction_All , 
                                    },
                                "comment":{
                                    "number_of_comments":number_comment , 
                                    "account_links_comment": auth_links_comments,
                                    "name_comment_list" : auth_names_comments ,
                                    "comment_list": comments  , 
                                } }

                    # crawl commen
                
                    data[unique_key] = data_line
                    print(f"Đã thêm mới phần tử với key: {unique_key}")
                    print(json.dumps(data_line, ensure_ascii=False, indent=4))
                else:
                    print(f"Phần tử với key: {unique_key} đã tồn tại!")

                    
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.write('\n')
                
                
                
if __name__ == '__main__':
    main()