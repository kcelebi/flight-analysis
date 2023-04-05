'''/****************************************************************************************************************************************************************
  Author:
  Kaya Celebi

  Written by Kaya Celebi, March 2022
****************************************************************************************************************************************************************/'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import date, datetime, timedelta
from typing import overload
import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import os


__all__  = ['scrape_data', 'make_url', 'cache_data', 'iterative_caching', 'load_cached', 'clean_cache']


'''
***********************************************
##################  CACHING  ##################
***********************************************
'''

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

    Function saves file with name "../flight_analysis_app/cached/origin_dest_dateleave_datereturn.json"
'''
def cache_data(data : dict, origin : str, dest : str) -> None:
	file_name = make_filename(origin = origin, dest = dest)

	if file_name in os.listdir('../flight_analysis_app/cached'):
		old_data = load_cached(origin = origin, dest = dest, return_df = False)

		for key in list(old_data.keys()):
			last_index = int(list(old_data[key].keys())[-1]) + 1
			for idx, val in enumerate(data[key]):
				old_data[key][last_index + idx] = val

		data = old_data

	file = open('../flight_analysis_app/cached/' + file_name, 'w')

	json.dump(data, file)

	file.close()


'''
    Load cached data.

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
    
    Returns:
        Dictionary with column name as key and cleaned column as value loaded from cache.

'''
def load_cached(origin : str, dest : str, return_df : bool = False):
    file = open('../flight_analysis_app/cached/' + make_filename(origin, dest), 'r')
    data = json.load(file)
    file.close()
    return pd.DataFrame(data) if return_df else data


'''
    Iteratively search through different departure and arrival dates for flights from a given origin
    and destination. Caches all results.

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return
        width : no. of days to search before and after departure and arrival date

    Returns:
        None, stores data into cache
'''
def iterative_caching(origin : str, dest : str, date_leave : str, date_return : str, width : int) -> None:
    date_format = '%Y-%m-%d'
    d_leave_ = []
    d_return_ = []
    for i in tqdm(range(-1*width, width), desc = 'Make URLs'):
        for j in range(-1*width, width):
            d_leave = datetime.strftime(datetime.strptime(date_leave, date_format) + timedelta(i), date_format)
            d_return = datetime.strftime(datetime.strptime(date_return, date_format) + timedelta(j), date_format)

            if d_leave < d_return:
                d_leave_ += [d_leave]
                d_return_ += [d_return]

    scrape_data(origin = origin, dest = dest, date_leave = d_leave_, date_return  = d_return_, cache = True)


'''
    Clean duplicate observations in cached data.
'''
def clean_cache() -> None:
    for file in tqdm(os.listdir('../flight_analysis_app/cached/')):
        if file[-4:] == 'json':
            df = load_cached(origin = file.split('_')[0], dest = file.split('_')[1][:-5], return_df = True)

            data = df.loc[df[['Leave Date', 'Return Date', 'Access Date', 'Depart Time (Leg 1)', 'Arrival Time (Leg 1)']].astype(str).drop_duplicates().index].to_dict()
            f = open('../flight_analysis_app/cached/' + file, 'w')
            json.dump(data, f)
            f.close()


def cache_condition(df : pd.DataFrame, date_leave : str, date_return : str) -> bool:
    today_date = date.today().strftime('%Y-%m-%d')

    if today_date not in df['Access Date']:
        return False

    if df[(df['Leave Date'] == date_leave) & (df['Return Date'] == date_return)].empty:
        return False

    return True

'''
    Check whether a given request has been cached or not.
'''
@overload
def check_cached(origin : str, dest : str, date_leave : str, date_return : str) -> bool:
    ...

@overload
def check_cached(origin : str, dest : str, date_leave : list, date_return : list) -> list:
    ...

'''
    Overloaded check_cached function. Either checks condition for one or 
    a list of requests.
'''
def check_cached(origin : str, dest : str, date_leave, date_return):
    '''
        Checking by filename
    '''
    file_name = make_filename(origin = origin, dest = dest)
    if file_name not in os.listdir('../flight_analysis_app/cached/'):
        return False

    df = load_cached(origin = origin, dest = dest, return_df = True)

    '''
        Checking only one request
    '''
    if isinstance(date_leave, str) and isinstance(date_return, str):
        return cache_condition(df = df, date_leave = date_leave, date_return = date_return)

    '''
        Checking all requests
    '''
    if isinstance(date_leave, list) and isinstance(date_return, list):
        return np.all([cache_condition(df = df, date_leave = date_leave[i], date_return = date_return[i]) for i in range(len(date_leave))])



'''
************************************************
##################  SCRAPING  ##################
************************************************
'''


'''
    Scrapes data from Google Flights using Selenium. Cleans, filters data and returns as pandas dataframe or dictionary.

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return

    Returns:
        Dictionary of columns
'''
@overload
def scrape_data(origin : str, dest : str, date_leave : str, date_return : str, cache : bool = False):
    ...
    '''data = None

    # if request has already been cached
    if make_filename(origin, dest) in os.listdir('../cached/'):
        data = load_cached(origin = origin, dest = dest)
        df = pd.DataFrame(data)

        # check that date + access date haven't been recorded, if so then scape it from website
        # otherwise, just load the dataframe from cache
        if df[(df['Leave Date'] == date_leave) & (df['Return Date'] == date_return)].empty or date.today().strftime('%Y-%m-%d') not in data['Access Date']:
            url = make_url(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
            new_data = get_results(url)

            for i in range(len(data.keys())):
                data[list(data.keys())[i]] += new_data[list(data.keys())[i]]

        else:
            print('Pulled from cache')

    else: #new, unseen request
        url = make_url(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)
        data = get_results(url)

    if cache:
        cache_data(data, origin, dest)

    return data'''

@overload
def scrape_data(origin : str, dest : str, date_leave : list, date_return : list, cache : bool = False) -> dict:
    ...

'''
    Overloaded scrape_data function, either scrapes list of urls or single url.
'''
def scrape_data(origin, dest, date_leave, date_return, cache = False) -> dict:
    '''
        Scraping multiple urls
    '''
    if isinstance(date_leave, list) and isinstance(date_return, list):
        # Construct list of urls
        url = [make_url(origin = origin, dest = dest, date_leave = date_leave[i], date_return = date_return[i]) for i in range(len(date_leave))]
        
        # Get the data of urls
        data = get_results(url = url, origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)

        # Cache them
        if cache:
            cache_data(data = data, origin = origin, dest = dest)

        return data

    '''
        Scraping single url
    '''
    if isinstance(date_leave, str) and isinstance(date_return, str):
        # Construct one url
        url = make_url(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)

        # Get the data
        data = get_results(url = url, origin = origin, dest = dest, date_leave = date_leave, date_return = date_return)

        # Cache it
        if cache:
            cache_data(data = data, origin = origin, dest = dest)

        return data

    else:
        raise WrongTypeError('Incorrect types provided')

'''
    Construct file name for caching

    Args:
        origin : Airport code of origin
        dest : Airport code of destination
        date_leave : Date of departure
        date_return : Date or return

    Returns:
        Filename of format "{origin}_{dest}.json"
'''
def make_filename(origin : str, dest : str) -> str:
    return '{}_{}.json'.format(origin, dest)

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
def make_url(origin : str, dest : str, date_leave : str, date_return : str) -> str:
    base = 'https://www.google.com/travel/flights?q=Flights%20to%20{}%20from%20{}%20on%20{}%20through%20{}'
    return base.format(dest, origin, date_leave, date_return)

'''
    Given Selenium driver, locates flight information by XPATH query.

    Args:
        d : Selenium driver object

    Returns:
        1D Array of results with flight information and some superfluous information (hotels, links, etc).
'''
def get_flight_elements(d) -> list:
    return d.find_element(by = By.XPATH, value = '//body[@id = "yDmH0d"]').text.split('\n')

'''
    Make URL request to Google Flights and collect info using XPATH query.

    Args:
        url : URL to make request designed for given origin and destination

    Returns:
        XPATH query result
'''
def make_url_request(url : str) -> list:
    ...

def make_url_request(url : list) -> list:
    ...

def make_url_request(url):
    if isinstance(url, str):
        # Instantiate driver and get raw data
        driver = webdriver.Chrome('/Users/kayacelebi/Downloads/chromedriver')
        driver.get(url)

        # Waiting and initial XPATH cleaning
        WebDriverWait(driver, timeout = 10).until(lambda d: len(get_flight_elements(d)) > 100)
        results = get_flight_elements(driver)

        driver.quit()

    if isinstance(url, list):
        # Instantiate driver
        driver = webdriver.Chrome('/Users/kayacelebi/Downloads/chromedriver')

        # Begin getting results for each url
        results = []
        for u in tqdm(url, desc = 'Data Scrape'):
            driver.get(u)

            try:
                WebDriverWait(driver, timeout = 30).until(lambda d: len(get_flight_elements(d)) > 100)
                results += [get_flight_elements(driver)]
            except:
                print('Timeout exception')

        driver.quit()

    return results
'''
    Uses Selenium to access Google Flights and grab results.

    Args:
        url : URL string of Google Flights page

    Returns:
        1D Array of results with flight information and some superfluous information (hotels, links, etc).
'''
@overload
def get_results(url: str) -> list:
    ...

@overload
def get_results(url: list) -> list:
    ...

'''
    Overloaded get_results function. Returns result for list of urls or single url.
'''
def get_results(url, origin, dest, date_leave, date_return):
    '''
        Return results for single url
    '''
    if isinstance(url, str) and isinstance(date_leave, str) and isinstance(date_return, str):

        if check_cached(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return):
            return load_cached(origin = origin, dest = dest)
        else:
            # Make URL request
            results = make_url_request(url = url)

            # Data cleaning
            flight_info = get_info(results) # First, get relevant results
            partition = partition_info(flight_info) # Partition list into "flights"

            return parse_columns(partition, date_leave, date_return) # "Transpose" to data frame

    '''
        Return results for list of urls
    '''
    if isinstance(url, list) and isinstance(date_leave, list) and isinstance(date_return, list):
        if check_cached(origin = origin, dest = dest, date_leave = date_leave, date_return = date_return):
            return load_cached(origin = origin, dest = dest)

        results = make_url_request(url = url)

        # Blank data frame to append results to.
        df = {
            'Leave Date' : [],
            'Return Date' : [],
            'Depart Time (Leg 1)' : [],
            'Arrival Time (Leg 1)' : [],
            'Airline(s)' : [],
            'Travel Time' : [],
            'Origin' : [],
            'Destination' : [],
            'Num Stops' : [],
            'Layover Time' : [],
            'Stop Location' : [],
            'CO2 Emission' : [],
            'Emission Avg Diff (%)' : [],
            'Price ($)' : [],
            'Trip Type' : [],
            'Access Date' : []
        }
        '''
            Clean the data and add individually to bigger dataframe
        '''
        for i, res in enumerate(results):
            flight_info, partition, new_data = None, None, None

            # Get relevant information
            try:
                flight_info = get_info(res)
            except:
                print('get_info() has an issue', date_leave[i], date_return[i])

            # Partition into "flights"
            try:
                partition = partition_info(flight_info)
            except:
                print('partition_info() has an issue', date_leave[i], date_return[i])

            # "Transpose" to data frame
            try:
                new_data = parse_columns(partition, date_leave[i], date_return[i])
            except:
                print('parse_columns() has an issue', date_leave[i], date_return[i])

            # Append data frame columns to bigger data frame
            try:
                for key in df.keys():
                    df[key] += new_data[key]
            except:
                print('Adding df to main df has an issue', date_leave[i], date_return[i])

        return df



'''
************************************************
##################  CLEANING  ##################
************************************************
'''


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
    if len(x) < 2:
        return False

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
            j += 1 

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
def parse_columns(grouped, date_leave, date_return):
    # Instantiate empty column arrays
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

    # For each "flight"
    for g in grouped:
        i_diff = 0 # int that checks if we need to jump ahead based on some conditions

        # Get departure and arrival times
        depart_time += [g[0]]
        arrival_time += [g[1]]

        # When this string shows up we jump ahead an index
        i_diff += 1 if 'Separate tickets booked together' in g[2] else 0

        # Add airline, travel time, origin, and dest
        airline += [g[2 + i_diff]]
        travel_time += [g[3 + i_diff]]
        origin += [g[4 + i_diff].split('–')[0]]
        dest += [g[4 + i_diff].split('–')[1]]
        
        # Grab the number of stops by splitting string
        num_stops = 0 if 'Nonstop' in g[5 + i_diff] else int(g[5 + i_diff].split('stop')[0])
        stops += [num_stops]

        # Add stop time/location given whether its nonstop flight or not
        stop_time += [None if num_stops == 0 else (g[6 + i_diff].split('min')[0] if num_stops == 1 else None)]
        stop_location += [None if num_stops == 0 else (g[6 + i_diff].split('min')[1] if num_stops == 1 and 'min' in g[6 + i_diff] else [g[6 + i_diff].split('hr')[1] if 'hr' in g[6 + i_diff] and num_stops == 1 else g[6 + i_diff]])]
        
        # Jump ahead an index if flight isn't nonstop to accomodate for stop_time, stop_location
        i_diff += 0 if num_stops == 0 else 1

        # If Co2 emission not listed then we skip, else we add
        if g[6 + i_diff] != '–':
            co2_emission += [float(g[6 + i_diff].replace(',','').split(' kg')[0])]
            emission += [0 if g[7 + i_diff] == 'Avg emissions' else int(g[7 + i_diff].split('%')[0])]

            price += [float(g[8 + i_diff][1:].replace(',',''))]
            trip_type += [g[9 + i_diff]]
        else:
            co2_emission += [None]
            emission += [None]
            price += [float(g[7 + i_diff][1:].replace(',',''))]
            trip_type += [g[8 + i_diff]]

       
    
    return {
        'Leave Date' : [date_leave]*len(grouped),
        'Return Date' : [date_return]*len(grouped),
        'Depart Time (Leg 1)' : depart_time,
        'Arrival Time (Leg 1)' : arrival_time,
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

