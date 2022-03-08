'''/****************************************************************************************************************************************************************
  Author:
  Kaya Celebi

  Written by Kaya Celebi, March 2022
****************************************************************************************************************************************************************/'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import date
import numpy as np
import pandas as pd
import json
import os


__all__  = ['scrape_data', 'make_url', 'cache_data']

'''
    Performs search and stores data into a JSON file for easy retrieval. 
    Keys are origin, destination, date leave and return, and date accessed.

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return

    Returns:
        None

    Function saves file with name "../cached/origin_dest_dateleave_datereturn.json"
'''
def cache_data(data, origin, dest, date_leave, date_return):
    #data = scrape_data(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return, return_df = False)

    file_name = make_filename(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
    file = open('../cached/' + file_name, 'w')
    json.dump(data, file)

    file.close()

    print('%s created' % file_name)

def load_cached(origin, dest, date_leave, date_return):
    return json.load(open('../cached/' + make_filename(origin, dest, date_leave, date_return), 'r'))

'''
    Scrapes data from Google Flights using Selenium. Cleans, filters data and returns as pandas dataframe or dictionary.

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return
        return_df : Whether to return as pandas df or dictionary

    Returns:
        pandas df or dictionary of columns
'''
def scrape_data(origin, dest, date_leave, date_return, return_df = True, cache = False):
    data = None

    if make_filename(origin, dest, date_leave, date_return) in os.listdir('../cached/'):
        data = load_cached(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
        if date.today().strftime('%Y-%m-%d') not in data['Access Date']:
            url = make_url(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
            results = get_results(url)

            flight_info = get_info(results)
            partition = partition_info(flight_info)
            new_data = parse_columns(partition)

            for i in range(len(data.keys())):
                data[data.keys()[i]] += new_data[data.keys()[i]]

            print('Updated cache')

        else:
            print('Pulled from cache')

    else:
        url = make_url(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
        results = get_results(url)

        flight_info = get_info(results)
        partition = partition_info(flight_info)
        data = parse_columns(partition)

    if cache:
        cache_data(data, origin, dest, date_leave, date_return)

    if return_df:
        return pd.DataFrame(data)
    return data

'''
    Construct file name for caching

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return

    Returns:
        Filename of format "origin_dest_dateleave_datereturn.json"
'''
def make_filename(origin, dest, date_leave, date_return):
    date_leave = date_leave.replace('-', '')
    date_return = date_return.replace('-', '')
    return '{}_{}_{}_{}.json'.format(origin, dest, date_leave, date_return)

'''
    Using Google's query format to access the appropriate Google flights page.

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return

    Returns:
        URL string of appropriate Google Flights page.
'''
def make_url(origin, dest, date_leave, date_return):
    base = 'https://www.google.com/travel/flights?q=Flights%20to%20{}%20from%20{}%20on%20{}%20through%20{}'
    return base.format(dest, origin, date_leave, date_return)

'''
    Given Selenium driver, locates flight information by XPATH query.

    Args:
        d : Selenium driver object

    Returns:
        1D Array of results with flight information and some superfluous information (hotels, links, etc).
'''
def get_flight_elements(d):
    return d.find_element(by = By.XPATH, value = '//body[@id = "yDmH0d"]').text.split('\n')

'''
    Uses Selenium to access Google Flights and grab results.

    Args:
        url : URL string of Google Flights page

    Returns:
        1D Array of results with flight information and some superfluous information (hotels, links, etc).
'''
def get_results(url):
    driver = webdriver.Chrome('/Users/kayacelebi/Downloads/chromedriver')
    driver.get(url)

    WebDriverWait(driver, timeout = 10).until(lambda d: len(get_flight_elements(d)) > 100)
    results = get_flight_elements(driver)

    driver.quit()
    return results

'''
    Takes results from Selenium XPATH query and filters out unnecessary information.

    Args:
        res : 1D Array of results with flight information and some superfluous information

    Returns:
        1D Array of results with only flight information, unpartitioned.
'''
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

'''
    Boolean helper function for partition_info(). Determines where flight info observation begins/ends.
'''
def end_condition(x):
    if x[-2] == '+':
        x = x[:-2]
    
    if x[-2:] == 'AM' or x[-2:] == 'PM':
        return True
    return False


'''
    Partitions results from get_info() into flight observations. Uses end_condition() to know
    when to start/stop a new obsevation.

    Args:
        info : 1D Array of results with only flight information, unpartitioned.

    Returns:
        2D matrix of flight information where each observation is a 10 or 11 sized array. 
        Each observation is size 10 if nonstop flight and size 11 if multiple stops (additional
        feature is stop location(s)).
'''
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

'''
    Takes partitioned information and cleans data, conforming to appropriate type and setting up
    for conversion to a pandas dataframe.

    Args:
        grouped : partitioned flight information in 2D matrix

    Returns:
        Dictionary with column name as key and cleaned column as value.
'''
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
    access_date = [date.today().strftime('%Y-%m-%d')]*len(grouped)

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
        'Trip Type' : trip_type,
        'Access Date' : access_date
    }

