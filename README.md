[![Build Status](https://travis-ci.org/kcelebi/Flight_Analysis.svg?branch=main)](https://travis-ci.org/kcelebi/Flight_Analysis)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Flight Price Analysis

Uses selenium and Python to scrape Google Flights data for analysis. One can use this repo to find the best flights according to some constraints (date, location, price min/max). One can also use this repo for general analysis regarding flights.

## Table of Contents
- [Overview](#Overview)
- [Usage](#usage)
- [Cache Data](#cache-data)
- [Real Usage](#real-usage) 😄


## Overview

Flight price calculation can either use newly scraped data (scrapes upon running it) or cached data that reports a price-change confidence determined by a trained model. Currently, many features of this application are in development. You can find updates and use some of the functionalities online [here](https://kayacelebi.shinyapps.io/flight_analysis_app/).

## Usage

The web scraping tool is currently functional only for scraping round trip flights for a given origin, destination, and date range. It can be easily used in a script or a jupyter notebook.

Note that the following packages are **absolutely required** as dependencies:
- tqdm
- selenium (make sure to update your [chromedriver](https://chromedriver.chromium.org)!)
- json

The main scraping function that makes up the backbone of most other functionalities is `scrape_data`. Note that the `cache` parameter refers to whether this output should be saved in a caching system. See [caching](#cache-data).

	# Parameter documentation
	# scrape_data(origin : str, destination : str, date_leave : str, date_return : str, cache : bool = False) -> dict
	# Try to keep the dates in format YYYY-mm-dd
	
	result = scrape_data('JFK', 'IST', '2022-05-20', '2022-06-10')
	
	# Can also input list of date strings for date_leave and date_return
	
	leave_dates = ['2022-05-20', '2022-05-21', '2022-05-22']
	return_dates = ['2022-06-10', '2022-06-11', '2022-06-12']
	range_result = scrape_data('JFK', 'IST', leave_dates, return_dates)


<!--## To Do

- [x] Scrape data and clean it
- [x] Testing for scraping
- [x] Add scraping docs
- [ ] Split Airlines
- [ ] Add day of week as a feature
- [ ] Support for Day of booking!! ("Delayed by x hr")
- [ ] Detail most common airports and automatically cache
- [ ] Algorithm to check over multiple days and return summary
- [x] Determine caching method: wait for request and cache? periodically cache?
- [ ] Model for observing change in flight price
	- Predict how much it'll maybe change
- [ ] UI for showing flights that are 'perfect' to constraint / flights that are close to constraints, etc
- [ ] Caching/storing data, uses predictive model to estimate how good this is

-->
## Real Usage

Here are some great flights I was able to find and actually booked when planning my travel/vacations:

- NYC ➡️ AMS (May 9), AMS ➡️ IST (May 12), IST ➡️ NYC (May 23) | Trip Total: $611 as of March 7, 2022
