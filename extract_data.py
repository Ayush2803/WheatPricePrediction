# MANUALLY SET THE DATE IN THE WEBDRIVER AND PRESS THE REFRESH BUTTON
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from datetime import date

states = {}


def get_states(site):
    driver = webdriver.Chrome('C:\\chromedriver')
    driver.get(site)
    driver.implicitly_wait(10)
    time.sleep(10)
    # SELECT WHEAT IN THE PAUSE TIME

    dropdown = Select(driver.find_element_by_id("min_max_state"))

    opt = dropdown.options
    n = len(opt)

    for i in range(n-1):
        dropdown.select_by_index(i)
        driver.implicitly_wait(10)
        state = dropdown.first_selected_option
        states[state.text] = i


def is_in(string, sub_str):
    if string.find(sub_str) == -1:
        return False
    else:
        return True


def mark1(site):
    driver = webdriver.Chrome('C:\\chromedriver')
    driver.get(site)
    driver.implicitly_wait(10)
    time.sleep(20)

    # MANUALLY SET THE MINIMUM DATE AVAILABLE IN THE FROM DATE
    start_date = date(2021, 8, 21)

    # MANUALLY SET UP THE DATE IN THE WEB DRVIER THAT OPENS UP

    dropdown = Select(driver.find_element_by_id("min_max_no_of_list"))
    min_prices = []
    max_prices = []
    modal_prices = []

    opt = dropdown.options
    n = len(opt)

    for i in range(n-1):
        dropdown.select_by_index(i)
        driver.implicitly_wait(1000)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        t_body = soup.find('tbody')
        rows = t_body.find_all('tr')

        for row in rows:
            Row = []
            cells = row.find_all('td')

            for cell in cells:
                Row.append(cell.text)

            if is_in(Row[2], "WHEAT") and Row[4] != '0':
                date_str = Row[-1].split('-')
                date_ = date(int(date_str[2]), int(
                    date_str[1]), int(date_str[0]))
                gap_ = date_-start_date
                gap = gap_.days

                min_prices.append(
                    [gap, states[Row[0]], int(Row[3].replace(',', ''))])
                modal_prices.append(
                    [gap, states[Row[0]], int(Row[4].replace(',', ''))])
                max_prices.append(
                    [gap, states[Row[0]], int(Row[5].replace(',', ''))])

    return min_prices, modal_prices, max_prices


str = 'https://enam.gov.in/web/dashboard/trade-data'
get_states(str)
min_, modal_, max_ = mark1(str)
min_data = np.array(min_)
modal_data = np.array(modal_)
max_data = np.array(max_)
min_df = pd.DataFrame(data=min_data, columns=['Day', 'State id', 'Min Price'])
min_df.to_csv(
    "D:\\Documents\\Python\\SystemOnSilicon Internship\\Wheat Price Prediction\\3 dimensional\\min_price_data.csv")
max_df = pd.DataFrame(data=max_data, columns=['Day', 'State id', 'Max Price'])
max_df.to_csv(
    "D:\\Documents\\Python\\SystemOnSilicon Internship\\Wheat Price Prediction\\3 dimensional\\max_price_data.csv")
modal_df = pd.DataFrame(data=modal_data, columns=[
                        'Day', 'State id', 'Modal Price'])
modal_df.to_csv(
    "D:\\Documents\\Python\\SystemOnSilicon Internship\\Wheat Price Prediction\\3 dimensional\\modal_price_data.csv")
with open('state_names.csv', 'w') as f:
    for key in states.keys():
        f.write("%s,%d\n" % (key, states[key]))
