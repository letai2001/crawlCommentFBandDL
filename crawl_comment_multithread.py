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



lock = threading.Lock()
visited_links_lock  = threading.Lock()
visited_links = set()
# Open the JSON file for reading
number_of_threads = 8
lock = threading.Lock()
queue_lock = threading.Lock()
visited_links = set()

try:
    with open('data22.json', 'r') as f:
        for line in f:
            obj = json.loads(line)
            visited_links.add(obj['Link'])
except json.decoder.JSONDecodeError as e:
    print(f'Lỗi phân tích JSON: {e}')

df_link = pd.read_csv('filtered_output.csv') 
# TSC = TikiScraper_link_item()
# df_link = TSC.scrape_page_link()

p_link = df_link['link_post'].to_list()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')  
data = []
def login_facebook(driver):
    driver.get('https://www.facebook.com/')
    txtUser = driver.find_element(By.ID , "email")
    txtUser.send_keys('wasantha.lifel.o.gy@gmail.com')
    sleep(2)
    txtPassword = driver.find_element(By.ID , "pass")
    txtPassword.send_keys('thanhnam4321')
    sleep(2)
    txtPassword.send_keys(Keys.ENTER)
    sleep(5)
def login_with_cookie(driver):
    driver.get('https://www.facebook.com/')
    sleep(3)
    cookies = pickle.load(open("my_cookie_new.pkl" , "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    sleep(3)
    driver.get('https://www.facebook.com/')
    sleep(2)



def get_data_from_link(queue   , lock , visited_links_lock , queue_lock):
    driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
    login_with_cookie(driver)
    sleep(2)
    while(True):
        with queue_lock:
            link = queue.get()
        
        if link is None:
            break
       
        if link not in visited_links:
                
                driver.get(link)
        sleep(2)
        unique_comments = set()
        with visited_links_lock:
                visited_links.add(link)
        while True:
            try:
                big_divs = driver.find_elements(By.XPATH , '//div[@class="x1lliihq xjkvuk6 x1iorvi4"]')

                for big_div in big_divs:
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
                    if joined_text not in unique_comments:
                        unique_comments.add(joined_text)
                        data.append({"Link": link,  'comment': joined_text , })
                        with lock:
                            with open('data22.json', 'a') as f:
                                json.dump(data[-1], f)
                                f.write('\n')

                more_button_2 = driver.find_element(By.XPATH , '//div[@role="button" and contains(.,"View more comments")]')

                # Cuộn trang đến nút đó
                driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -100);", more_button_2)
                # Nhấp vào nút đó
                more_button_2.click()
                
                # Đợi một chút để trang web tải thêm bình luận
                sleep(3)

            except Exception as e:
                
                # Nếu không tìm thấy nút "Xem thêm bình luận", thoát khỏi vòng lặp
                break

                    
        # Ghi dữ liệu vào file JSON
            
def main():
    queue = Queue()
    for link in p_link:
        queue.put(link)
    for i in range(number_of_threads):
        queue.put(None)
    threads = []

    for i in range(number_of_threads):
        t = threading.Thread(target=get_data_from_link, args=(queue, lock, visited_links_lock , queue_lock ,))
        threads.append(t)

    # Bắt đầu chạy các thread
    for t in threads:   
        t.start()

    # Đợi cho tất cả các thread hoàn thành công việc
    for t in threads:
        t.join()
if __name__ == "__main__":
    main()