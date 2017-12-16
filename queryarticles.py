import json
import os
import time
import datetime
from bs4 import BeautifulSoup
from collectarchive import NYTmetaquery, DateList, UrlRequest, FileNotinDir
from random import randint
from helpfunc import PageExists
from config import *



# Request and save articles in a local directory for a given month (requires connection)
# date = 'YYYYMM' - string, argv contains argument limpages: number of pages to be downloaded.
def QueryArticle(date, *argv): 
	
	if(type(date)==str):
		year = int(date[0:4])
		month = int(date[5:6])
	elif(type(date)==list):
		year = date[0]
		month = date[1]

	filename = "nyt_"+str(year)+"_"+str(month)+".json"
	ensure_dir(archdir)
	ensure_dir(artdir)

	# Check if json metadata file exists in local directory and load it. If not request it and use it.	
	if FileNotinDir(archdir, filename):
		NYTmetaquery(date, date)	
	with open(archdir+filename) as zfile:
		metadata = json.load(zfile)

	urls = [metadata["response"]["docs"][i]["web_url"] for i in range(len(metadata["response"]["docs"]))];

	direct = artdir + str(year) + "_" + str(month) + "/"
	filelist = os.listdir(direct)
	if(len(argv)==0):
		# Find index of url that was last downloaded (assumes only downloading .html files)
		for i in range(len(urls)):
			flag = 0
			if (urls[i].split(".")[-1] == "html"):
				for j in range(len(filelist)):
					if (filelist[j] == urls[i].split("/")[-1]):
						flag = 1
				if flag == 0:
					testpage = UrlRequest(urls[i])
					if(PageExists(testpage)):
						numfile = i
						break
					
		# Loop through list of "web_url"'s, query each ending with .html, and save to local directory
		for url in urls[numfile:-1]:
			print(url)
			if(url.split(".")[-1] == "html"):		# This condition needs to be changed (many articles are not .html)
				full_page = UrlRequest(url)
				if(PageExists(full_page)):
					try:	
						fp= full_page.decode("utf-8")
						name = url.split("/")[-1]			
						print(name)
						htmlfile = open(direct+name, 'w')
						htmlfile.write(fp)
						htmlfile.close()
						time.sleep(0.4)
					except:
						print("Error occured")
				else:
					print(str(full_page)+": Not Found")


	elif(len(argv)==1):
		limpages = argv[0]
		numart = len(urls)
		numlist = len(filelist)		# Number of pages already downloaded
					
		
		if(limpages - numlist <= 0):
			print("Directory contains more than " + str(limpages) + " articles")
			return

		for i in range(limpages - numlist):
			pagesaved = 0
			while(pagesaved == 0):
				ind = randint(0, numart-1) 		# Choose a random index (article) - make a full vector rand
				name = urls[ind].split("/")[-1]
				print(urls[ind])
				if(FileNotinDir(direct, name)):
					if(urls[ind].split(".")[-1] == "html"):		# 
						full_page = UrlRequest(urls[ind])
						if(PageExists(full_page)):
							try:
								fp= full_page.decode("utf-8")				
								print(name)
								htmlfile = open(direct+name, 'w')
								htmlfile.write(fp)
								htmlfile.close()
								time.sleep(.2)
								pagesaved = 1
							except:
								print("Error occured")
								time.sleep(1)

						else:
							print(str(full_page)+": Not Found")


# Retrieve articles from a range of months
# start_date, end_date = 'YYYYMM' - string
def QueryArticleLoop(start_date, end_date, limpages):
	dates = DateList(start_date, end_date)
	for date in dates:
		print(date)
		QueryArticle(date, limpages)




if __name__ == "__main__":
	if(len(sys.argv)==4):
		QueryArticleLoop(sys.argv[1], sys.argv[2], int(sys.argv[3]))
	else:
		QueryArticleLoop("199601", "199712", 1000)
	