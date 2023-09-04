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
import time_process as tp


class Detail_Post_Crawler:
    def __init__(self , driver):
        self.driver = driver
    
    def find_author(self):

        # Danh sách các cấu trúc XPath có thể chứa tên tác giả
        xpaths = [
            '//div[@id="objects_container"]//table[@role="presentation"]//strong/span/a',
            '//div[@id="objects_container"]//table[@role="presentation"]//span/strong/a',
            '//div[@id="objects_container"]//table[@role="presentation"]//strong/a',
            '//div[@id="objects_container"]//table[@role="presentation"]//span/a'
        ]

        auth_element = None
        for xpath in xpaths:
            try:
                auth_element = self.driver.find_element(By.XPATH, xpath)
                break
            except:
                continue

        if auth_element:
            link = auth_element.get_attribute('href')
            text = auth_element.get_attribute('text')
            return link, text
        else:
            return None, None

    def find_content(self):
        try:
            div_elem = self.driver.find_element(By.XPATH, '//div[@data-ft=\'{"tn":"*s"}\']')
            # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
            p_elements = div_elem.find_elements(By.TAG_NAME, 'p')
            texts = [elem.text for elem in p_elements]

            # Gộp tất cả các dòng text thành một văn bản
            full_text = ' '.join(texts)
        except Exception as e:
            full_text = ''
        return full_text
    def find_content_background(self):
        try:
            divs_with_style = self.driver.find_element(By.XPATH , '//div[@data-ft=\'{"tn":"*s"}\']//div[contains(@style, "background-image")]')

        # Duyệt qua từng thẻ div và lấy các văn bản trong thẻ span có style chứa chuỗi "background-image"
            
            all_text = ' '.join(span.text  for span in divs_with_style.find_elements(By.XPATH , './/span'))
        except Exception as e:
            all_text = ''
        return all_text
    def find_link_share(self):
        try:
            divs_with_table = self.driver.find_element(By.XPATH , '//div[@data-ft=\'{"tn":"H"}\'][.//table]')
            link_share_element = divs_with_table.find_element(By.TAG_NAME , 'a')
            link_share = link_share_element.get_attribute('href')
            table_element = divs_with_table.find_element(By.XPATH , './/table')
            table_text = table_element.text
        except Exception as e:
            table_text = ''
            link_share = ''
        return link_share , table_text
            
    def find_content_share(self):
        try:
            outer_div = self.driver.find_elements(By.XPATH, '//div[@data-ft=\'{"tn":"H"}\']')
            inner_div_s = outer_div[0].find_element(By.XPATH, './/div[@data-ft=\'{"tn":"*s"}\']')
            p_elements = inner_div_s.find_elements(By.TAG_NAME, 'p')
            texts = [elem.text for elem in p_elements]

            # Gộp tất cả các dòng text thành một văn bản
            full_text = ' '.join(texts)
        except:
            full_text = ''
        return full_text




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

    def count_react_item(self):
        reaction_All = reaction_Like = reaction_Love = reaction_Care = reaction_Wow = reaction_Haha = reaction_Angry = reaction_Huhu = 0
        try:
            link_element = self.driver.find_element(By.XPATH, '//div[contains(@id, "sentence_")]//a[contains(@href, "/ufi/reaction/profile/")]')

        # Lấy giá trị href từ thẻ a
            link_href = link_element.get_attribute('href')
            
            sleep(random.uniform(2.25, 5.5) )
            # driver.get(link_href)
            link_element.click()
            sleep(random.uniform(2.25, 5.5) )
            
            # Duyệt qua từng thẻ div và tìm các thẻ con có arial-label chứa các reaction như "Like", "Haha", ...
            reaction_Like = self.count_react("Like")
            reaction_Love = self.count_react("Love")
            reaction_Care = self.count_react("Care")
            reaction_Wow = self.count_react("Wow")
            reaction_Haha = self.count_react("Haha")
            reaction_Angry = self.count_react("Angry")
            reaction_Huhu = self.count_react("Sad")
            reaction_All = reaction_Like+reaction_Love+reaction_Care+reaction_Wow+reaction_Haha+reaction_Angry+reaction_Huhu
            sleep(random.uniform(2.25, 5.5) )
            self.driver.back()
        except Exception as e:
            print(e)
            pass
        # sleep(random.uniform(2.25, 5.5) )
        

        return reaction_All ,  reaction_Like , reaction_Love, reaction_Care , reaction_Wow , reaction_Haha , reaction_Angry , reaction_Huhu
    def find_all_images(self , link):
        xpath_img = '//div[@data-ft=\'{"tn":"H"}\']//a[contains(@href, \'photo\')]//img'    
        img_elements = self.driver.find_elements(By.XPATH , xpath_img)
        xpath_href_img = '//div[@data-ft=\'{"tn":"H"}\']//a[contains(@href, \'photo\')]'
        href_img_elements = self.driver.find_elements(By.XPATH , xpath_href_img)
        # Lưu trữ các liên kết hình ảnh
        image_links = [img_element.get_attribute("src") for img_element in img_elements]
        image_links_a = [href_img_element.get_attribute("href") for href_img_element in href_img_elements]
        ids_hrefs = [re.search(r'fbid=(\d+)', link).group(1) for link in image_links_a if re.search(r'fbid=(\d+)', link)]
        start_meet_video = 0
        if len(image_links_a) >1:
            self.driver.get(image_links_a[len(image_links_a)-1])
            abbr_element  = self.driver.find_elements(By.XPATH, '//div[@data-ft=\'{"tn":",g"}\']//abbr')
            time_image = abbr_element[0].text

            while(True):
                xpath_next = '//a[starts-with(@href, \'/photo.php?\') and normalize-space()="Next"]'
                next_element = self.driver.find_elements(By.XPATH, xpath_next)
                next_link = next_element[0].get_attribute("href")

                if(start_meet_video != 0):
                    next_link = 'Previous'
                    
                try:
                    id_match = re.search(r'fbid=(\d+)', next_link).group(1)
                except:
                    try:
                        if(start_meet_video ==0):
                            self.driver.get(image_links_a[0])
                            start_meet_video = start_meet_video+1
                        xpath_next = '//a[starts-with(@href, \'/photo.php?\') and normalize-space()="Previous"]'
                        next_element = self.driver.find_element(By.XPATH, xpath_next)
                        next_link = next_element.get_attribute("href")
                        id_match = re.search(r'fbid=(\d+)', next_link).group(1)
                    except:
                        break
                if id_match not in ids_hrefs:
                    image_links_a.append(next_link)
                    ids_hrefs.append(id_match)
                    sleep(random.uniform(2.25, 5.5) )

                    self.driver.get(next_link)
                    sleep(random.uniform(2.25, 5.5) )
                    abbr_element_next  = self.driver.find_element(By.XPATH, '//div[@data-ft=\'{"tn":",g"}\']//abbr')
            # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
                    time_image_next = abbr_element_next.text
                    if time_image_next!=time_image:
                        break
                    img_element = self.driver.find_element(By.XPATH, '//div[@style="text-align:center;"]//img')

                    image_links.append(img_element.get_attribute("src"))

                else:
                    break
            sleep(random.uniform(2.25, 5.5) )
            self.driver.get(link)
            sleep(random.uniform(2.25, 5.5) )
        
        return image_links
    def find_link_video(self):
        video_link = "no video"
        try:
            outer_div = self.driver.find_elements(By.XPATH, '//div[@data-ft=\'{"tn":"H"}\']')

            element = outer_div[0].find_element(By.XPATH , "//a[starts-with(@href, '/video_redirect/')]")
            video_link = element.get_attribute("href")
        except Exception as e:
            pass
        return video_link

    def find_time(self):
        try:
            abbr_element  = self.driver.find_element(By.XPATH, '//footer[@data-ft=\'{"tn":"*W"}\']//abbr')
            # Trích xuất nội dung text từ tất cả thẻ p con bên trong thẻ div tìm được
            time_text = abbr_element.text
            time_pro = tp.getCreatedTime(time_text)
            # Gộp tất cả các dòng text thành một văn bả
        except Exception as e:
            time_pro = ''
        return time_pro


    #time process 












