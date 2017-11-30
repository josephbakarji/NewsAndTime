import json
import os
import time
import datetime
from collectarchive import DateList
from helpfunc import ensure_dir
from config import *
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import re
import csv
import pdb
from scipy.sparse import save_npz, csr_matrix


stop_words = set(stopwords.words('english'))
ps = PorterStemmer()


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



# Maketable takes as input the feature words and returns an Article-vs-Word X table
# INPUT:
# - ftword: list of chosen feature space of size num_words. (output of ChooseWords)
# - start_date: format 'YYYYMM' of type str
# - end_date: format 'YYYYMM' of type str
# - trainsize: Number of training examples.
# OUTPUT:
# - AWarr: Article*Words int array (of size (trainsize*Months)x(len(ftword) ) 
# - Ylabels: List of integers [0 : len(ftword)] mapped from dates and used as labels.
def Maketable(ftword, start_date, end_date, trainsize):
	
	datelist = DateList(start_date, end_date)
	AWarr = np.zeros((trainsize*len(datelist), len(ftword) + 1), dtype=np.int32)
	Ylabels = np.zeros(trainsize*len(datelist), dtype=np.int32)
	datedict = MakeDictLabel(datelist)
	wordind = MakeDictIndex(ftword)
	ensure_dir(metarchdir)

	print(wordind)

	trainidx = [] # Array of training index limit in dictionary (not all articles are taken because of filtered dates)
	for j in range(len(datelist)):
		date = datelist[j]
		print(date)
		filename = str(date[0]) +"_"+ str(date[1]) + ".json"
		with open(metarchdir+filename) as zfile:
			metacont = json.load(zfile)

		row0 = trainsize*j
		for i in range(trainsize):
			#pdb.set_trace()
			wlist = metacont["docs"][i]["content"]
			Ylabels[row0 + i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				sword = ps.stem(word.lower())
				if sword in wordind:
					AWarr[ i + row0, wordind[sword] ] += 1

	return AWarr, Ylabels


# MonthlyStat takes a time range and training set size and returns 
# INPUT:
# - start_date: format 'YYYYMM' of type str
# - end_date: format 'YYYYMM' of type str
# - trainsize: Number of training examples.
# OUTPUT:
# - MWarr: Months*Words array with count
# - wordarray: vector of words (with type str) matching columns of MWarr
# - datelist: list of dates matching the raws of MWarr.
def MonthlyStat(start_date, end_date, trainsize):
	datelist = DateList(start_date, end_date)
	datedict = MakeDictLabel(datelist)
	wordict = dict()
	wordind = dict()
	ensure_dir(tabledir)
	ensure_dir(metarchdir)

	for j in range(len(datelist)):
		date = datelist[j]
		print(date)
		print(len(wordict))
		filename = str(date[0]) +"_"+ str(date[1]) + ".json"
		with open(metarchdir+filename) as zfile:
			metacont = json.load(zfile)

			for i in range(trainsize):
					wlist = metacont["docs"][i]["content"]
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
	MWarr = np.zeros((len(datelist), len(wordict)), dtype= np.int32)
	wordarray = np.empty(len(wordict), dtype = '<U20')

	i = 0
	for sword, dates in wordict.items():
		wordind[sword] = i
		wordarray[i] = sword
		for d, count in dates.items():
			MWarr[datedict[d], i] = count
		i += 1

	#saveMWarr(MWarr, wordarray, datelist, 'MonthWord_'+start_date+'_'+end_date+'_'+str(trainsize)+'.txt')

	return MWarr, wordarray, datelist 


# ChooseWords takes the full Month-Word array and generates the feature (words) space 
# INPUT:
# - MWarr: Month*Words array with integer entries counting occurence of words each month.
# - wordarray: vector of words (with type str) matching columns of MWarr
# - num_words: number of words to be chosen as feature space.
# - count_floor: lower limit on the total number of occurence of words.
# - method: measure to be used to choose the words (type str): options: ['sumvar', ...]
# OUTPUT:
# - topwords: list of chosen feature space of size num_words.
def ChooseWords(MWarr, wordarray, num_words, count_floor, method):
	
	# Remove words with total occurence less than count_floor
	Mwordtot = np.sum(MWarr, axis=0)
	swind = [index for index, value in enumerate(Mwordtot) if value > count_floor]
	
	for idx in sorted(swind, reverse=True):
		del wordarray[idx]
	print('number of words below limit is: ', len(swind))
	
	MWarr = np.delete(MWarr, swind, 1)
	Mwordtot = np.sum(MWarr, axis=0)


	# Filter words with the highest measure according to method (add methods in elif: statements)
	if(method=='sumvar'):
		sep_score = np.log(Mwordtot) * ( np.sum(np.abs(np.diff(MWarr, axis=0)), axis=0)  /  Mwordtot )
		sortind = np.argsort(sep_score)
		topscoreind = np.flip( sortind[-num_words:] , axis=0)
		topscores = [sep_score[x] for x in topscoreind]
		topwords = np.take(wordarray,  topscoreind)
		MWtop = np.take(MWarr, topscoreind, axis=1)
	else:
		print('invalid measure')
		return

	plottopwords(topwords, MWtop, topscores, 12)

	return topwords 


# Saves MWarr (with first row as wordarray) and first two columns as YEAR and MONTH to filename
def saveMWarr(MWarr, wordarray, datelist, filename):
	file = open(tabledir+filename,'w')
	file.write('YEAR \t MONTH')
	for word in wordarray:
		file.write('\t' + word)
	for i in range(len(datelist)):
		file.write('\n')
		file.write(str(datelist[i][0])+'\t'+str(datelist[i][1]))
		countlist = MWarr[i,:]
		for count in countlist:
			file.write('\t'+str(count))


# Reads MWarr from file_path and returns lists of year, month and wordarray, and MWarr.
def readMWarr(file_path):
	year = []
	month = []
	MWarr = []
	with open(file_path) as tsv:
		for idx, line in enumerate( csv.reader(tsv, delimiter='\t') ):
			if(idx == 0):
				wordarray = line[2:]
			else:
				year.append(int(line[0]))
				month.append(int(line[1]))
				MWarr.append([int(i) for i in line[2:]]) # slow

	year = np.asarray(year)
	month = np.asarray(month)
	MWarr = np.asarray(MWarr)

	return year, month, wordarray, MWarr



# Plots the top plotnum words of the with the top score from ChooseWords().
def plottopwords(topwords, MWtop, topscores, plotnum):

	fig = plt.figure()
	
	for i in range(plotnum):
		plt.subplot(4, 3, i+1)
		plt.plot(MWtop[:,i])
		plt.ylabel(topwords[i] + '- scr: ' + str(topscores[i])[0:4])

	plt.show()

if __name__ == "__main__":
	#ftword = ['President', 'election', 'Trump', 'beauty', 'hope', 'january']
	#start_date = '199101'
	#end_date = '199504'
	#trainsize = 700
	#AWarr = Maketable(ftword, start_date, end_date, trainsize)

	# trainsize = 700
	# g = MonthlyStat(start_date, end_date, trainsize)
	#print(g)

	start_date = '198701'
	end_date = '200712'
	trainsize = 700
	file_path = './tabledir/MonthWord_198701_200712_700.txt'
	outfile = tabledir+'ArticleWord_'+start_date+'_'+end_date
	num_words = 10000
	count_floor = 1000
	method = 'sumvar'

	year, month, wordarray, MWarr = readMWarr(file_path)
	ftwords = ChooseWords(MWarr, wordarray, num_words, count_floor, method)
	# X, Y = Maketable(ftwords, start_date, end_date, trainsize)
	# save_npz(outfile +'X.npz', csr_matrix(X))
	# np.savetxt(outfile +'Y.txt', Y, fmt='%d')
