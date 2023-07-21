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
import os
import csv
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
driver.get('https://www.facebook.com/')
sleep(3)
cookies = pickle.load(open("my_cookie2.pkl" , "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
sleep(3)
driver.get('https://www.facebook.com/')
sleep(2)
driver.get('https://www.facebook.com/fabrizioromanoherewego') # Thay thế 'your_url' bằng URL thực tế bạn muốn truy cập
sleep(3)
# Mở (hoặc tạo) file CSV
crawled_hrefs = set()

with open('output.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if row:  # Kiểm tra xem dòng không rỗng
            crawled_hrefs.add(row[0])

# Kiểm tra độ dài của file CSV
num_lines = len(crawled_hrefs)

# Nếu file CSV đã có 1000 dòng hoặc nhiều hơn, không thực thi vòng lặp
if num_lines < 5000:
    # Mở file CSV trong chế độ ghi tiếp tục
    with open('output2.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        while True:  # Vòng lặp vô hạn, dừng lại khi đạt được điều kiện
            # Cuộn trang xuống đến cuối
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            
            # Tìm tất cả các nút share trên trang
            shareBtns = driver.find_elements(By.XPATH , '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"]')
            
            # Lấy href từ các nút share, kiểm tra xem chúng đã được crawl chưa và nếu chưa thì ghi vào file CSV
            for btn in shareBtns:
                href = btn.get_attribute('href')
                if href not in crawled_hrefs:
                    crawled_hrefs.add(href)
                    writer.writerow([href])
            
            # Kiểm tra độ dài file CSV, dừng vòng lặp nếu file CSV đã chứa 1000 dòng
            if len(crawled_hrefs) >=5000:
                break

            # Dừng chương trình trong một khoảng thời gian (ví dụ 5 giây) trước khi cuộn trang tiếp theo
            sleep(4)
