# ccv_automation

An automation script created using Python and Selenium for automating account creation

## Required Installations
Requires Selenium for Python. This can usually be installed by `python -m pip install selenium`.  
Currently uses the latest ChromeDriver to do the tasks in Google Chrome. [Download ChromeDriver 90 here](https://sites.google.com/chromium.org/driver/). 

## Current Supported Tasks
* Add user to CCV and CCV_ANNOUNCE lists in listserv
* Add user to Brown:Services:HPC group in Grouper

## Known Bugs
* Currently only works if you input your password in correctly the first time
* Likely will only work on Windows machines

## Potential future features
* Ask for you to add to Google Sheets, etc. (remind you of the steps that are currently not automated)
* Generate email message to send back to user with information 
* Connect to Google Sheets API to allow for automatic insertion into the Google Sheet
* Automate inserting batch file text into Webmin (will likely require refactoring for use on Linux machines)
* Scrape from Deskpro / automatically insert into Deskpro for retrieving/sending information to/from users
