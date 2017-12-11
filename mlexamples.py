import numpy as np  
import matplotlib.pyplot as plt  
import nltk 
import time
from wordstat import readMetacont, readMWarr, ChooseWords, saveMWarrSparse, MakeDictLabel, saveDataSparse, plottopwords
from helpfunc import DateList, ensure_dir
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer  
import pdb
from config import *
from nltk.stem import PorterStemmer
import json


def MakeMonthlyCorp(start_date, end_date, statset):
	ylabel = []
	corpus = []
	Mcorpus = []
	for date in DateList(start_date, end_date):
		print(date)
		metacont, filename = readMetacont(date)
		for article in metacont['docs'][0:statset]:
			corpus.append(' '.join(article['content']))
		Mcorpus.append( ' '.join(corpus))
		ylabel.append(date)
	
	return ylabel, Mcorpus

def MakeArticleCorp(start_date, end_date, trainsize, devsize, testsize):
	train_corpus = []
	train_ylabel = []
	dev_corpus = []
	dev_ylabel = []
	test_corpus = [] 
	test_ylabel = [] 
	datelist = DateList(start_date, end_date)
	datedict = MakeDictLabel(datelist)

	for date in datelist:
		print(date)
		metacont, filename = readMetacont(date)
		for article in metacont['docs'][0:trainsize]:
			train_corpus.append(' '.join(article['content']))
			train_ylabel.append( datedict[ str(date[0]) + str(int(date[1])) ] )
		for article in metacont['docs'][trainsize:trainsize+devsize]:
			dev_corpus.append(' '.join(article['content']))
			dev_ylabel.append( datedict[ str(date[0]) + str(int(date[1])) ] )
		for article in metacont['docs'][trainsize+devsize:trainsize+devsize+testsize]:
			test_corpus.append(' '.join(article['content']))
			test_ylabel.append( datedict[ str(date[0]) + str(int(date[1])) ])

	return train_corpus, train_ylabel, dev_corpus, dev_ylabel, test_corpus, test_ylabel

def MakeSentenceList(start_date, end_date, trainsize):
	
	Scorpus = []
	for date in DateList(start_date, end_date):
		print(date)
		metacont, filename = readMetacont(date)
		for article in metacont['docs'][0:trainsize]:
			for sentence in (' '.join(article['content'])).split('.'):
				Scorpus.append(sentence.split(' '))
	return Scorpus

# NO STEMMING?
def MakeTableFaster(start_date, end_date, MWfile, num_words, count_floor, method, trainsize, devsize, testsize):
	file_path = tabledir + MWfile 

	t0 = time.time()
	train_corpus, train_ylabel, dev_corpus, dev_ylabel, test_corpus, test_ylabel = MakeArticleCorp(start_date, end_date, trainsize, devsize, testsize)
	print('finished making article corpus')
	datelist, wordarray, MWarr = readMWarr(file_path) # avoid reading MWarr
	ftwords, MWtop, topscores = ChooseWords(MWarr, wordarray, num_words, count_floor, method)
	print('done choosing words')	
	
	vectorizer2 = CountVectorizer(stop_words='english', vocabulary = ftwords)
	AWarr_train = vectorizer2.fit_transform(train_corpus)
	AWarr_dev = vectorizer2.fit_transform(dev_corpus)
	AWarr_test = vectorizer2.fit_transform(test_corpus)
	tend = time.time() - t0

	print('saving data')
	saveDataSparse(tabledir, AWarr_train, AWarr_dev, AWarr_test, train_ylabel, dev_ylabel, test_ylabel, ftwords, \
		start_date, end_date, count_floor, tend, method, file_path)

	plottopwords(ftwords, MWtop, topscores, datelist, 12)


def MakeMetarchStem(start_date, end_date):
	ps = PorterStemmer()
	directory = archive_dir + 'metarchstem/'
	ensure_dir(directory)
	datelist = DateList(start_date, end_date)
	for date in datelist:
		print(date)
		metacont, filename = readMetacont(date)
		for article in metacont['docs']:
			wordlist = []
			for word in article['content']:
				wordlist.append( ps.stem(word.lower()) )
			article['content'] = wordlist

		with open(directory + filename, 'w') as zfile:
			json.dump(metacont, zfile)
#def MakeArticleCorp(start_date, end_date):
#	ylabel = []
#	corpus = []
#	Acorpus = []
#	for date in DateList(start_date, end_date):
#		print(date)
#		metacont, filename = readMetacont(date)
#		for article in metacont['docs']:
#			Acorpus.append(' '.join(article['content']))
#			ylabel.append(date)
#	
#	return ylabel, Acorpus
#

if __name__ == '__main__':

	start_date = '198701'
	end_date = '201612'
	MWfile =  'MonthWord_198701_201612_700.txt'
	num_words = 3000
	count_floor = 500

	method = 'minmax'

	trainsize = 360
	testsize = 30
	devsize = 30

	MakeTableFaster(start_date, end_date, MWfile, num_words, count_floor, method, trainsize, devsize, testsize)
	datelist, wordarray, MWarr = readMWarr(file_path, 'words')
	ftwords, MWtop, topscores = ChooseWords(X, wordarray, num_words, count_floor, method)

	#ylabel, Mcorpus = MakeMonthlyCorp(start_date, end_date)
	Aylabel, MakeArticleCorp(start_date, end_date)
	vectorizer = CountVectorizer(stop_words='english', vocabulary=ftwords)
	BowMat = vectorizer.fit_transform(Acorpus)
	


