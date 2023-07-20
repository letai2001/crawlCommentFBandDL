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
import humanfriendly
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
from queue import Queue
import json
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pickle




df_link = pd.read_csv('filtered_output.csv') 
# TSC = TikiScraper_link_item()
# df_link = TSC.scrape_page_link()

p_link = df_link['link_post'].to_list()
# p_link = p1_link[42:100]
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}') 
driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
 
driver.get('https://www.facebook.com/')
sleep(3)
cookies = pickle.load(open("my_cookie.pkl" , "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
sleep(3)
driver.get('https://www.facebook.com/')
sleep(2)

#git
data = []
MAX_RETRIES = 5
visited_links = set()
try:
    with open('data21.json', 'r') as f:
        for line in f:
            obj = json.loads(line)
            visited_links.add(obj['Link'])
except json.decoder.JSONDecodeError as e:
    print(f'Lỗi phân tích JSON: {e}')
for link in p_link:
    if link not in visited_links:# Open the JSON file for reading
        driver.get(link)
        sleep(2)

            # # Cuộn trang xuống 1/3 chiều cao của trang
    # Danh sách để chứa văn bản đã được nối từ mỗi thẻ div lớn
        joined_texts = []
        # unique_comments = set()
        visited_links.add(link)
        processed = 0

        while True:
            try:
                big_divs = driver.find_elements(By.XPATH , '//div[@class="x1lliihq xjkvuk6 x1iorvi4"]')

                for big_div in big_divs[processed:]:
                    more_button = big_div.find_elements(By.XPATH , './/div[@role="button" and text()="See more"]')
                    if more_button: 
                        # Nhấp vào nút đó
                        driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -100);",more_button[0])
                        more_button[0].click()
                    # Trong mỗi thẻ div lớn, tìm tất cả các thẻ div con
                    text_elements = big_div.find_elements(By.XPATH , './/span[@dir="auto" and @lang="en"]/div/div[@dir="auto"]')
                    # Lấy văn bản từ mỗi thẻ div con và nối chúng lại với nhau
                    texts = [element.text for element in text_elements]
                    joined_text = ' '.join(texts)
                    # Chỉ thêm văn bản đã được nối vào danh sách nếu nó không tồn tại trong set
                    # if joined_text not in unique_comments:
                    # unique_comments.add(joined_text)
                    data.append({"Link": link,  'comment': joined_text , })
                    with open('data21.json', 'a') as f:
                        json.dump(data[-1], f)
                        f.write('\n')
                processed = len(big_divs)
                more_button_2 = driver.find_element(By.XPATH , '//div[@role="button" and contains(.,"View more comments")]')

                # Cuộn trang đến nút đó
                driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -50);", more_button_2)
                # Nhấp vào nút đó
                more_button_2.click()
                
                # Đợi một chút để trang web tải thêm bình luận
                sleep(3)

            except Exception as e:
                
                # Nếu không tìm thấy nút "Xem thêm bình luận", thoát khỏi vòng lặp
                break
        
# Khởi tạo một set để lưu trữ các comment duy nhất


    

    
            
    

