'''/****************************************************************************************************************************************************************
  Written by Kaya Celebi, April 2023
****************************************************************************************************************************************************************/'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import os

__all__ = ['CacheControl']

class _CacheControl:

	def __init__(self):
		...

	def __call__(self):
		...

	def __str__(self):
		...

	def __repr__(self):
		...

CacheControl = _CacheControl()