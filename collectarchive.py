import json
import datetime
from helpfunc import UrlRequest, FileNotinDir, DateList, ensure_dir
from config import *
import time
import sys

# start_date and end_date format is "YYYYMM", type: string
def NYTmetaquery(start_date, end_date) :

	DateArray = DateList(start_date, end_date)	
	ensure_dir(archdir)

	print('Running NYTmetaquery for date range: ', DateArray[0], DateArray[-1])
	for date in DateArray:
		print(date)

		name = "nyt_"+str(date[0])+"_"+str(date[1])+".json"
		
		if FileNotinDir(archdir, name): 
			request_string = "https://api.nytimes.com/svc/archive/v1/" + str(date[0]) + "/" + str(date[1]) +".json?api-key=" + apikey
			page = UrlRequest(request_string)

			if page:
				articles = json.loads(page.decode('utf-8'))
				with open(archdir+name, 'w') as outfile:
					json.dump(articles, outfile)
			else:
				print("page "+name+" was not read")
			time.sleep(3)	

if __name__=='__main__':
	if(len(sys.argv)==3):
		NYTmetaquery(sys.argv[1], sys.argv[2])
