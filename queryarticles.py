import json
import os
import time
import datetime
from bs4 import BeautifulSoup
from collectarchive import NYTmetaquery, DateList, UrlRequest, FileNotinDir




def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)


# Request and save articles in a local directory for a given month
# date = 'YYYYMM' - string
def QueryArticle(date):
	
	if(type(date)==str):
		year = int(date[0:4])
		month = int(date[5:6])
	elif(type(date)==list):
		year = date[0]
		month = date[1]

	archdirect = "./archive/"
	ensure_dir(archdirect)
	filename = "nyt_"+str(year)+"_"+str(month)+".json"

	# Check if json metadata file exists in local directory and load it. If not request it and use it.	
	if FileNotinDir(archdirect, filename):
		NYTmetaquery(date, date)
	with open(archdirect+filename) as zfile:
		metadata = json.load(zfile)

	urls = [metadata["response"]["docs"][i]["web_url"] for i in range(len(metadata["response"]["docs"]))];

	name = urls[0].split("/")[-1]
	direct = "./fullarticles/" + str(year) + "_" + str(month) + "/"
	ensure_dir(direct+name)
	
	# Find index of url that was last downloaded (assumes only downloading .html files)
	filelist = os.listdir(direct)
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
				fp= full_page.decode("utf-8")
				name = url.split("/")[-1]			
				print(name)

				htmlfile = open(direct+name, 'w')
				htmlfile.write(fp)
				htmlfile.close()
				time.sleep(1)
			else:
				print(str(full_page)+": Not Found")


# Retrieve articles from a range of months
# start_date, end_date = 'YYYYMM' - string
def QueryArticleLoop(start_date, end_date):
	dates = DateList(start_date, end_date)
	for date in dates:
		print(date)
		QueryArticle(date)

def PageExists(page):
	return (page != 404) and (page != 410) 


if __name__ == "__main__":
	
	QueryArticleLoop("199104", "201710")
	