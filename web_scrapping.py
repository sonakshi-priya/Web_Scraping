from selenium.webdriver.common import keys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import json

reservoirs = ["Harangi", "Hemavathi","K.R.S", "Kabini"]

weeks = list(range(1, 53))
weeks_str = [str(week) for week in weeks]

years = list(range(2010, 2021))
years_str = [str(year) for year in years]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# d = webdriver.Chrome(executable_path='C:\Program Files\Google\Chrome\Application\chrome.exe', options=chrome_options)
driver = webdriver.Chrome(r'C:\Users\sonak\Downloads\chromedriver_win32\chromedriver.exe')
driver.get("https://www.ksndmc.org/Reservoir_Details.aspx")
driver.implicitly_wait(30)
# try:
#     Reservoir_table = d.find_elements_by_path('')




class WebTable:
    # accept the web element (table) as parameter to then constructor
    def __init__(self, webTable):
        self.table = webTable

    def get_all_data(self):
        # get number of rows
        rows = driver.find_elements_by_xpath('//*[@id="ctl00_cpMainContent_GridView1"]//tr')
        noOfRows = len(rows)
        # get number of columns
        noOfColumns = len(self.table.find_elements_by_xpath("//tr[2]/td"))
        allData = []
        # iterate over the rows, to ignore the headers we have started the i with '1'
        for i in range(2, noOfRows + 1):
            # reset the row data every time
            ro = []
            # iterate over columns
            for j in range(1, noOfColumns) :
                # get text from the i th row and j th column
                ro.append(self.table.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text)

            # add the row data to allData of the self.table
            allData.append(ro)

        return allData

try:
    


    for reservoir in reservoirs:
        for year in years_str:
            for week in weeks_str:
                time.sleep(5)
                select_reservoir = Select(driver.find_element_by_id('ctl00_cpMainContent_DropDownList1'))
                select_year = Select(driver.find_element_by_id('ctl00_cpMainContent_Year_list'))
                select_week = Select(driver.find_element_by_id('ctl00_cpMainContent_weekList'))
                button = driver.find_element_by_id('ctl00_cpMainContent_Button1')
                # driver.implicitly_wait(5)
                
                # select by visible text
                print('Reservoir = ' + reservoir)
                select_reservoir.select_by_visible_text(reservoir)
                # driver.implicitly_wait(1)
                time.sleep(1)
                print('Year = ' + year)
                select_year.select_by_visible_text(year)
                # driver.implicitly_wait(1)
                time.sleep(1)
                print('Week = ' + week)
                select_week.select_by_visible_text(week)
                # driver.implicitly_wait(1)
                time.sleep(1)
                button.click()
                # driver.implicitly_wait(10)
                time.sleep(10)

                # Get Data
                webTable = WebTable(driver.find_element_by_xpath('//*[@id="ctl00_cpMainContent_GridView1"]'))
                data = webTable.get_all_data()
                print('Number of rows = ' + str(len(data)))
                filename = './data/' + reservoir + '_' + year + '_' + week + '.json'
                dataToWrite = {
                    'data': data
                }
                with open(filename, 'w') as fp:
                    json.dump(dataToWrite, fp)
    
except NoSuchElementException as e:
    print (e)


# driver = webdriver.Chrome(r"C:\Users\sonak\Downloads\chromedriver_win32")
# # driver.maximize_window()
# driver.get("https://www.google.com/")
# driver.find_element_by_name("q").send_keys("javatpoint")
# time.sleep(3)
# driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
# time.sleep(3)
# driver.close()
