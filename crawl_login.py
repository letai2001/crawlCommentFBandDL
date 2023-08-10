import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
import pickle
import undetected_chromedriver as uc

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')


# driver = webdriver.Chrome("C:\\Users\\Admin\\Downloads\\chromdriv\\chromedriver.exe" , options=chrome_options)
driver = uc.Chrome(options = chrome_options)

driver.get('https://www.facebook.com/')

# fill in account and password
txtUser = driver.find_element(By.ID , "email")
txtUser.send_keys('ove67156@omeie.com')
sleep(2)    
txtPassword = driver.find_element(By.ID , "pass")
txtPassword.send_keys('thanhnam4321')
sleep(2)
txtPassword.send_keys(Keys.ENTER)
sleep(10)
pickle.dump(driver.get_cookies() , open("my_cookie_3.pkl" , "wb"))

driver.close()