import numpy as np  
import matplotlib.pyplot as plt  
import nltk 
import time
from wordstat import readMetacont, readMWarr, ChooseWords
from helpfunc import DateList
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer  

start_date = '198701'
end_date = '201612'
trainsize = 800
devsize = 100
file_path = './tabledir/MonthWord_198701_201612_700.txt'
num_words = 10000
count_floor = 400
method = 'logsumvar'

datelist, wordarray, MWarr = readMWarr(file_path)
ftwords, MWtop, topscores = ChooseWords(MWarr, wordarray, num_words, count_floor, method)

vectorizer = CountVectorizer(stop_words='english', vocabulary=ftwords)

joiningtime= time.time()
corpus = []
for date in DateList(start_date, end_date):
	print(date)
	metacont = readMetacont(date)
	for article in metacont['docs']:
		corpus.append(' '.join(article['content']))
print('Time to join data = ', time.time() - joiningtime)


t0= time.time()

BowMat = vectorizer.fit_transform(corpus)

print(time.time()-t0)

X = BowMat.toarray()
print(X)
