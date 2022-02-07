## selenium_bbot
INSTALLATION GUIDE:
Install and extract the python file selenium_bbot. Alternatively, clone this repository.
In terminal window, navigate to the project folder and run the following command

  -pip install -r requirements.txt
  
# IMPORTANT:
It is recommended to monitor the bot in case something goes wrong. \n
During midnight, the servers run at a very slow rate. If it takes more than 7 seconds to load the court page, manually refresh the page.
Check the MIDNIGHT variable is set correctly to 00:00:00. This variable decides when the page is loaded.

# selenium_bbot auto
Run this python file for a hands free booking. Use this with task scheduler. 
Key in your login details by changing the USERNAME and PASSWORD variable.

# deprecated
download chrome driver with the link: https://chromedriver.chromium.org/downloads
to check google chrome version, click the 3 dots on the top right corner of chrome->help->About Google Chrome. It should be version 92
extract the chrome driver in the dafault download directory
copy the full file directory and paste it into selenium_bbot, line 12 where chromedriver_path = r"...". remember the .exe at the end
