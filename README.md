[![kcelebi](https://circleci.com/gh/kcelebi/flight-analysis.svg?style=svg)](https://circleci.com/gh/kcelebi/flight-analysis)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live on PyPI](https://github.com/kcelebi/flight-analysis/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/kcelebi/flight-analysis/actions/workflows/publish.yml)

# Flight Analysis

This project provides tools and models for users to analyze, forecast, and collect data regarding flights and prices. There are currently many features in initial stages and in development. The current features (as of 8/29/22) are:

- Scraping tools for Google Flights
- Base analytical tools/methods for price forecasting/summary
- Models to demonstrate ML techniques on forecasting
- API for access to previously collected data

## Table of Contents
- [Overview](#Overview)
- [Usage](#usage)
- [Updates & New Features](#updates-&-new-features)
- [Real Usage](#real-usage) 😄


## Overview

Flight price calculation can either use newly scraped data (scrapes upon running it) or cached data that reports a price-change confidence determined by a trained model. Currently, many features of this application are in development.

## Usage

The web scraping tool is currently functional only for scraping round trip flights for a given origin, destination, and date range. It can be easily used in a script or a jupyter notebook.

Note that the following packages are **absolutely required** as dependencies:
- tqdm
- selenium (make sure to update your [chromedriver](https://chromedriver.chromium.org)!)
- json

You can easily install this by running `pip install -r requirements.txt`.

The main scraping function that makes up the backbone of most other functionalities is `scrape_data`. Note that the `cache` parameter refers to whether this output should be saved in a caching system. See further documentation on caching (to be available soon).

	# Parameter documentation
	# scrape_data(origin : str, destination : str, date_leave : str, date_return : str, cache : bool = False) -> dict
	# Try to keep the dates in format YYYY-mm-dd
	
	result = scrape_data('JFK', 'IST', '2022-05-20', '2022-06-10')
	
	# Can also input list of date strings for date_leave and date_return
	
	leave_dates = ['2022-05-20', '2022-05-21', '2022-05-22']
	return_dates = ['2022-06-10', '2022-06-11', '2022-06-12']
	range_result = scrape_data('JFK', 'IST', leave_dates, return_dates)
	
## Updates & New Features


<!--
## Cache Data

The caching system for this application is mainly designed to make the loading of data more efficient. For the moment, this component of the application hasn't been designed well for the public to easily use so I would suggest that most people leave it alone, or fork the repository and modify some of the functions to create folders in the destinations that they would prefer. The key caching functions are:

- `cache_data`
- `load_cached`
- `iterative_caching`
- `clean_cache`
- `cache_condition`
- `check_cached`

All of these functions are clearly documented in the `scraping.py` file.
-->
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
