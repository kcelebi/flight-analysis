'''/****************************************************************************************************************************************************************
  Written by Kaya Celebi, April 2023
****************************************************************************************************************************************************************/'''

import numpy as np
import pandas as pd
from tqdm import tqdm
from scrape import _Scrape
import json
import os

__all__ = ['CacheControl']

class _CacheControl:

	def __init__(self):
		self.directory = None

	def __call__(self, *args):
		self.directory = args[0]
		for obj in tqdm(args[1:], desc = "Caching Data"):
			if _CacheControl._check_scrape(obj):
				self.cache(obj)

	def __str__(self):
		return "Function to store scraped data."

	def __repr__(self):
		return "<Function to store scraped data: CacheControl>"

	def cache(self, obj):
		fname = self.directory + _CacheControl._get_file_name(obj.origin, obj.dest)

		df = obj.data
		# if fname exists blah blah blah
		#
		#
		
		df.to_csv(fname)


	'''
		Check that the scraping instance is valid
	'''
	@staticmethod
	def _check_scrape(arg):
		return isinstance(arg, _Scrape)

	'''
		Generate a filename given the object
	'''
	@staticmethod
	def _get_file_name(airport1, airport2):
		# create filename by alphabetical of 2 airports, regardless of origin or dest
		airports = sorted([airport1, airport2])
		return "{}-{}.csv".format(*airports)



CacheControl = _CacheControl()