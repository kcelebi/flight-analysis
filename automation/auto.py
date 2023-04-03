import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sys.path.append('../src')
from scraping import *
import scraping


airport_list = [
	'JFK', 'LGA', 'RDU', 'IST', 'CDG', 'EWR', 'LHR', 'TPA', 'SAW'
]

same_city = {
	'New York': ['LGA', 'EWR', 'JFK'],
	'Istanbul': ['IST', 'SAW']
}

same_city_pairwise = {}
for key in same_city.keys():
	for val in same_city[key]:
		same_city_pairwise[val] = [x for x in same_city[key] if x != val]
		

print('Generating %d lists' % (len(airport_list)*2 - 2))
for i in airport_list:
	for j in airport_list:
		if i != j and j not in same_city_pairwise[i]:
			iterative_caching(i, j, '2022-11-10', '2022-12-10', 20)



