import urllib.request
import json
import datetime
from http.client import IncompleteRead
import time
import os


# Example: https://api.nytimes.com/svc/archive/v1/2004/2.json?api-key=c969986d00bd44eebdc3546f365121cc

# start_date and end_date format is "YYYYMM", type: string
def NYTmetaquery(start_date, end_date) :

	DateArray = DateList(start_date, end_date)

	path = "./archive/"
	apikey = "c969986d00bd44eebdc3546f365121cc"

	for date in DateArray:

		name = "nyt_"+str(date[0])+"_"+str(date[1])+".json"
		
		if FileNotinDir(path, name): 
			request_string = "https://api.nytimes.com/svc/archive/v1/" + str(date[0]) + "/" + str(date[1]) +".json?api-key=" + apikey
			page = UrlRequest(request_string)

			if page:
				articles = json.loads(page.decode('utf-8'))
				with open(path+name, 'w') as outfile:
					json.dump(articles, outfile)
			else:
				print("page "+name+" was not read")
			time.sleep(3)	



def DateList(start_date, end_date):
	DateArray = []
	if(type(start_date) == str):
		start_year = int(start_date[0:4])
		start_month = int(start_date[5:6])
		end_year = int(end_date[0:4])
		end_month = int(end_date[5:6])
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
