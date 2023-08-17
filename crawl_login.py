import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
import pickle
import undetected_chromedriver as uc
import os
import csv
import re
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notification")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
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
driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
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
    link_count = 1
    while len(comments)<=200:
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
            driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", a_element)

            link = a_element.get_attribute('href')
            # sleep(random.uniform(2.25, 5.5) )
            a_element.click()
            link_count += 1

            # fake(driver , link_count , link)
        except Exception as e:
            print(e)
            break

    return auth_links_comments, auth_names_comments, comments , link_count

# driver.get('https://www.facebook.com//')

# txtUser = driver.find_element(By.ID , "email")
# txtUser.send_keys('yco17417@omeie.com')
# # txtUser.send_keys('sda80931@omeie.com')

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
# def get_link(driver , link , csv_filename):
#     sleep(1.75)
#     driver.get(link)
#     sleep(2)
    # if not os.path.exists(csv_filename) or os.path.getsize(csv_filename) == 0:
    #     with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    #         csv_writer = csv.writer(csv_file)
    #         csv_writer.writerow(["Full_Story_Links", "Number_comments"])
    # existing_links = set()
    #             # Đọc nội dung hiện tại của file CSV để xác định những link đã ghi vào trước đó
    # if os.path.isfile(csv_filename):
    #     with open(csv_filename, mode="r", newline="", encoding="utf-8") as csv_file:
    #         csv_reader = csv.reader(csv_file)
    #         header = next(csv_reader)  # Đọc tiêu đề cột
    #         if header != ["Full_Story_Links", "Number_comments"]:
    #             # Thêm tiêu đề cột nếu không tồn tại
    #             with open(csv_filename, mode="w", newline="", encoding="utf-8") as new_csv_file:
    #                 csv_writer = csv.writer(new_csv_file)
    #                 csv_writer.writerow(["Full_Story_Links", "Number_comments"])
    #         else:
    #             for row in csv_reader:
    #                     link_row = row[0] 
    #                     # Truy cập cột "Full_Story_Links" (cột thứ 0)
    #                     existing_links.add(extract_id(link_row))
while True:
    try:
        div_elements = driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')

        full_story_links = []
        number_comments = []

        for i in range(0 ,len(div_elements)):
            
            driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", div_elements[i])
            full_story_element = div_elements[i].find_element(By.XPATH, ".//a[text()='Full Story']")
            driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", full_story_element)
            full_story_link = full_story_element.get_attribute('href')
            full_story_element.click()
            print("Adding new link to list:", full_story_link)
        # full_story_links.append(full_story_link)
        # try:
        #     comment_element = div.find_element(By.XPATH, ".//a[contains(text(),'Comment')]")
        #     comment_text = comment_element.get_attribute('text')
        #     comment_number = re.search(r'(\d+(?:,\d+)?)\s+Comment', comment_text).group(1)

        # except Exception as e:
        #     comment_number = 0
        # number_comments.append(comment_number)
            auth_links_comments, auth_names_comments, comments , link_count = crawl_comments(driver)
            for i in range(0 , link_count):
                driver.back()
            div_elements = driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')
        # Ghi dữ liệu vào file CSV chỉ cho những link mới
        # with open(csv_filename, mode="a" if os.path.exists(csv_filename) else "w", newline="", encoding="utf-8") as csv_file:
        #     csv_writer = csv.writer(csv_file)
        #     for link, comment_number in zip(full_story_links, number_comments):
        #         csv_writer.writerow([link, comment_number])

        # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
        sleep(random.uniform(2.25, 5.5) )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        see_more_link = driver.find_element(By.XPATH, "//div[contains(@text, 'ee more')]//a")
        see_more_href = see_more_link.get_attribute("href")
        sleep(random.uniform(2.25, 5.5) )
        driver.get(see_more_href)
        sleep(random.uniform(2.25, 5.5) )

        # Tiếp tục xử lý và ghi dữ liệu vào file CSV nếu cần

    except Exception as e:
        print(e)
        break
