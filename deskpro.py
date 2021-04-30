import ticket_script
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

def retrieve_from_deskpro(driver, ticket_id):
    driver.get("https://ithelp.brown.edu/agent/")

    # ensure that only one ticket is open
    tabs_open = driver.find_elements_by_xpath("//a[@class='ng-binding']").length
    if tabs_open != 0:
        # Right click the tabs bar and close all tabs
        print("Closing Deskpro tabs")
        tabs_bar = driver.find_element_by_xpath("//div[@class='deskproTabListInner ng-isolate-scope']")
        ActionChains(driver).context_click(tabs_bar)
        driver.find_element_by_xpath("//a[@ng-click='closeAll()']").click()
    
    ticket_message = driver.find_elements_by_xpath("//div[@class='body-text-message unreset']")[-1]
    

    
    

