import time as timer
import tkinter as tk
import threading
from datetime import datetime, time
from tkinter.constants import BOTTOM, BROWSE, LEFT, RIGHT, TOP
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

chromedriver_path = r"C:\Users\umer2\Downloads\chromedriver_win32\chromedriver.exe"
MIDNIGHT = "00:00:00"
COURT_ORDER = [3, 4, 1, 2, 5, 6]
COURT_TO_XPATH_1600_1700 = ["tr[50]/td[10]", "tr[51]/td[9]", "tr[52]/td[9]", "tr[53]/td[9]", "tr[54]/td[9]", "tr[55]/td[9]"]
COURT_TO_XPATH_1700_1800 = ["tr[56]/td[10]", "tr[57]/td[9]", "tr[58]/td[9]", "tr[59]/td[9]", "tr[60]/td[9]", "tr[61]/td[9]"]
COURT_TO_XPATH_1800_1900 = ["tr[62]/td[10]", "tr[63]/td[9]", "tr[64]/td[9]", "tr[65]/td[9]", "tr[66]/td[9]", "tr[67]/td[9]"]
user_database = {
    "YX": ["YTAY033", "P@ssw0rd!@as"],
    "ZH": ["TANZ0154", "Buttosai1998!"],
    "CELESTE": ["ta0005te", "MHiss@CE230121"],
    "JOLENE": ["JOLE0009", "Bts1306!"],
    "NIGEL": ["nleong003", "S765432e!"]
}

class App(tk.Frame):
    user_listbox = None
    timing_listbox = None
    debugger_mode = False
    driver = webdriver.Chrome(chromedriver_path) 
    pause_till_midnight = threading.Event()

    def __init__(self, master=None):
        super().__init__(master)
        self.firstpage_init()

    def firstpage_init(self):
        frame_main = tk.Frame(bg="grey")
        frame_a = tk.Frame(master=frame_main, bg="grey")
        frame_b = tk.Frame(master=frame_main, bg="grey")
        
        self.user_listbox = tk.Listbox(master=frame_a, width=47, height=20, selectmode=BROWSE, exportselection=0)
        count = 1
        for i in user_database:
            self.user_listbox.insert(count, i)
            count += 1
        self.user_listbox.insert(count, "DEBUGGER")
        self.debugger_mode = True
        user_label = tk.Label(master=frame_a, text="User", bg="grey", bd=0)
        self.user_listbox.pack(side=BOTTOM)
        user_label.pack(side=TOP)

        self.timing_listbox = tk.Listbox(master=frame_b, width=47, height=20, selectmode=BROWSE, exportselection=0)
        self.timing_listbox.insert(1, "1600-1700")
        self.timing_listbox.insert(2, "1700-1800")
        self.timing_listbox.insert(3, "1800-1900")
        timing_label = tk.Label(master=frame_b, text="Timing", bg="grey", bd=0)
        self.timing_listbox.pack(side=BOTTOM)
        timing_label.pack(side=TOP)

        confirm_button = tk.Button(text="Confirm", command=self.confirm_clicked)

        frame_a.pack(side=LEFT)
        frame_b.pack(side=RIGHT)
        frame_main.pack(side=TOP)
        confirm_button.pack(side=BOTTOM)

    def confirm_clicked(self):
        if self.debugger_mode:
            user = user_database["YX"]
        else:
            user = user_database[self.user_listbox.get(self.user_listbox.curselection())]
        timing = self.timing_listbox.get(self.timing_listbox.curselection())

        self.driver.get('https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg=')

        username_element = self.driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input"
        ).send_keys(user[0])

        username_OK = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
            "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[4]/td/input[1]"))
        ).click()

        password_element = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH,
            "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input"))
        ).send_keys(user[1])

        password_OK = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH,
            "/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[5]/td/input[1]"))
        ).click()

        if not self.debugger_mode:
            self.wait_till_midnight()
            print("Its midnight!")

        north_hill_court = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[1]/td/input"))
        ).click()

        # html patterns show xpath up till 2nd last segment (tr[...]) is fixed,
        # tr[...] corresponding to the row of the RIGHT MOST column, and td corresponding to the column whole row,
        # with tr[50] being the first target (1600-1700 court 1) and 
        # tr[67] being the last target (1800-1900 court 6), 
        # meaning all targeted rows are numbered sequentially from 50-67.
        # 1600-1700 tr[50-55], 1700-1800 tr[56-61], 1800-1900 tr[62-67]
        # empty courts have an additional final segment named "input" after the td[...], and must be included in the xpath for bbot to find the button
        # note that ALL court one columns extend to 10 columns, meaning td[10] must be used instead of td[9]
        #example of taken court element-(1700-1800 court 1) "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[56]/td[10]"
        #example of taken court element-(1800-1900 court 1) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[62]/td[10]"
        #example of empty court element-(1900-2000 court 1) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[68]/td[10]/input"
        #example of taken court element-(1600-1700 court 2) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[51]/td[9]"
        #example of taken court element-(1600-1700 court 3) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[52]/td[9]"
        #example of taken court element-(1700-1800 court 3) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[58]/td[9]"
        #example of taken court element-(1800-1900 court 3) "//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/tr[64]/td[9]"
        # confirm button element- //*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/input[18]

        for i in COURT_ORDER:
            checker_thread = threading.Thread(target=self.select_court, args=[i, timing])
            checker_thread.start()

        confirm_book_button = WebDriverWait(self.driver, 65).until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/input[18]"))
        ).click()

    def get_time(self):
        count = 0
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == MIDNIGHT:
                self.pause_till_midnight.set()
                break
            print("Seconds elapsed ", count)  
            timer.sleep(1)
            count += 1          

    def wait_till_midnight(self):
        thread = threading.Thread(target=self.get_time)
        thread.start()
        self.pause_till_midnight.wait()
    
    def select_court(self, court_number, timing):
        element = None
        if timing == "1600-1700":
            element = COURT_TO_XPATH_1600_1700[court_number-1]
        elif timing == "1700-1800":
            element = COURT_TO_XPATH_1700_1800[court_number-1]
        elif timing == "1800-1900":
            element = COURT_TO_XPATH_1800_1900[court_number-1]
        court_button = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, 
            "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/{}/input".format(element)))
        ).click()

def main():
    root = tk.Tk()
    root.geometry("600x369")
    root.configure(bg='grey')
    app = App(root)
    app.mainloop()
    
if __name__ == "__main__":
    main()