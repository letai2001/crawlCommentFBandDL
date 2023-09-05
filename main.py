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
from utils import Detail_Post_Crawler
from post import Post
from utils_comment import Detail_Comment_Crawler
import time_process as tp
DRIVER_PATH = "C:\\Users\\ADMIN\\Downloads\\chromedrivver\\chromedriver-win64\\chromedriver.exe"
USER_NAME = 'lee_tai12@yahoo.com.vn'
PASS = 'thanhnam4321'
FILE_JSON_POST = 'data_post.json'
FILE_JSON_COMMENT = 'data_comment.json'
SEARCH_MORE_XPATH = '//*[@id="see_more_pager"]/a/span'
GROUP_MORE_XPATH = '//a[span[text()="See more posts"]]'


class MbasicCrawlerTool:
    def __init__(self, username=None, password=None):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-notification")
        chrome_options.add_argument("--incognito")
        # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
        # chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')

        # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        # chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(DRIVER_PATH , options=chrome_options)
 
        self.post_detail = Detail_Post_Crawler(self.driver)
        self.username = username
        self.password = password

        if username and password:
            self.login(username, password)
    def login(self , username , password):
        self.driver.get('https://www.facebook.com//')
        txtUser = self.driver.find_element(By.ID , "email")
        txtUser.send_keys(username)
        sleep(2)    
        txtPassword = self.driver.find_element(By.ID , "pass")
        txtPassword.send_keys(password)
        sleep(2)
        txtPassword.send_keys(Keys.ENTER)
        sleep(10)
    def browse_link_story(self , link_list_story , see_more_xpath):
        self.driver.get(link_list_story)
        sleep(3)
        while True:

            try:
                div_elements = self.driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')

                full_story_links = []
                number_comments = []
                
                for i in range(1 ,len(div_elements)):
                    current_post = Post()
                    comments = {}
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", div_elements[i+1])
                        full_story_element = div_elements[i+1].find_element(By.XPATH, ".//a[text()='Full Story']")
                        self.driver.execute_script("arguments[0].scrollIntoView();window.scrollBy(0, -200);", full_story_element)
                        full_story_link = full_story_element.get_attribute('href')
                        try:
                            comment_element = div_elements[i+1].find_element(By.XPATH, ".//a[contains(text(),'Comment')]")
                            comment_text = comment_element.get_attribute('text')
                            comment_number = re.search(r'(\d+(?:,\d+)?)\s+Comment', comment_text).group(1)

                        except Exception as e:
                            comment_number = 0

                        sleep(random.uniform(2.25, 3) )
                        full_story_element.click()
                        # link_get_story = link_get_story+ 1 
                        # print('link_get_story = ' , link_get_story)
                        # driver = fake(driver , link_get_story , full_story_link)
                        # sleep(random.uniform(3.5, 5.5) )
                        print("Adding new link to list:", full_story_link)
                        current_post = self.get_data_detail_post(comment_number , full_story_link)
                        
                        comments = self.crawl_comments(current_post)

                        self.export_to_json(FILE_JSON_POST , current_post)
                        sleep(random.uniform(3,4.5) )
                        self.driver.get(link_list_story)

                        div_elements = self.driver.find_elements(By.XPATH, './/footer[@data-ft=\'{"tn":"*W"}\']')

                    except Exception as e:
                        print(e)
                        pass
                        
                sleep(random.uniform(2.25, 5.5) )
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                see_more_link = self.driver.find_element(By.XPATH, see_more_xpath)
                link_list_story = see_more_link.get_attribute("href")
                

                sleep(random.uniform(2.25, 5.5) )
                self.driver.get(link_list_story)
                sleep(random.uniform(2.25, 5.5) )

                # Tiếp tục xử lý và ghi dữ liệu vào file CSV nếu cần

            except Exception as e:
                print(e)
                break
    def extract_id(self , link):
        id_value = 0
        try:
            id_match = re.search(r'story_fbid=([^&]+)', link)
            if id_match:
                id_value = id_match.group(1)
            else:
                group_id_match = re.search(r'/groups/([^/]+/permalink/[^/?]+)', link)
                if group_id_match:
                    id_value = group_id_match.group(1)
                else:
                    id_value = None
        except Exception as e:
            print(f"Error: {e}")
        return id_value
    def get_data_detail_post(self , number_comment , link):
        current_post = Post()
        
        current_post.id = self.extract_id(link)

        if 'permalink' in current_post.id:
            current_post.type = 'mbasic_group'
        else:
            current_post.type = 'mbasic_story'

        current_post.author_link , current_post.author = self.post_detail.find_author()
        current_post.content = self.post_detail.find_content()
        current_post.created_time , _ = self.post_detail.find_time()
        current_post.image_url = self.post_detail.find_all_images(link)
        current_post.video = self.post_detail.find_link_video()
        current_post.comment = number_comment
        all , current_post.like , current_post.love , care  , current_post.wow , current_post.haha , current_post.angry , current_post.sad = self.post_detail.count_react_item()
        return current_post
    
    def get_data_detail_comment(self , element,  current_post):
        comment_detail = Detail_Comment_Crawler(self.driver , element)
        current_comment = Post()
        current_comment.id = comment_detail.find_id()
        current_comment.type = "mbasic_comment"
        current_comment.author_link , current_comment.author = comment_detail.find_author()
        current_comment.created_time = comment_detail.find_created_time()
        current_comment.video  = comment_detail.find_video()
        current_comment.image_url = comment_detail.find_image_list()
        current_comment.content =    comment_detail.find_content()
        current_comment.source_id = current_post.id
        current_comment.like , current_comment.love , current_comment.wow , current_comment.haha , current_comment.angry , current_comment.sad = comment_detail.find_reaction()
        return current_comment
    def extract_info_from_div_comment(self , current_post):
        comments = {}
        div_comment_elements = self.driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
        for i in range(0 ,len(div_comment_elements)):
            try:
                comment_post = Post()

                comment_post = self.get_data_detail_comment(div_comment_elements[i] , current_post)
                comments[comment_post.id] = comment_post.to_dict_comment()
                
                div_comment_elements = self.driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
                try:
                    xpath_rep =f"//div[contains(@id, 'comment_replies_more') and contains(@id, '_{comment_post.id}')]//a[starts-with(@href, '/comment/replies/')]"
                    # xpath_rep = "//a[starts-with(@href, '/comment/replies/')]"
                    rep_element =  div_comment_elements[i].find_element(By.XPATH , xpath_rep)
                    rep_href = rep_element.get_attribute("href")
                    sleep(2)
                    self.driver.get(rep_href)
                    sleep(2)
                    div_comment_reps = self.driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
                    for i in range(1 ,len(div_comment_reps)):
                        comment_post_rep = self.get_data_detail_comment(div_comment_reps[i] , current_post)
                        comments[comment_post_rep.id] = comment_post_rep.to_dict_comment()
                        div_comment_reps = self.driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
                    self.driver.back()
                    div_comment_elements = self.driver.find_elements(By.XPATH, "//div[string-length(@id) >= 15 and translate(@id, '1234567890', '') = '']")
                except Exception as e:
                    print(e)
                    pass
            
            except Exception as e:
                print(e)
                pass
        return comments
    def crawl_comments(self , current_post):
        comments = {}    
        div_prev_elements = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
        div_more_elements = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
        link_count = 1
        while len(comments)<=100:
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
                comment_per_page = self.extract_info_from_div_comment(current_post)
                comments.update(comment_per_page)

                with open(FILE_JSON_COMMENT, 'w', encoding='utf-8') as f:
                    json.dump(comments, f, ensure_ascii=False, indent=4)
                    f.write('\n')
                print(len(comments)) 
                print(comments) 
                
                if len(div_more_elements) - len(div_prev_elements) < 0:
                    div_prev_elements = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'see_prev')]")
                    a_element = div_prev_elements[0].find_element(By.TAG_NAME, "a")
                elif len(div_more_elements) - len(div_prev_elements) > 0:
                    div_more_elements = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'see_next')]")
                    a_element = div_more_elements[0].find_element(By.TAG_NAME, "a")
                else:
                    break
                self.driver.execute_script("arguments[0].scrollIntoView();", a_element)

                link = a_element.get_attribute('href')
                sleep(random.uniform(2.25, 5.5) )
                a_element.click()
                # driver = fake(driver , link_get_story ,link)
                

                # fake(driver , link_count , link)
            except Exception as e:
                print(e)
                break

        return  comments 

    
    def export_to_json(self , file_json_name , current_post):
        
        if os.path.exists(file_json_name):
            if os.path.getsize(file_json_name) == 0:
                data = {}
            else:
                with open(file_json_name, 'r', encoding='utf-8') as f:
                    data = json.load(f)
        else:
                data = {}
        unique_key = current_post.id
        to_dict = {}
        if unique_key not in data:
            
            data[unique_key] = current_post.to_dict_post()
            print(f"Đã thêm mới phần tử với key: {unique_key}")
            print(json.dumps(current_post.to_dict_post(), ensure_ascii=False, indent=4))

        else:
            print(f"Phần tử với key: {unique_key} đã tồn tại!")

            
        with open(file_json_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.write('\n')
    def run_crawl_group(self , link_group):
        self.browse_link_story(link_group , GROUP_MORE_XPATH)
    def run_crawl_search(self , keywords):
        encoded_search_term = keywords.replace(' ', '%20')

        # Tạo link dựa trên từ vừa mã hóa
        base_url = 'https://mbasic.facebook.com/search/posts?q='
        filters = '&filters=eyJyZWNlbnRfcG9zdHM6MCI6IntcIm5hbWVcIjpcInJlY2VudF9wb3N0c1wiLFwiYXJnc1wiOlwiXCJ9In0%3D'
        link_find = base_url + encoded_search_term + filters

        self.browse_link_story(link_find ,SEARCH_MORE_XPATH )

        
        



class MbasicCrawlerJob:
    @staticmethod
    def run_script1(username, password , link_group):
        tool = MbasicCrawlerTool(username=username, password=password )
        tool.run_crawl_group(link_group)
    @staticmethod
    def run_script2(username ,password , keywords ):
        tool = MbasicCrawlerTool(username=username, password=password )
        tool.run_crawl_search(keywords)
if __name__ == "__main__":
    MbasicCrawlerJob.run_script1(
        username="lee_tai12@yahoo.com.vn", password="thanhnam4321", link_group = 'https://mbasic.facebook.com/groups/1212236082236816'
    )

    


