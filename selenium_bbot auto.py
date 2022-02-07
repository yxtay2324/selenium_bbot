import time as timer
import pyautogui
from datetime import datetime
from multiprocess import Process
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException

# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chromedriver_path = ChromeDriverManager().install()

MIDNIGHT = "00:00:00"
TIMING = "2100-2200"
USERNAME = ' '
PASSWORD = ' '

AVAILABLE_TIMINGS = {
    "1000-1100": 14,
    "1100-1200": 20,
    "1200-1300": 26,
    "1300-1400": 32,
    "1400-1500": 38,
    "1500-1600": 44,
    "1600-1700": 50,
    "1700-1800": 56,
    "1800-1900": 62,
    "1900-2000": 68,
    "2000-2100": 74,
    "2100-2200": 80
}
        
def start_bot():
    timing = TIMING
    user = [USERNAME, PASSWORD]
    process_1 = Process(target=new_window, args=(False, user, 6, timing,))
    process_1.start()
    process_1.join()
    """
    process_2 = Process(target=new_window, args=(self.debugger_mode, user, 2, timing,))
    process_3 = Process(target=new_window, args=(self.debugger_mode, user, 4, timing,))

    
    process_2.start()
    process_3.start()

    
    process_2.join()
    process_3.join()
    """

    # html patterns show xpath up till 2nd last segment (tr[...]) is fixed,
    # tr[...] corresponding to the row of the RIGHT MOST column, and td corresponding to the column whole row,
    # with tr[50] being the first target (1600-1700 court 1) and 
    # tr[67] being the last target (1800-1900 court 6), 
    # meaning all targeted rows are numbered sequentially from 50-67.
    # 1600-1700 tr[50-55], 1700-1800 tr[56-61], 1800-1900 tr[62-67]
    # empty courts have an additional final segment named "input" after the td[...], and must be included in the xpath for bbot to find the button
    # note that ALL court one columns extend to 10 columns, meaning td[10] must be used instead of td[9]
    # example of taken court element-(1700-1800 court 1) "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[56]/td[10]"
    # example of taken court element-(1800-1900 court 1) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[62]/td[10]"
    # example of empty court element-(1900-2000 court 1) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[68]/td[10]/input"
    # example of taken court element-(1600-1700 court 2) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[51]/td[9]"
    # example of taken court element-(1600-1700 court 3) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[52]/td[9]"
    # example of taken court element-(1700-1800 court 3) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[58]/td[9]"
    # example of taken court element-(1800-1900 court 3) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[64]/td[9]"
    # confirm button element- //*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/input[18]


def new_window(debug, username, court_number, timing):
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(
        'https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg=')

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

    if not debug:
        count = 0
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == MIDNIGHT:
                break
            timer.sleep(1)
            count += 1

    north_hill_court = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
        "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[1]/td/input"))
    ).click()

    #key = timing + " court " + str(court_number)
    #element = COURT_TO_XPATH[key]
    element_tr = AVAILABLE_TIMINGS[timing] + (court_number - 1)
    if court_number == 1:
        element_td = "td[10]"
    else:
        element_td = "td[9]"
    element = "tr[" + str(element_tr) + "]/" + element_td
    court_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
        "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/{}/input".format(element))) #element is tr[68]/td[10]
    ).click()

    try:
        confirm_book_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
            "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/input[18]"))
        ).click()
        pyautogui.alert("Court booked. Click OK to exit.")
        timer.sleep(180)
    except UnexpectedAlertPresentException as e:
        pyautogui.alert(title='Error', text=format(str(e)))
        timer.sleep(180)


def main():
    start_bot()

if __name__ == "__main__":
    main()
