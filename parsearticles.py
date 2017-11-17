from bs4 import BeautifulSoup
import json
import os
from collectarchive import DateList
from queryarticles import ensure_dir
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()

def Parsehtml(file_path):

	myfile = open(file_path, 'r').read()
	soup = BeautifulSoup(myfile, "html5lib")
	title = soup.title
	date = soup.find_all('meta', itemprop="datePublished")[0]['content'].split("-")

	#print(file_path)
	
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

# date = "YYYYMM"
def BuildDict(date):
	if(type(date)==str):
		directory = "./fullarticles/"+str(int(date[0:4]))+"_"+str(int(date[5:6]))+"/"
	elif(type(date)==list):
		directory = "./fullarticles/"+str(date[0])+"_"+str(date[1])+"/"
	metarchdir = "./metarch/"
	ensure_dir(metarchdir)
	print(directory)


	filelist = os.listdir(directory)
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

def BuildDictLoop(start_date, end_date):
	dlist = DateList(start_date, end_date)
	for date in dlist:
		BuildDict(date)

if __name__ == "__main__":
	BuildDictLoop("199002", "199601")

