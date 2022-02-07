import time as timer
import pyautogui
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from multiprocess import Process
from tkinter.constants import BOTTOM, BROWSE, LEFT, RIGHT, TOP
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException

# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

chromedriver_path = ChromeDriverManager().install()

MIDNIGHT = "17:22:10"

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

username = ""
password = ""
timing = ""

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {} 
  
        for F in (LoginPage, TimingPage, ConfirmationPage):
  
            frame = F(container, self)
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_timing_frame(self, cont, user_box, password_box):
        frame = self.frames[cont]
        global username
        username = user_box.get()
        global password
        password = password_box.get()
        frame.tkraise()
    
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        label = ttk.Label(self, text ="Login")
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        user_box = ttk.Entry(self, text="User Name", textvariable=username)
        user_box.grid(row = 1, column = 1, padx = 10, pady = 10)

        password_box = ttk.Entry(self, text ="Password", textvariable=password, show='*')
        password_box.grid(row = 2, column = 1, padx = 10, pady = 10)

        confirm_button = ttk.Button(self, text ="Confirm", command = lambda : controller.show_timing_frame(TimingPage, user_box, password_box))
        confirm_button.grid(row = 3, column = 1, padx = 10, pady = 10)
  
class TimingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        timing_label = tk.Label(self, text="Timing", bd=0)
        timing_label.grid(row = 0, column = 1, padx = 10, pady = 10)

        timing_listbox = tk.Listbox(self, width=47, height=20, selectmode=BROWSE, exportselection=0)
        for count, item in enumerate(AVAILABLE_TIMINGS):
            timing_listbox.insert(count, item)
        timing_listbox.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        confirm_button = ttk.Button(self, text ="Confirm", command = lambda : start_bot(timing_listbox))
        confirm_button.grid(row = 2, column = 1, padx = 10, pady = 10)
  
class ConfirmationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="You have selected", bd=0)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        user_label = tk.Label(self, text=username)
        user_label.grid(row = 1, column = 1, padx = 10, pady = 10)
        password_label = tk.Label(self, text=password)
        password_label.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        confirm_button = ttk.Button(self, text ="Confirm", command = lambda : start_bot())
        confirm_button.grid(row = 2, column = 1, padx = 10, pady = 10)
        
def start_bot(time):
    timing = time.get(time.curselection())
    user = [username, password]
    process_1 = Process(target=new_window, args=(user, 6, timing,))
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


def new_window(username, court_number, timing):
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
    #root = tk.Tk()
    #root.geometry("800x800")
    #root.configure(bg='grey')
    app = tkinterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
