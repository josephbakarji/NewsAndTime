import os
import urllib.request
from http.client import IncompleteRead


def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)


def PageExists(page):
	return (page != 404) and (page != 410) 


def DateList(start_date, end_date):
	DateArray = []
	if(type(start_date) == str):
		start_year = int(start_date[0:4])
		start_month = int(start_date[4:])
		end_year = int(end_date[0:4])
		end_month = int(end_date[4:])
	elif(type(start_date) == list):
		start_year = start_date[0]
		start_month = start_date[1]
		end_year = end_date[0]
		end_month = end_date[1]

	y = start_year
	m = start_month
	while(1):
		DateArray.append([y,m])
		if(y >= end_year and m >= end_month):
			break

		if (m==12):
			m = 1
			y = y + 1
		else:
			m = m + 1

	return DateArray



def UrlRequest(URL):
	try:
		try:
			page = urllib.request.urlopen(URL).read()
		except IncompleteRead as e:
			page = e.partial
	except urllib.request.HTTPError as g:
		return g.code

	return page



def FileNotinDir(path, filename):
	flag = 1
	for files in os.listdir(path):
		if files == filename:
			flag = 0
			break
	return flag
