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
def login(driver):
    driver.get('https://www.facebook.com/')
    sleep(3)
    cookies = pickle.load(open("my_cookie_new.pkl" , "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    sleep(3)
    driver.get('https://www.facebook.com/')
    sleep(2)

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-notification")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
driver = uc.Chrome(options = chrome_options)
# login(driver)    
def logout(driver):
    driver.get('https://mbasic.facebook.com/')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    xpath_expression = "//a[contains(text(), 'Logout')]"
    logout_button = driver.find_element(By.XPATH , xpath_expression)
    sleep(3)
    # Thực hiện các hành động trên thẻ (ví dụ: nhấp chuột để đăng xuất)
    logout_button.click()
    value_to_click = "Don't save and log out"
    input_element = driver.find_element(By.XPATH , f"//input[@value='{value_to_click}']")

    # Thực hiện hành động nhấp chuột vào phần tử
    input_element.click()
    sleep(3)
    try:
        value_contain = "Don't save"

        # Tìm phần tử <input> dựa trên giá trị thuộc tính 'value' chứa chuỗi
        xpath_expression = f"//input[contains(@value, \"{value_contain}\") and @type='submit']"
        input_element = driver.find_element(By.XPATH, xpath_expression)
        sleep(3)
        # Thực hiện hành động nhấp chuột vào phần tử
        input_element.click()
    except:
        pass

    
    sleep(3)
# driver.get('https://mbasic.facebook.com/story.php?story_fbid=pfbid04AtuyaTTCabFn524AB1erKdmp4Znz6nAsUvZM4idbgGEPQGvpZjgtTwQM96HkQhCl&id=100070521700525&eav=AfYwpRhc2OzTuaAZjjTZyi5w4anwEvPeYSUZsGadbDuKNSm4-_wGeWcZmUMizL7K1cI&__xts__%5B0%5D=12.AbrnYfZhK5bbkFKI7OkAa6kkFvw1coN_3uyyO0WsHakCy9N2oHWqmPhDSaYVrIfd66JfDX7Pn86mm7z5E50qZ5b_PYIUl4O-wrAJiZrp5FJfYYFA971Mw0ZLyxF2gu8Irw_dQhfKPqkA4LYReQ6dmSotxAt06WeM7SQ8vXG9MuW31D9vvL_TDssEzbyKKvnzg52jX3YXYFGkaeZoPeFAgqOxvcKl379CcVkngLf3jBFUUjfIoY_bO_5hvQ9LO1cYBfd3q2DsXHE4rYMryo0sgtRNr2KoW9PHIKkitPUCHPMo2jVCpa_K8xLrdNJ60sMa9MDPnBf0SuItBEhcBaS914yPnOa4xc6nMc7FFSOumj1myGpj3TvOFzKJLzfFFHrenBGz4iJrHO6gTwJShERJoSwrInyEh8HdeHg7zpMhvDtXBAwCV6vEjy8ln50NmBiVFstelYqRszavtZogYbf_naNDi6cqCl3E5fJDkzlT8QwNThFk3tdgyG22Yt_ltMlc-zcXeIxzG8k99DPx9sZbzL6x6g6FO9d7XfgyTwXyY9RFJ50oLWz6uTuXrAm_sNvK3v-fC15XD7WEOKYw3xh9MdzIL5pal_7coj-BweTQeYyCjp9hMyQVQlQ64221qGA_6lM&__tn__=%2AW&paipv=0#footer_action_list,3')
sleep(3)
value_contain = "Don't save"

# Tìm phần tử <input> dựa trên giá trị thuộc tính 'value' chứa chuỗi
xpath_expression = f"//input[contains(@value, \"{value_contain}\") and @type='submit']"
input_element = driver.find_element(By.XPATH, xpath_expression)

# Thực hiện hành động nhấp chuột vào phần tử
input_element.click()

# logout(driver)