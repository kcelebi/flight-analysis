[![Build Status](https://travis-ci.org/kcelebi/Flight_Analysis.svg?branch=main)](https://travis-ci.org/kcelebi/Flight_Analysis)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Flight Price Analysis

Uses selenium and Python to scrape Google Flights data for analysis. One can use this repo to find the best flights according to some constraints (date, location, price min/max). One can also use this repo for general analysis regarding flights.

## Table of Contents
- [Overview](#Overview)
- [To Do](#to-do)
- [Real Usage](#real-usage) 😄


## Overview

Flight price calculation can either use newly scraped data (scrapes upon running it) or cached data that reports a price-change confidence determined by a trained model.


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
