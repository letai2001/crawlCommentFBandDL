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
from webdriver_manager.chrome import ChromeDriverManager
import time_process as tp

class Detail_Comment_Crawler :
    def __init__(self , driver , comment_element):
        self.driver = driver
        self.comment_element = comment_element
    def find_id(self):
        comment_id = self.comment_element.get_attribute("id")
        return comment_id
    def find_author(self):
        first_nested_div = self.comment_element.find_element(By.XPATH, ".//div[1]")
        h3_element = first_nested_div.find_element(By.TAG_NAME, "h3")
        a_element = h3_element.find_element(By.TAG_NAME, "a")
        author_link = a_element.get_attribute("href")
        author = a_element.text
        return author_link , author
    

    def find_content(self):
        first_nested_div = self.comment_element.find_element(By.XPATH, ".//div[1]")
        h3_element = first_nested_div.find_element(By.TAG_NAME, "h3")
        adjacent_div = h3_element.find_element(By.XPATH, "following-sibling::div[1]")
        content = adjacent_div.text
        return content
    def find_created_time(self):
        time_element = self.comment_element.find_element(By.TAG_NAME, "abbr")
        time_text = time_element.text
        time_process  , _= tp.getCreatedTime(time_text)
        created_time = time_process
        return created_time
    def find_image_list(self):
        image_url = []
        comment_id = self.comment_element.get_attribute("id")
        try:
            xpath_img = f"//div[@id='{comment_id}']//a[contains(@href, 'photo')]//img"

                
            img_element = self.driver.find_element(By.XPATH , xpath_img)
            img_link = img_element.get_attribute('src')
            image_url.append(img_link)
        except Exception as e:
            image_url = ''
        return image_url
    def find_video(self):
        video_url = []
        comment_id = self.comment_element.get_attribute("id")
        try:  
            
            video_element = self.driver.find_element(By.XPATH , f"//div[@id='{comment_id}']//a[starts-with(@href, '/video_redirect/')]")
            video_href  = video_element.get_attribute('href')
            video_url.append(video_href)
        except Exception as e:
            video_url = ''
    def count_react(self , react):
        number = 0
        
        try:
            xpath_expression = f"//a[@role='button']/img[@alt='{react}']/following-sibling::span"
            reaction_count = self.driver.find_element(By.XPATH, xpath_expression).text
            if 'K' in reaction_count:
                number = int(float(reaction_count.replace('K', '')) * 1000)
            else:
                number = int(reaction_count)

        except Exception as e:
            pass
        return number

    def find_reaction(self):
        comment_id = self.comment_element.get_attribute("id")
        reaction_Like = reaction_Love = reaction_Wow = reaction_Haha = reaction_Angry = reaction_Huhu = 0

        try: 
            link_element = self.comment_element.find_element(By.XPATH  , f"//span[contains(@id, 'like') and contains(@id, '_{comment_id}')]//a[contains(@href, '/ufi/reaction/profile/')]")  
            link_href = link_element.get_attribute('href')
            
            sleep(random.uniform(2.25, 5.5) )
    # driver.get(link_href)
            self.driver.get(link_href)
            # link_element.click()
            
            sleep(random.uniform(2.25, 5.5) )
            
            reaction_Like = self.count_react(self.driver , "Like")
            reaction_Love = self.count_react(self.driver , "Love")
            reaction_Wow = self.count_react(self.driver , "Wow")
            reaction_Haha = self.count_react(self.driver , "Haha")
            reaction_Angry = self.count_react(self.driver , "Angry")
            reaction_Huhu = self.count_react(self.driver , "Sad")
            
            self.driver.back()
        except Exception as e:
           pass

        return reaction_Like , reaction_Love , reaction_Wow , reaction_Haha , reaction_Angry  , reaction_Huhu
    def get_data_from_comment(driver , comment_element):
        comment_post = Post()
        comment_id = comment_element.get_attribute("id")
        comment_post.id = comment_id
        
        first_nested_div = comment_element.find_element(By.XPATH, ".//div[1]")
        h3_element = first_nested_div.find_element(By.TAG_NAME, "h3")
        a_element = h3_element.find_element(By.TAG_NAME, "a")
        comment_post.author_link = a_element.get_attribute("href")
        comment_post.author = a_element.text
        
        adjacent_div = h3_element.find_element(By.XPATH, "following-sibling::div[1]")
        comment_post.content = adjacent_div.text
        time_element = comment_element.find_element(By.TAG_NAME, "abbr")
        time_text = time_element.text
        time_process  , _= time_process.getCreatedTime(time_text)
        comment_post.created_time = time_process
        
        try:
            xpath_img = f"//div[@id='{comment_id}']//a[contains(@href, 'photo')]//img"

                
            img_element = driver.find_element(By.XPATH , xpath_img)
            img_link = img_element.get_attribute('src')
            comment_post.image_url.append(img_link)
        except Exception as e:
            comment_post.image_url = ''
        
        try:  
            
            video_element = driver.find_element(By.XPATH , f"//div[@id='{comment_id}']//a[starts-with(@href, '/video_redirect/')]")
            video_href  = video_element.get_attribute('href')
            comment_post.video.append(video_href)
        except Exception as e:
            comment_post.video = ''
        try: 
            link_element = comment_element.find_element(By.XPATH  , f"//span[contains(@id, 'like') and contains(@id, '_{comment_id}')]//a[contains(@href, '/ufi/reaction/profile/')]")  
            link_href = link_element.get_attribute('href')
            
            sleep(random.uniform(2.25, 5.5) )
    # driver.get(link_href)
            driver.get(link_href)
            # link_element.click()
            
            sleep(random.uniform(2.25, 5.5) )
            
            reaction_Like = count_react(driver , "Like")
            reaction_Love = count_react(driver , "Love")
            reaction_Care = count_react(driver , "Care")
            reaction_Wow = count_react(driver , "Wow")
            reaction_Haha = count_react(driver , "Haha")
            reaction_Angry = count_react(driver , "Angry")
            reaction_Huhu = count_react(driver , "Sad")
            reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
            comment_post.like = reaction_Like
            comment_post.love = reaction_Love
            comment_post.wow = reaction_Wow
            comment_post.haha = reaction_Haha
            comment_post.angry = reaction_Angry
            comment_post.sad = reaction_Huhu
            driver.back()
        except Exception as e:
            comment_post.like = 0
            comment_post.love = 0
            comment_post.wow = 0
            comment_post.haha = 0
            comment_post.angry = 0
            comment_post.sad = 0
        return comment_post
