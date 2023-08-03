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
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os
link_csv = 'out_put.csv'
fix_link_csv = 'filtered_output.csv'
name_row = 'link_post'
# TSC = TikiScraper_link_item()
# df_link = TSC.scrape_page_link()

# p_link = p1_link[42:100]
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}') 

def get_post_link(driver ,link_csv , url):
    driver.get(url) # Thay thế 'your_url' bằng URL thực tế bạn muốn truy cập
    sleep(3)

    crawled_hrefs = set()
    if not os.path.exists(link_csv):
    # Tệp không tồn tại, tạo tệp mới
        with open(link_csv, "w", newline="", encoding="utf-8") as file:
            # Ghi dòng tiêu đề nếu cần
            # header = ["Column 1", "Column 2", ...]
            # writer = csv.writer(file)
            # writer.writerow(header)
            pass  # Bỏ qua hoặc thay đổi thành mã tạo dòng tiêu đề

    
    with open(link_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # Kiểm tra xem dòng không rỗng
                crawled_hrefs.add(row[0])

# Kiểm tra độ dài của file CSV
    num_lines = len(crawled_hrefs)
    num_lines_2 = 0

    # Nếu file CSV đã có 1000 dòng hoặc nhiều hơn, không thực thi vòng lặp
    if num_lines < 500:
        # Mở file CSV trong chế độ ghi tiếp tục
        with open(link_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            while True:  # Vòng lặp vô hạn, dừng lại khi đạt được điều kiện
                # Cuộn trang xuống đến cuối
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                
                # Tìm tất cả các nút share trên trang
                shareBtns = driver.find_elements(By.XPATH , '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"]')
                
                # Lấy href từ các nút share, kiểm tra xem chúng đã được crawl chưa và nếu chưa thì ghi vào file CSV
                if(num_lines == 0):
                    for btn in shareBtns[num_lines_2:]:
                        href = btn.get_attribute('href')
                        crawled_hrefs.add(href)
                        writer.writerow([href])
                        
                else:
                    for btn in shareBtns:
                        href = btn.get_attribute('href')
                        if href not in crawled_hrefs:
                            crawled_hrefs.add(href)
                            writer.writerow([href])
                        else:
                            break
                
                # Kiểm tra độ dài file CSV, dừng vòng lặp nếu file CSV đã chứa 1000 dòng
                num_lines_2 = len(crawled_hrefs)
                if num_lines_2 >=500:
                    break

                # Dừng chương trình trong một khoảng thời gian (ví dụ 5 giây) trước khi cuộn trang tiếp theo
                sleep(1)

def fix_csv(name_csv , fix_csv , name_row):
    filtered_links = []

# Đọc file CSV hiện tại và lưu các liên kết thỏa mãn vào danh sách filtered_links
    with open(name_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].startswith("https://www.facebook.com/fabrizioromanoherewego/posts"):
                filtered_links.append(row[0])

    # Ghi các liên kết đã lọc vào một file mới (hoặc ghi đè lên file hiện tại nếu bạn muốn)
    with open(fix_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name_row])  # Ghi tiêu đề cột vào dòng đầu tiên của file
        for link in filtered_links:
            writer.writerow([link])

 
def loginFB(driver):
    driver.get('https://www.facebook.com/')
    sleep(3)
    cookies = pickle.load(open("my_cookie.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    sleep(3)
    driver.get('https://www.facebook.com/')
    sleep(2)
    
    
def get_content_post(driver):
    xpath_main_div = '//div[contains(@class, "x126k92a")]'

    parent_element = driver.find_elements(By.XPATH,xpath_main_div )

    complete_text = ' '.join(div.text for div in parent_element)
    return complete_text

def get_time_post(driver):
    time_element = driver.find_element(By.XPATH, "//span[@class='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']/a/span")

# time_text = ''.join(item['text'] for item in tmp).lower()
    time_text = time_element.text

    return time_text
    
def get_image_post(driver):
    img_tags = driver.find_elements(By.XPATH, '//div[@class="xqtp20y x6ikm8r x10wlt62 x1n2onr6"]/div/img')
    link_imgs = [img_tag.get_attribute('src') for img_tag in img_tags]
    return link_imgs

def crawl_comment(driver, comments_data , account_comment_list):
    joined_text = []
    processed = 0
    while True:
        try:
            big_divs = driver.find_elements(
                By.XPATH, '//div[@class="x1lliihq xjkvuk6 x1iorvi4"]')
            big_link_accounts = driver.find_elements(By.XPATH, '//span[@class="xt0psk2"]/a[@aria-hidden="true"]')
            for big_div, big_link_account in zip(big_divs[processed:], big_link_accounts[processed:]):
                try:
                    more_button = big_div.find_elements(
                        By.XPATH, './/div[@role="button" and text()="See more"]')
                    if more_button:
                        driver.execute_script(
                            "arguments[0].scrollIntoView(); window.scrollBy(0, -100);", more_button[0])
                        more_button[0].click()
                except Exception as e:
                    pass

                text_elements = big_div.find_elements(
                    By.XPATH, './/span[@dir="auto" and @lang="en"]/div/div[@dir="auto"]')
                texts = [element.text for element in text_elements]
                joined_text = ' '.join(texts)
                comments_data.append(joined_text)

                account_comment_list.append(big_link_account.get_attribute('href'))               
            processed = len(big_divs)
            more_button_2 = driver.find_element(
                By.XPATH, '//div[@role="button" and contains(.,"View more comments")]')
            driver.execute_script(
                "arguments[0].scrollIntoView(); window.scrollBy(0, -50);", more_button_2)
            more_button_2.click()
            sleep(2)

        except Exception as e:
            break
    
    
def count_react(element, react):
    number = 0
    try:
        # Sử dụng f-string để nối biến react vào chuỗi XPath
        reaction = element.find_element(By.XPATH, f".//*[contains(@aria-label, '{react}')]")
        aria_label = reaction.get_attribute('aria-label')
        
        number = aria_label.split()[-1]
    except Exception as e:
        pass
    return number
def count_react_item(driver):
    wait = WebDriverWait(driver, 10)

    button_div = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@aria-label, "Like") and @role="button"]')))
    driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", button_div)

    driver.execute_script("arguments[0].click();", button_div)
    sleep(2.5)

    react_element = driver.find_element(By.CSS_SELECTOR , '.x14ju556.x1n2onr6')

    # Duyệt qua từng thẻ div và tìm các thẻ con có arial-label chứa các reaction như "Like", "Haha", ...
    reaction_Like = count_react(react_element , "Like")
    reaction_Love = count_react(react_element , "Love")
    reaction_Care = count_react(react_element , "Care")
    reaction_Wow = count_react(react_element , "Wow")
    reaction_Haha = count_react(react_element , "Haha")
    reaction_Angry = count_react(react_element , "Angry")
    reaction_Huhu = count_react(react_element , "Huhu")

    close_button = driver.find_element(By.XPATH, "//div[@aria-label='Close']")

    # Bấm vào nút đóng bằng JavaScript
    driver.execute_script("arguments[0].click();", close_button)
    sleep(1.5)
    return reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu


def count_share_post(driver):
    share_xpath = "//span[contains(text(), 'shares') and contains(@class, 'x193iq5w')]"
    share_element = driver.find_element(By.XPATH , share_xpath)
    share_text = share_element.text
    return share_text


def count_comments_post(driver):
    comment_sum_xpath = "//span[contains(text(), 'comments') and contains(@class, 'x193iq5w')]"
    cm_sum_element = driver.find_element(By.XPATH , comment_sum_xpath)
    cm_sum_text = cm_sum_element.text
    return cm_sum_text


#git
data = []
visited_links = set()
try:
    with open('data21.json', 'r') as f:
        for line in f:
            obj = json.loads(line)
            visited_links.add(obj['Link'])
except json.decoder.JSONDecodeError as e:
    print(f'Lỗi phân tích JSON: {e}')
def main():
    driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
    url = 'https://www.facebook.com/fabrizioromanoherewego'
    loginFB(driver)
    sleep(2)
    get_post_link(driver ,link_csv ,url )
    
    fix_csv(link_csv , fix_link_csv , name_row)
    df_link = pd.read_csv(fix_link_csv) 

    p_link = df_link[name_row].to_list()

    
    for link in p_link:
        if link not in visited_links:# Open the JSON file for reading
            driver.get(link)
            sleep(2)

                # # Cuộn trang xuống 1/3 chiều cao của trang
        # Danh sách để chứa văn bản đã được nối từ mỗi thẻ div lớn
            link_imgs = get_image_post(driver)
            time_post = get_time_post(driver)
            content_post = get_content_post(driver)
            
            share_count = count_share_post(driver)
            comment_count = count_comments_post(driver)
            comments_data = []
            account_comment_list = []
            reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu = count_react_item(driver)
            crawl_comment(driver, comments_data,account_comment_list)

            data_line = {"Link": link.split('/')[-1], 
                            "image_post_link": link_imgs
                        ,"time":time_post , "content": content_post , 
                                    

                        "reaction": {"Like": reaction_Like, "Love": reaction_Love , 
                                    "Care": reaction_Care , "Wow": reaction_Wow , 
                                    "Haha": reaction_Haha , "Angry": reaction_Angry,
                                    "Huhu": reaction_Huhu,
                            },
                        "share":share_count,
                        "comment":{
                            "number_comments": comment_count , 
                            "comment_list" : comments_data ,
                            "account_links_comment": account_comment_list
                        } }
        
                # crawl comment
            


                
            data.append(data_line)
            visited_links.add(link)
            with open('data23.json', 'a') as f:
                json.dump(data_line, f,indent=4)
                f.write('\n')

        
# Khởi tạo một set để lưu trữ các comment duy nhất

if __name__ == "__main__":
    main()
    

    
            
    

