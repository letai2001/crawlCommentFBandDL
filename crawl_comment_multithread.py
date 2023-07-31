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
import os
import pickle

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')


data = []

number_of_threads = 2


def loginFB(driver):
    driver.get('https://www.facebook.com/')
    sleep(3)
    cookies = pickle.load(open("my_cookie2.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    sleep(3)
    driver.get('https://www.facebook.com/')
    sleep(2)


def crawl_comment(driver, comments_data):
    joined_text = []
    processed = 0
    while True:
        try:
            big_divs = driver.find_elements(
                By.XPATH, '//div[@class="x1lliihq xjkvuk6 x1iorvi4"]')

            for big_div in big_divs[processed:]:
                try:
                    more_button = big_div.find_elements(
                        By.XPATH, './/div[@role="button" and text()="Xem thêm"]')
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
                comments_data["comments"].append(joined_text)

            processed = len(big_divs)
            more_button_2 = driver.find_element(
                By.XPATH, '//div[@role="button" and contains(.,"Xem thêm bình luận")]')
            driver.execute_script(
                "arguments[0].scrollIntoView(); window.scrollBy(0, -50);", more_button_2)
            more_button_2.click()
            sleep(2)

        except Exception as e:
            break


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


def find_time(driver):
    time_element = driver.find_element(
        By.XPATH, "//span[@class='x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j']/a/span")

    # time_text = ''.join(item['text'] for item in tmp).lower()
    time_text = time_element.text
    return time_text


def find_post(driver):
    parent_element = driver.find_element(
        By.XPATH, "//div[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a']")

    # Tìm tất cả các phần tử div con bên trong có thuộc tính dir='auto'
    div_elements = parent_element.find_elements(
        By.XPATH, ".//div[@dir='auto']")

    # Lấy văn bản từ mỗi phần tử div và nối chúng lại
    complete_text = ' '.join(div.text for div in div_elements)
    return complete_text


visited_links = set()
# Open the JSON file for reading

try:
    with open('data.json', 'r') as f:
        for line in f:
            obj = json.loads(line)
            visited_links.add(obj['Link'])
except json.decoder.JSONDecodeError as e:
    print(f'Lỗi phân tích JSON: {e}')


def get_data_from_link(queue, lock, visited_links_lock, queue_lock):
    driver = webdriver.Chrome(
        "C:\\Users\\Admin\\Downloads\\crawlDataTraining_selenium\\chromedriver.exe", options=chrome_options)
    loginFB(driver)
    while(True):
        with queue_lock:
            link = queue.get()

        if link is None:
            break

        if link not in visited_links:
            driver.get(link)
            sleep(1.5)
            time = find_time(driver)
            post = find_post(driver)
            comments_data = {"Link": link, "time": time,
                             "content": post,  "comments": []}
            # crawl comment
            crawl_comment(driver, comments_data)

            data.append(comments_data)

            with visited_links_lock:
                visited_links.add(link)
        # Ghi dữ liệu vào file JSON
            with lock:
                with open('data.json', 'a') as f:
                    json.dump(data[-1], f)
                    f.write('\n')


def main():

    df_link = pd.read_csv('filtered_output.csv')
    p_link = df_link['link_post'].to_list()

    lock = threading.Lock()
    visited_links_lock = threading.Lock()
    queue_lock = threading.Lock()

    queue = Queue()
    for link in p_link:
        queue.put(link)
    for i in range(number_of_threads):
        queue.put(None)
    threads = []

    for i in range(number_of_threads):
        t = threading.Thread(target=get_data_from_link, args=(
            queue, lock, visited_links_lock, queue_lock,))
        threads.append(t)

    # Bắt đầu chạy các thread
    for t in threads:
        t.start()

    # Đợi cho tất cả các thread hoàn thành công việc
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
