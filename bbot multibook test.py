from multiprocessing import Process
import time as timer
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import datetime, time

chromedriver_path = r"C:\Users\umer2\Downloads\chromedriver_win32\chromedriver.exe"
user_database = {
    "YX": ["YTAY033", "P@ssw0rd!@as"],
    "ZH": ["TANZ0154", "Buttosai1998!"],
    "CELESTE": ["ta0005te", "MHiss@CE230121"],
    "JOLENE": ["JOLE0009", "Bts1306!"],
    "NIGEL": ["nleong003", "S765432e!"]
}
MIDNIGHT = "00:52:00"

def select_court(username):
    driver = webdriver.Chrome(chromedriver_path) 
    driver.get('https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg=')

    username_element = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input"
    ).send_keys(username[0])

    username_OK = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
        "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[4]/td/input[1]"))
    ).click()

    password_element = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,
        "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input"))
    ).send_keys(username[1])

    password_OK = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,
        "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[5]/td/input[1]"))
    ).click()

    count = 0
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == MIDNIGHT:
            break
        timer.sleep(1)
        count += 1  
    
    north_hill_court = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
        "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[1]/td/input"))
    ).click()

def main():
    process_yx = Process(target=select_court, args=(user_database["YX"], ))
    process_zh = Process(target=select_court, args=(user_database["ZH"], ))

    process_yx.start()
    process_zh.start()

    process_yx.join()
    process_zh.join()

if __name__ == "__main__":
    main()