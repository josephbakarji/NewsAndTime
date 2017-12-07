from bs4 import BeautifulSoup
import json
import os
from collectarchive import DateList
from config import *
from queryarticles import QueryArticleLoop
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()

# discard articles with no content, no date or no title?
def Parsehtml(file_path):

	myfile = open(file_path, 'r').read()
	soup = BeautifulSoup(myfile, "html5lib")
	title = soup.title
	date = soup.find_all('meta', itemprop="datePublished")[0]['content'].split("-")

	
	body = []
	content = []
	body.append( soup.find_all("p", class_="story-body-text story-content"))
	body.append( soup.find_all("p", itemprop="articleBody"))
	body.append( soup.find_all("p", itemprop="reviewBody"))

	for b in body:
		if(b!=[]):
			content = b
			break
	if(content==[]):
		print("Content not found")

	tit = title.string
	purecontent = [c.string for c in content]

	
	return tit, purecontent, date

# date = "YYYYMM", second argument is limpages (in case a limited pages is to be imposed)
def BuildDict(date, *argv):
	if(type(date)==str):
		directory = artdir +str(int(date[0:4]))+"_"+str(int(date[4:]))+"/"
	elif(type(date)==list):
		directory = artdir +str(date[0])+"_"+str(date[1])+"/"
	print(directory)

	if(len(argv)==0):
		filelistemp = os.listdir(directory)
	elif(len(argv)==1):
		filelistemp = os.listdir(directory)[:argv[0]]

	filelist = filelistemp
	dictlist = []

	for f in filelist:
		tit, content, date = Parsehtml(directory+f)
		mcont = {'title': t.tokenize(tit), 'content':t.tokenize(content), 'date':date}
		dictlist.append(mcont)
		print(len(dictlist)/len(filelist))
	ss = {'docs': dictlist}

	with open(metarchdir + directory.split("/")[-2]+".json", 'w') as outfile:
		json.dump(ss, outfile)
	print(metarchdir + directory.split("/")[-1]+".json")
	print(ss)

def BuildDictLoop(start_date, end_date, *argv):
	dlist = DateList(start_date, end_date)
	if(len(argv)==1):
		limpages = argv[0]
		for date in dlist:
			BuildDict(date, limpages)
	elif(len(argv)==0):
		for date in dlist:
			BuildDict(date)

if __name__ == "__main__":
	BuildDictLoop("198701", "198702", 1000)
	BuildDictLoop("199104", "199104", 1000)

