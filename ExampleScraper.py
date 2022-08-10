import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import sys

def function(url, webdriver):
    url = 'https://proxy1.jpenergy.com/maps/OutageWebMap/'

    chrome_driver_path = "C:\\Users\eddyd\Pictures\CS\Downloads\chromedriver.exe"

    #make driver headless
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    webdriver = webdriver.Chrome(
        executable_path=chrome_driver_path, options=chrome_options
    )
    webdriver.get(url)

    #added delay to wait for website
    delay = 3
    try:
        myElem = WebDriverWait(webdriver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print("Page is ready!")
    except TimeoutException:
        print("")

    #path to the scrapable text
    outage_data = webdriver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div/div[3]/div/div[2]/div/div/div/div[2]/div/div/table/tbody[1]')

    name_list, final_output, temp2 = [], [], []
    name = ""
    num_outages, percent_outage, count = 0, 0, 0

    #scraping the site for text
    for outage in outage_data:
        temp = outage.text.strip().replace("%", "")
        temp2 = temp.split()
    for item in temp2:
        #formatting the text
        current = re.sub("[^.%a-zA-Z0-9]", "~", item)
        if "~" in current:
            temp2.remove(item)

    #adding text to list
    for i in range(len(temp2)):
        if i % 3 == 0:
            name = temp2[i]
        if i % 3 == 1:
            num_outages = temp2[i]
        if i % 3 == 2:
            percent_outage = temp2[i]
        name_list = [name, num_outages, percent_outage]
        count += 1
        if count % 3 == 0:
            #compiling final output
            final_output.append(name_list)
    return (final_output)
