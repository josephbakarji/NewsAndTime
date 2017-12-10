from config import *
import json
from helpfunc import DateList, PageExists, FileNotinDir, UrlRequest, ensure_dir
from wordstat import readMetacont
from collectarchive import NYTmetaquery
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()
from random import randint
import pdb
import re
from bs4 import BeautifulSoup

def FixArchive(start_date, end_date, count_floor, req_size):
	
	datelist = DateList(start_date, end_date)
	
	for date in datelist:
		print(date)
		QueryNewArticle(date, count_floor, req_size)



def QueryNewArticle(date, count_floor, req_size):				
	if(type(date)==str):
		year = int(date[0:4])
		month = int(date[4:])
	elif(type(date)==list):
		year = date[0]
		month = date[1]
	
	try:
		metacont, metafilename = readMetacont(date)
	except:
		metacont = {}
	
	arch_filename = "nyt_"+str(year)+"_"+str(month)+".json"
	if FileNotinDir(archdir, arch_filename):
		NYTmetaquery(date, date)	
	with open(archdir+arch_filename) as zfile:
		metadata = json.load(zfile)


	titlist = [artic['title'] for artic in metacont['docs']]

	filename = "nyt_"+str(year)+"_"+str(month)+".json"
			

	urls = [metadata["response"]["docs"][i]["web_url"] for i in range(len(metadata["response"]["docs"]))];
	numart = len(urls)
	lenmetacont = len(metacont['docs'])

	for i in range(len(metacont['docs'])):
		print( len(metacont['docs'][i]['content']))
		if(len(metacont['docs'][i]['content'])< count_floor):
			pagesaved = 0
			while(pagesaved == 0):
				ind = randint(0, numart-1) 		# Choose a random index (article) - make a full vector rand
				name = urls[ind].split("/")[-1]
				print(urls[ind])
				if(urls[ind].split(".")[-1] == "html"):		# 
					full_page = UrlRequest(urls[ind])
					if(PageExists(full_page)):
						#pdb.set_trace()
						try:
							fp= full_page.decode("utf-8")				
							soup = BeautifulSoup(fp, "html5lib")
							tit = t.tokenize((soup.title).string)
							if tit not in titlist:
								body = []
								content = []
								body.append( soup.find_all("p", class_="story-body-text story-content"))
								body.append( soup.find_all("p", itemprop="articleBody"))
								body.append( soup.find_all("p", itemprop="reviewBody"))
								for b in body:
									if(b!=[]):
										content = b
										break
								purecontent = t.tokenize([c.string for c in content])
								if(len(purecontent)>count_floor):
									metacont['docs'][i]['title'] = tit
									metacont['docs'][i]['content'] = purecontent
									metacont['docs'][i]['date'] = t.tokenize(soup.find_all('meta', itemprop="datePublished")[0]['content'].split("-"))
									pagesaved = 1
									print('added new article')
								else:
									print('not enough words = ', len(purecontent))
							else:
								print('article already in list')

						except:
							print("page could not be opened")

	
	if( lenmetacont<req_size):
		for i in range(req_size - lenmetacont):
			pagesaved = 0
			while(pagesaved == 0):
				ind = randint(0, numart-1) 		# Choose a random index (article) - make a full vector rand
				name = urls[ind].split("/")[-1]
				print(urls[ind])
				if(urls[ind].split(".")[-1] == "html"):		# 
					full_page = UrlRequest(urls[ind])
					if(PageExists(full_page)):
						#pdb.set_trace()
						try:
							fp= full_page.decode("utf-8")				
							soup = BeautifulSoup(fp, "html5lib")
							tit = t.tokenize((soup.title).string)
							if tit not in titlist:
								body = []
								content = []
								body.append( soup.find_all("p", class_="story-body-text story-content"))
								body.append( soup.find_all("p", itemprop="articleBody"))
								body.append( soup.find_all("p", itemprop="reviewBody"))
								for b in body:
									if(b!=[]):
										content = b
										break
								purecontent = t.tokenize([c.string for c in content])
								if(len(purecontent)>count_floor):
									dd = t.tokenize(soup.find_all('meta', itemprop="datePublished")[0]['content'].split("-"))
									mcont = {'title':tit, 'content':purecontent, 'date': dd}
									metacont['docs'].append(mcont)
									pagesaved = 1
									print('added new article')
								else:
									print('not enough words len = ', len(purecontent))
							else:
								print('article already in list')

						except:
							print("page could not be opened")


	with open(metarchdir + metafilename, 'w') as outfile:
		json.dump(metacont, outfile)

	print('done with '+ metafilename )



def RemoveUselessWords(start_date, end_date):
	direc = './metarchdircorr/'
	ensure_dir(direc)

	datelist = DateList(start_date, end_date)
	for date in datelist:

		metacont, filename = readMetacont(date)
		#print(metacont)
		for article in metacont['docs']:
			for word in article['content']:
				s = word.encode('unicode-escape').decode('ascii')
				if re.match("^[a-zA-Z0-9.,()$-]*$", s) is None:
					article['content'].remove(word)
					#print(s)

		with open(direc+filename, 'w') as outfile:
			json.dump(metacont, outfile)


def FixDates(start_date, end_date, metarchdircorr):
	
	ensure_dir(metarchdircorr)


	datelist = DateList(start_date, end_date)
	for date in datelist:

		filename = str(date[0])+'_'+str(date[1])+'.json'
		fdir = metarchdircorr+filename
		with open(fdir) as zfile:
			metacont = json.load(zfile)

		for article in metacont['docs']:
			if 'date' in article:
				if(len(article['date'])>5):
					article['date'] = [article['date'][2], article['date'][6], article['date'][10]]
				print(article['date'])
			else:
				article['date'] = [str(date[0]), str(date[1]), str(25)]

		with open(fdir, 'w') as rfile:
			json.dump(metacont, rfile)



if __name__ == '__main__':
	min_words = 100
	articles_per_month = 1000;
	# for i in range(1):
	# 	try:
	# 		FixArchive('200301','201612', min_words, articles_per_month)
	# 	except:
	# 		print("----------------CRASHED TRY AGAIN----------------")

	#RemoveUselessWords('198701','201612')

	metarchdircorr = './metarchdircorr/'
	start_date = '200612'
	end_date = '201612'