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
import csv
import os
import undetected_chromedriver as uc



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

link = 'https://mbasic.facebook.com/search/posts?q=phandong&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D'
sleep(1.75)
driver.get(link)
sleep(2)

while True:
    try:
        div_elements = driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')
        full_story_links = []
        number_comments = []

        # Đọc nội dung hiện tại của file CSV để xác định những link đã ghi vào trước đó
        existing_links = set()
        csv_filename = "full_story_links.csv"
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
                        existing_links.add(row[0])  # Lưu các link đã ghi vào danh sách

        for div in div_elements:
            full_story_element = div.find_element(By.XPATH, ".//a[text()='Full Story']")
            full_story_link = full_story_element.get_attribute('href')
            if full_story_link not in existing_links:  # Kiểm tra xem link đã tồn tại hay chưa
                print("Adding new link to list:", full_story_link)
                full_story_links.append(full_story_link)
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
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        see_more_link = driver.find_element(By.XPATH, "//div[contains(@id, 'see_more')]//a")
        see_more_href = see_more_link.get_attribute("href")
        sleep(1.5)
        driver.get(see_more_href)
        sleep(1.5)

        # Tiếp tục xử lý và ghi dữ liệu vào file CSV nếu cần

    except Exception as e:
        print(e)
        break


# Đóng trình duyệt khi hoàn thành

# Đóng trình duyệt
driver.quit()
