import numpy as np  
import matplotlib.pyplot as plt  
import nltk 
import time
from wordstat import readMetacont, readMWarr, ChooseWords
from helpfunc import DateList
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer  
import pdb
from config import *

def MakeMonthlyCorp(start_date, end_date):
	ylabel = []
	corpus = []
	Mcorpus = []
	for date in DateList(start_date, end_date):
		print(date)
		metacont, filename = readMetacont(date)
		for article in metacont['docs']:
			corpus.append(' '.join(article['content']))
		Mcorpus.append( ' '.join(corpus))
		ylabel.append(date)
	
	return ylabel, Mcorpus


#def MonthlyStat

if __name__ == '__main__':

	start_date = '198701'
	end_date = '199012'
	file_path = tabledir + 'MonthWord_198701_201612_750.txt'
	num_words = 10000
	count_floor = 400
	method = 'logsumvar'



	ylabel, Mcorpus = MakeMonthlyCorp(start_date, end_date)
	vectorizer = CountVectorizer(stop_words='english')
	BowMat = vectorizer.fit_transform(Mcorpus)
	X = BowMat.toarray()

	# datelist, wordarray, MWarr = readMWarr(file_path)
	ftwords, MWtop, topscores = ChooseWords(X, wordarray, num_words, count_floor, method)
