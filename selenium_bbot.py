import multiprocessing
import time as timer
import tkinter as tk
#from pathos.multiprocessing import ProcessPool
from multiprocess import Process
from datetime import datetime
from tkinter.constants import BOTTOM, BROWSE, LEFT, RIGHT, TOP
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pathos.helpers import freeze_support

chromedriver_path = r"C:\Users\Annihilat0R\Downloads\chromedriver_win32\chromedriver.exe"
MIDNIGHT = "00:02:00"
COURT_ORDER = [3, 4, 1, 2, 5, 6]
COURT_TO_XPATH = {
    "1600-1700 court 1": "tr[50]/td[10]",
    "1600-1700 court 2": "tr[51]/td[9]",
    "1600-1700 court 3": "tr[52]/td[9]",
    "1600-1700 court 4": "tr[53]/td[9]",
    "1600-1700 court 5": "tr[54]/td[9]",
    "1600-1700 court 6": "tr[55]/td[9]",
    "1700-1800 court 1": "tr[56]/td[10]",
    "1700-1800 court 2": "tr[57]/td[9]",
    "1700-1800 court 3": "tr[58]/td[9]",
    "1700-1800 court 4": "tr[59]/td[9]",
    "1700-1800 court 5": "tr[60]/td[9]",
    "1700-1800 court 6": "tr[61]/td[9]",
    "1800-1900 court 1": "tr[62]/td[10]",
    "1800-1900 court 2": "tr[63]/td[9]",
    "1800-1900 court 3": "tr[64]/td[9]",
    "1800-1900 court 4": "tr[65]/td[9]",
    "1800-1900 court 5": "tr[66]/td[9]",
    "1800-1900 court 6": "tr[67]/td[9]"
}
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
        if self.user_listbox.get(self.user_listbox.curselection()) == "DEBUGGER":
            user = user_database["YX"]
            self.debugger_mode = True
        else:
            user = user_database[self.user_listbox.get(self.user_listbox.curselection())]
        timing = self.timing_listbox.get(self.timing_listbox.curselection())


        process_1 = Process(target=new_window, args=(user, 3, timing,))
        process_2 = Process(target=new_window, args=(user, 2, timing,))
        process_3 = Process(target=new_window, args=(user, 4, timing,))

        process_1.start()
        process_2.start()
        process_3.start()

        process_1.join()
        process_2.join()
        process_3.join()

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
       

def new_window(username, court_number, timing):
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
    
    north_hill_court = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, 
        "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[1]/td/input"))
    ).click()

    key = timing + " court " + str(court_number)
    element = COURT_TO_XPATH[key]
    court_button = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, 
        "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/table[2]/tbody/{}/input".format(element)))
    ).click()      

    confirm_book_button = WebDriverWait(driver, 65).until(EC.element_to_be_clickable((By.XPATH, 
        "//*[@id='top']/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/input[18]"))
    ).click()  

def main():
    root = tk.Tk()
    root.geometry("600x369")
    root.configure(bg='grey')
    app = App(root)
    app.mainloop()
    
if __name__ == "__main__":
    #from pathos.helpers import freeze_support
    #freeze_support()
    main()