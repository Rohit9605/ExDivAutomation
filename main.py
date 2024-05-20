from __future__ import print_function
import webbrowser
import logging
import configparser
from rauth import OAuth1Service
from logging.handlers import RotatingFileHandler
from accounts.accounts import Accounts
import pandas as pd
import schedule
from schedule import every, repeat
from datetime import time, timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# loading configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt=f'%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

def oauth_etrade():

    """Allows user authorization for the sample application with OAuth 1"""
    success = False
    while (success == False):
        try:
           etrade = OAuth1Service(
              name="etrade",
              consumer_key=config["DEFAULT"]["CONSUMER_KEY"],
              consumer_secret=config["DEFAULT"]["CONSUMER_SECRET"],
              request_token_url="https://api.etrade.com/oauth/request_token",
              access_token_url="https://api.etrade.com/oauth/access_token",
              authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
              base_url="https://api.etrade.com")
           
           # def renew_token():
           #     url = "https://api.etrade.com/oauth/renew_access_token"
           
           #     response = session.get(url, header_auth=True)
           #     print(response)

           # renew_token()
           # Step 1: Get OAuth 1 request token and secret
           request_token, request_token_secret = etrade.get_request_token(
               params={"oauth_callback": "oob", "format": "json"})

           # Step 2: Go through the authentication flow. Login to E*TRADE.
           # After you login, the page will provide a text code to enter.
           authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
           webbrowser.open(authorize_url)
           text_code = input("Please accept agreement and enter text code from browser: ")
           
           # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
           session = etrade.get_auth_session(request_token,
                                      request_token_secret,
                                      params={"oauth_verifier": text_code})
           print(session)
           success = True
        except:
           print("Failed to authenticate trying again")
    

    base_url = "https://api.etrade.com"
    accounts = Accounts(session, base_url)
    accounts.account_list()

def click():
    PATH = "C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"
    #cService = webdriver.ChromeService(executable_path=PATH)
    #driver = webdriver.Chrome(service = cService)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    service = Service(executable_path=PATH)
    driver=webdriver.Chrome(service=service, options=options)

    #webdriver performs all actions on webbrowser (eg Chrome)
    #driver = webdriver.Chrome(PATH)
    #driver.implicitly_wait(10)
    driver.get("https://us.etrade.com/e/t/etws/authorize?key=7661fa0f2eb1f9abe3b5ffec7be0aba8&token=+h+bfhKLbdVrKXVYSwSylrPQqoBhI46a3uAacPLUxyA=")
    
    #sleep(30)
    # try:
        # link = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.LINK_TEXT, "Accept"))
        # )
    
    #Login Page
    logon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mfaLogonButton"))
    )
    #logon = driver.find_element(By.ID, "mfaLogonButton")
    #link1.click()
    element = driver.find_element(By.ID, "USER")
    element.send_keys("rohitgundam05")
    element = driver.find_element(By.ID, "password")
    element.send_keys("Trade123$$??")
    logon.click()

    #Account notice Page
    # link2 = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.NAME, "raccontinue"))
    # )
    # link2.click()
    # link2 = WebDriverWait(driver, 10).until(
    #      continue_button = driver.find_element(By.ID, "continue-button")
    # )
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "continue-button")))
    # element.click()
    # actions = ActionChains(driver)
    # actions.click(continue_button)
    # actions.perform()


    # except:
    #     driver.quit()
    #gets title of webpage
    #driver.title()
    #closes tab
    #driver.close()
    #closes browser
    #driver.quit()

#schedule.every().day.at("11:12").do(oauth_etrade)
if __name__ == "__main__":
    click()
    oauth_etrade()
    # while True:
    #     schedule.run_pending()
    


