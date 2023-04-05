'''/****************************************************************************************************************************************************************
  Written by Kaya Celebi, April 2023
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

__all__ = ['CacheControl', 'Scrape']

class _CacheControl:
	...

class _Scrape:

	def __init__(self):
		self._origin = None
		self._dest = None
		self._date_leave = None
		self._date_return = None
		self._cache = None

	def __call__(self, *args):
		self._set_properties(*args)
		self._scrape_data()

	def __str__(self):
		return "{dl}: {org} --> {dest}\n{dr}: {dest} --> {org}".format(
			dl = self._date_leave,
			dr = self._date_return,
			org = self._origin,
			dest = self._dest
		)

	def __repr__(self):
		return "{dl}: {org} --> {dest}\n{dr}: {dest} --> {org}".format(
			dl = self._date_leave,
			dr = self._date_return,
			org = self._origin,
			dest = self._dest
		)

	'''
		Set properties upon scraper called.
	'''
	def _set_properties(self, *args):
		(
			self._origin, self._dest, self._date_leave,
			self._date_return, self._cache
		) = args

	@property
	def origin(self):
		return self._origin

	@origin.setter
	def origin(self, x : str) -> None:
		self._origin = x

	@property
	def dest(self):
		return self._dest

	@dest.setter
	def dest(self, x : str) -> None:
		self._dest = x

	@property
	def date_leave(self):
		return self._date_leave

	@date_leave.setter
	def date_leave(self, x : str) -> None:
		self._date_leave = x

	@property
	def date_return(self):
		return self._date_return

	@date_return.setter
	def date_return(self, x : str) -> None:
		self._date_return = x

	'''
		Scrape the object
	'''
	def _scrape_data(self):
		url = self._make_url()
		return self._get_results(url)


	def _make_url(self):
		return 'https://www.google.com/travel/flights?q=Flights%20to%20{dest}%20from%20{org}%20on%20{dl}%20through%20{dr}'.format(
			dest = self._dest,
			org = self._origin,
			dl = self._date_leave,
			dr = self._date_return
		)

	def _get_results(self, url):
		results = _Scrape._make_url_request(url)

		flight_info = _Scrape._get_info(results)
		parition = _Scrape._partition_info(flight_info)

		return parse_columns

	@staticmethod
	def _make_url_request(url):
		driver = webdriver.Chrome('/Users/kayacelebi/Downloads/chromedriver')
		driver.get(url)

		# Waiting and initial XPATH cleaning
		WebDriverWait(driver, timeout = 10).until(lambda d: len(_Scrape._get_flight_elements(d)) > 100)
		results = _Scrape._get_flight_elements(driver)

		driver.quit()

	@staticmethod
	def _get_flight_elements(driver):
		return driver.find_element(by = By.XPATH, value = '//body[@id = "yDmH0d"]').text.split('\n')

	@staticmethod
	def _get_info(result):
		info = []
		collect = False
		for r in result:
			if 'more flights' in r:
				collect = False

			if collect and 'price' not in r.lower() and 'prices' not in r.lower() and 'other' not in r.lower() and ' – ' not in r.lower():
				info += [r]

			if r == 'Sort by:':
				collect = True

		return info

	@staticmethod
	def _partition_info(info):
		...


CacheControl = _CacheControl()
Scrape = _Scrape()