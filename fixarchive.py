from config import *
import json
from helpfunc import DateList, PageExists, FileNotinDir, UrlRequest
from wordstat import readMetacont
from collectarchive import NYTmetaquery
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()
from random import randint
import pdb
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
	
	metacont, metafilename = readMetacont(date)
	
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

if __name__ == '__main__':
	min_words = 100
	articles_per_month = 1000;
	for i in range(10):
		try:
			FixArchive('199006','201612', min_words, articles_per_month)
		except:
			print("----------------CRASHED TRY AGAIN----------------")