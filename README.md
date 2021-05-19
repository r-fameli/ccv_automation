# ccv_automation

An automation script created using Python and Selenium for automating account creation

## Required Installations
Utilizes Python 3 and requires Selenium for Python. This can usually be installed by `python -m pip install selenium` if you have `pip`.
This script requires web drivers for the browser you choose (either Chrome or Firefox), use `pip install webdriver-manager` to install the webdriver manager that will handle this process.

## How to Run
* Clone the code from this repository
* Navigate to the automation-script folder that this is in using your terminal
* Run `python main.py` (alternatively, `python3 main.py` depending on your Python setup)
* Choose your browser using the prompt (either Chrome or Firefox)
    * _Note: Currently, ChromeDriver will spam with unnecessary errors soon after the web driver installs, so this may obscure some of the prompts. For this reason, Firefox is recommended._
* A web browser will open up. Do not interact with anything in the opened browser unless there is a step that requires manual login or two-factor authentication (i.e. Brown logins). The script will only open pages for steps that it can automate
    * _Note: If you would like to see the browser operations in action, move the terminal to one side of the screen and the browser to the other so that neither is obscured. _

## Current Features
* Provides reminders for Google Sheets and other tasks
* Waits for script user to log in manually
* Adds user to CCV and CCV_ANNOUNCE lists in listserv
* Adds user to Brown:Services:HPC group in Grouper
* Generates HTML of email to send to user

## Known Problems
* Has not been tested on non-Windows machines
* Code will have to be reworked if any of the websites involved update their structure, as it relies on the current HTML

## Potential future features
* Connect to Google Sheets API to allow for automatic insertion into the Google Sheet
* Automate inserting batch file text into Webmin - WIP
* Scrape from Deskpro / automatically insert into Deskpro for retrieving/sending information to/from users
