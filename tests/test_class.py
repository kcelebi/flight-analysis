import pytest
from pathlib import Path
#from src.scraping import *
from src.scrape_dev import *

def func_0():
	return True

def func_1():
	return Scrape("LGA", "RDU", "2023-05-15", "2023-06-15")

def func_2():
	return Scrape("IST", "CDG", "2023-07-15", "2023-07-20")

func1res = func_1()
func2res = func_2()

def test_0():
	assert func_0(), "Test 0 Failed"

def test_1():
	assert func1res.data.shape[0] > 0, "Test 1 Failed."

def test_2():
	assert func1res.origin == "LGA", "Test 2 Failed."

def test_3():
	assert func1res.dest == "RDU", "Test 3 Failed."

def test_4():
	assert func1res.date_leave == "2023-05-15", "Test 4 Failed."

def test_5():
	assert func1res.date_return == "2023-06-15", "Test 5 Failed."

def test_6():
	assert func2res.date.shape[0] > 0, "Test 6 Failed".

def test_7():
	assert func2res.origin == "IST", "Test 7 Failed".

def test_8():
	assert func2res.dest == "CDG", "Test 8 Failed".

def test_9():
	assert func2res.date_leave == "2023-07-15", "Test 9 Failed."

def test_10():
	assert func2res.date_return == "2023-07-20", "Test 10 Failed."