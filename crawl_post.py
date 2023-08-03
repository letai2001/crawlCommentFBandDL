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
cookies = pickle.load(open("my_cookie2.pkl" , "rb"))
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

for link in p_link:
    # link = 'https://www.facebook.com/raumdeuter13/posts/pfbid0hpsTAbDL71XLwqC5WDsuRtQSLbasEqX7ULmffW7b3xZGykCc9bzr5vYJAunYm4DGl'
    driver.get(link)
    sleep(2)



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
    comments_data = {"Link": link, "time":time_text , "content": complete_text}
    data.append(comments_data)
    with open('data23.json', 'a') as f:
            json.dump(data[-1], f)
            f.write('\n')

