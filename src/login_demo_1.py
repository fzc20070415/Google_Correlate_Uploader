from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from config import *

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

CSV_OUTPUT_DIR = '../data/output.csv'
NAME = "112"

def login(USR, PWD):
    print("Logging in to Google")
    browser.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/')
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#identifierId")))
    next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#identifierNext > span > span")))
    input.send_keys(USR)
    next.click()
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")))
    next = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#passwordNext > span > span")))
    input.send_keys(PWD)
    next.click()
    wait.until(EC.presence_of_all_elements_located((By.ID, "gsr")))

def upload_csv(CSV_DIR, monthly=False):
    print("-"*40)
    print("Uploading csv to Google Correlate ({})".format("monthly" if monthly else "weekly"))
    if monthly:
        type = "monthly"
    else:
        type = "weekly"
    try:
        browser.get('http://www.google.com/trends/correlate/edit?e=&t='+type)
        file = wait.until(EC.presence_of_element_located((By.ID, "csv-"+type)))
        name = wait.until(EC.presence_of_element_located((By.ID, "name-"+type)))
        submit = wait.until(EC.element_to_be_clickable((By.ID, "submit-"+type)))
        name.send_keys(NAME)   # Random Input
        file.send_keys(os.path.abspath(CSV_DIR))
        time.sleep(1)
        submit.click()
    except TimeoutException:
        return upload_csv(CSV_DIR, monthly)
    wait.until(EC.presence_of_all_elements_located((By.ID, "footer")))

def analyze_result():
    print("Analyzing result:")
    result = browser.find_element_by_id("results")
    # print(result.text)
    if result.text == "No results found for " + NAME + ". Edit this data":
        print("\tNo results found.")
        return 0
    print("\t Results found!")
    return 1

def read_result():
    print("ERROR: login_demo_1.read_result() not implemented, aborting")
    exit()
    # TODO

    return []


def main():
    print("Checking configuration file: USR={}, PWD={}".format(USR,PWD))

    login(USR, PWD)
    upload_csv(CSV_OUTPUT_DIR)
    if analyze_result():
        browser.maximize_window()
        input("Found relevant info: Press Enter to Continue...")
    # upload_csv("../data/RETAILSMNSA.csv", True)
    # analyze_result()

if __name__ == "__main__":
    main()
