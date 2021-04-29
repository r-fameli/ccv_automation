# ccv_automation

An automation script created using Python and Selenium for automating account creation

## Required Installations
Utilizes Python 3 and requires Selenium for Python. This can usually be installed by `python -m pip install selenium` if you have `pip`.
To install the web driver for Firefox, use `pip install webdriver-manager`. If the script is not able to install geckodriver using webdriver manager, (install geckodriver here)[https://github.com/mozilla/geckodriver/releases]



Currently uses the latest ChromeDriver to do the tasks in Google Chrome. [Download ChromeDriver 90 here](https://sites.google.com/chromium.org/driver/). 

## How to Run
* Clone the code from this repository
* Navigate to the automation-script folder that this is in using your terminal
* Run `python ticket_script.py` (alternatively, `python3 ticket_script.py` depending on your Python setup)
* A Firefox browser will open up. Do not change anything in the browser unless there is a step that requires manual login. The script will only open pages for steps that it can automate

## Current Features
* Provides reminders for Google Sheets and other tasks
* Allows automatic login to services or waits for manual log in
* Add user to CCV and CCV_ANNOUNCE lists in listserv
* Add user to Brown:Services:HPC group in Grouper

## Known Problems
* No way to update passwords if they are input incorrectly on startup
* Likely will only work on Windows machines
* Code will have to be reworked if any of the websites involved update their structure, as it relies on the current HTML

## Potential future features
* Connect to Google Sheets API to allow for automatic insertion into the Google Sheet
* Automate inserting batch file text into Webmin (will likely require refactoring for use on Linux machines)
* Scrape from Deskpro / automatically insert into Deskpro for retrieving/sending information to/from users
