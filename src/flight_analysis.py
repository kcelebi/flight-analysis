'''/****************************************************************************************************************************************************************
  Author:
  Kaya Celebi

  Written by Kaya Celebi, March 2022
****************************************************************************************************************************************************************/'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


__all__  = ['scrape_data']

def scrape_data(origin, dest, date_leave, date_return):
    url = make_url(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
    results = get_results(url)

    flight_info = get_info(results)
    partition = partition_info(flight_info)
    data = parse_columns(partition)

    return pd.DataFrame(data)


def make_url(origin, dest, date_leave, date_return):
    base = 'https://www.google.com/travel/flights?q=Flights%20to%20{}%20from%20{}%20on%20{}%20through%20{}'
    return base.format(dest, origin, date_leave, date_return)

def get_flight_elements(d):
    return d.find_element(by = By.XPATH, value = '//body[@id = "yDmH0d"]').text.split('\n')

def get_results(url):
    driver = webdriver.Chrome('/Users/kayacelebi/Downloads/chromedriver')
    driver.get(url)
    WebDriverWait(driver, timeout = 10).until(lambda d: len(get_flight_elements(d)) > 100)
    results = get_flight_elements(driver)
    driver.quit()
    return results

def get_info(res):
    info = []
    collect = False
    for r in res:

        if 'more flights' in r:
            collect = False

        if collect and 'price' not in r.lower() and 'prices' not in r.lower() and 'other' not in r.lower() and ' – ' not in r.lower():
            info += [r]

        if r == 'Sort by:':
            collect = True
            
    return info

def end_condition(x):
    if x[-2] == '+':
        x = x[:-2]
    
    if x[-2:] == 'AM' or x[-2:] == 'PM':
        return True
    return False

def partition_info(info):
    i=0
    grouped = []
    while i < len(info)-1:
        j = i+2
        end = -1
        while j < len(info):
            if end_condition(info[j]):
                end = j
                break
            j +=1 

        #print(i, end)
        if end == -1:
            break
        grouped += [info[i:end]]
        i = end
        
    return grouped


def parse_columns(grouped):
    depart_time = []
    arrival_time = []
    airline = []
    travel_time = []
    origin = []
    dest = []
    stops = []
    stop_time = []
    stop_location = []
    co2_emission = []
    emission = []
    price = []
    trip_type = []

    for g in grouped:
        depart_time += [g[0]]
        arrival_time += [g[1]]
        airline += [g[2]]
        travel_time += [g[3]]
        origin += [g[4].split('–')[0]]
        dest += [g[4].split('–')[1]]
        
        num_stops = 0 if 'Nonstop' in g[5] else int(g[5].split('stop')[0])
        stops += [num_stops]

        stop_time += [None if num_stops == 0 else (g[6].split('min')[0] if num_stops == 1 else None)]
        stop_location += [None if num_stops == 0 else (g[6].split('min')[1] if num_stops == 1 else g[6])]
        
        i_diff = 0 if num_stops == 0 else 1
        
        co2_emission += [float(g[6 + i_diff].replace(',','').split(' kg')[0])]
        emission += [0 if g[7 + i_diff] == 'Avg emissions' else int(g[7 + i_diff].split('%')[0])]
        
        price += [float(g[8 + i_diff][1:].replace(',',''))]
        
        trip_type += [g[9 + i_diff]]
    
    return {
        'Depart Time' : depart_time,
        'Arrival Time' : arrival_time,
        'Airline(s)' : airline,
        'Travel Time' : travel_time,
        'Origin' : origin,
        'Destination' : dest,
        'Num Stops' : stops,
        'Layover Time' : stop_time,
        'Stop Location' : stop_location,
        'CO2 Emission' : co2_emission,
        'Emission Avg Diff (%)' : emission,
        'Price ($)' : price,
        'Trip Type' : trip_type
    }

