import json
import os
import time
import datetime
from collectarchive import DateList
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
stop_words = set(stopwords.words('english'))

def MakeDictIndex(ftword):
	wordict = dict() 
	for i in range(len(ftword)):
		wordict[ftword[i]] = i
	return wordict

def MakeDictLabel(dates):
	datedict = dict() 
	for i in range(len(dates)):
		datedict[str(dates[i][0])+str(dates[i][1])] = i
	return datedict 

def AcceptableString(word):
	return (re.match('\w+$', word) is not None) and (word not in stop_words)
####################################################

def Maketable(ftword, start_date, end_date, trainsize):
	
	datelist = DateList(start_date, end_date)
	direct = "./metarch/"
	Xtable = np.zeros((trainsize*len(datelist), len(ftword) + 1), dtype=np.int32)
	Ylabels = np.zeros(trainsize*len(datelist), dtype=np.int32)
	datedict = MakeDictLabel(datelist)
	wordind = MakeDictIndex(ftword)
	print(wordind)

	for j in range(len(datelist)):
		date = datelist[j]
		print(date)
		filename = str(date[0]) +"_"+ str(date[1]) + ".json"
		with open(direct+filename) as zfile:
			metacont = json.load(zfile)

		row0 = trainsize*j
		for i in range(trainsize):
			wlist = metacont["docs"][i]["content"]
			d = metacont["docs"][i]["date"]
			Ylabels[row0 + i] = datedict[d[0]+str(int(d[1]))]
			for word in wlist:
				if word in wordind:
					Xtable[ i + row0, wordind[word] ] += 1
		 
	return Xtable, Ylabels


def MonthlyStat(start_date, end_date, trainsize):
	datelist = DateList(start_date, end_date)
	direct = "./metarch/"
	datedict = MakeDictLabel(datelist)
	wordict = dict()
	wordind = dict()

	ps = PorterStemmer()

	for j in range(len(datelist)):
		date = datelist[j]
		print(date)
		print(len(wordict))
		filename = str(date[0]) +"_"+ str(date[1]) + ".json"
		with open(direct+filename) as zfile:
			metacont = json.load(zfile)

			for i in range(trainsize):
					wlist = metacont["docs"][i]["content"]
					#d = metacont["docs"][i]["date"]
					#Ylabels[row0 + i] = datedict[d[0]+str(int(d[1]))]
					for word in wlist:
						if AcceptableString(word):
							
							sword = ps.stem(word.lower())
							dd = str(date[0])+str(date[1])
							if sword in wordict:
								if dd in wordict[sword]:
									wordict[sword][dd] += 1
								else:
									wordict[sword][dd] = 1
							else:	
								wordict[sword] = {dd:1}

	print("done reading")
	Mtable = np.zeros((len(datelist), len(wordict)), dtype= np.int32)

	i = 0
	for sword, dates in wordict.items():
		wordind[sword] = i
		for d, count in dates.items():
			Mtable[datedict[d], i] = count
		i += 1

	return Mtable




if __name__ == "__main__":
	#ftword = ['President', 'election', 'Trump', 'beauty', 'hope', 'january']
	#start_date = '199101'
	#end_date = '199504'
	#trainsize = 700
	#Xtable = Maketable(ftword, start_date, end_date, trainsize)

	start_date = '198701'
	end_date = '199601'
	trainsize = 700

	g = MonthlyStat(start_date, end_date, trainsize)
	print(g)