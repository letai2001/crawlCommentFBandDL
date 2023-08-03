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




df_link = pd.read_csv('filtered_output.csv') 
# TSC = TikiScraper_link_item()
# df_link = TSC.scrape_page_link()

p_link = df_link['link_post'].to_list()
# p_link = p1_link[42:100]
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
def find_name(driver):
    # Danh sách các cấu trúc XPath có thể chứa tên
    xpaths = [
        '//h2[contains(@class, "x1heor9g")]//span[contains(@class, "xt0psk2")]/strong/span',
        '//h2[contains(@class, "x1heor9g")]//span[contains(@class, "xt0psk2")]/a/strong/span'
    ]
    
    # Thử tìm tên theo từng cấu trúc trong danh sách
    for xpath in xpaths:
        try:
            name_element = driver.find_element(By.XPATH, xpath)
            return name_element.text
        except NoSuchElementException:
            pass
    
    return None

# for link in p_link:
link = 'https://www.facebook.com/fabrizioromanoherewego/posts/pfbid0rJY2rhx19GVc7ajnzKPrtuHidoiU8ssC6K634YeXuuain7db7Gb5hfkW3VXaDxRml'
driver.get(link)
sleep(2)


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



# Tìm thẻ span có id là ":r7:"
# tmp = []
# big_span = driver.find_elements(By.XPATH, "//span[@class='xmper1u xt0psk2 xjb2p0i x1qlqyl8 x15bjb6t x1n2onr6 x17ihmo5 x1g77sc7']")
# spans_text = big_span[0].find_elements(By.XPATH, ".//span")
# for span in spans_text:
#     text = span.text
#     order_value =  int(span.value_of_css_property('order'))
#     position_value = span.value_of_css_property('position')
#     # has_vdwwD_class = 'vdwD' in span.get_attribute('class') udwC

#     if position_value == 'relative':
#         tmp.append({'order_value' : order_value, 'text' : text})

# tmp.sort(key=lambda x: x['order_value'])
xpath_main_div = '//div[contains(@class, "x126k92a")]'

parent_element = driver.find_elements(By.XPATH,xpath_main_div )

# Tìm tất cả các phần tử div con bên trong có thuộc tính dir='auto'
# div_elements = parent_element.find_elements(By.XPATH, ".//div")

# Lấy văn bản từ mỗi phần tử div và nối chúng lại
complete_text = ' '.join(div.text for div in parent_element)



time_element = driver.find_element(By.XPATH, "//span[@class='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']/a/span")

# time_text = ''.join(item['text'] for item in tmp).lower()
time_text = time_element.text

img_tag = driver.find_element(By.XPATH , '//div[@class="xqtp20y x6ikm8r x10wlt62 x1n2onr6"]/div/img')


# Tìm thẻ <img> bên trong thẻ <a>

# Lấy thuộc tính 'src' chứa link ảnh
link_url_author = img_tag.get_attribute('src')
blocking_element_xpath = '//path[d="M15 35.8C6.5 34.3 0 26.9 0 18 0 8.1 8.1 0 18 0s18 8.1 18 18c0 8.9-6.5 16.3-15 17.8l-1-.8h-4l-1 .8z"]'

wait = WebDriverWait(driver, 10)
button_div = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[starts-with(@aria-label, "Like") and @role="button"]')))
driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", button_div)

# Nhấp vào nút
# button_div.click()
# Nhấp vào nút
# button_div.click()

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

width = driver.execute_script("return window.innerWidth")
height = driver.execute_script("return window.innerHeight")

# Tạo một tọa độ ngẫu nhiên trong kích thước của cửa sổ trình duyệt
random_x = random.randint(0, width)
random_y = random.randint(0, height)

# Sử dụng ActionChains để thực hiện click tại tọa độ ngẫu nhiên
action = ActionChains(driver)
action.move_by_offset(random_x, random_y).click().perform()
sleep(1.5)

share_xpath = "//span[contains(text(), 'shares') and contains(@class, 'x193iq5w')]"
share_element = driver.find_element(By.XPATH , share_xpath)
share_text = share_element.text
comment_sum_xpath = "//span[contains(text(), 'comments') and contains(@class, 'x193iq5w')]"
cm_sum_element = driver.find_element(By.XPATH , comment_sum_xpath)
cm_sum_text = cm_sum_element.text
data_line = {"Link": link.split('/')[-1], 
                    
    
    "image_post_link": link_url_author
,"time":time_text , "content": complete_text , 
               

"reaction": {"Like": reaction_Like, "Love": reaction_Love , 
             "Care": reaction_Care , "Wow": reaction_Wow , 
             "Haha": reaction_Haha , "Angry": reaction_Angry,
             "Huhu": reaction_Huhu,
    },
"share":share_text,
"comment":{
    "number_comments": cm_sum_text
} }
data.append(data_line)
with open('data23.json', 'a') as f:
        json.dump(data[-1], f,indent=4)
        # f.write('\n')