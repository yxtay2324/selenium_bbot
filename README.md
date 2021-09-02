# selenium_bbot
THINGS TO NOTE:
It is recommended to monitor the bot in case something goes wrong.
During midnight, the servers run at a very slow rate. If it takes more than 7 seconds to load the court page, manually refresh the page. 

INSTALLATION GUIDE
Install and extract the python file selenium_bbot
run cmd and the following commands
  -pip install selenium
  -pip install multiprocess
download chrome driver with the link: https://chromedriver.chromium.org/downloads
to check google chrome version, click the 3 dots on the top right corner of chrome->help->About Google Chrome. It should be version 92
extract the chrome driver in the dafault download directory
copy the full file directory and paste it into selenium_bbot, line 12 where chromedriver_path = r"...". remember the .exe at the end

To run selenium_bbot, double click the python file. You should see the main page with user and timing option
