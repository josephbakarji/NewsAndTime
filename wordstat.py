#% matplotlib inline
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
import string

stop_words = set(stopwords.words('english'))
manual_reject = set(string.ascii_lowercase)
reject_list = stop_words and manual_reject

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

def MakeDictLabelYearly(dates):
	datedict = dict() 
	for i in range(len(dates)):
		datedict[str(dates[i][0])+str(dates[i][1])] = dates[i][0]
	return datedict 

def AcceptableString(word):
	return (re.match("^[a-zA-Z.,()$-]*$",word) is not None) and (word not in reject_list)
####################################################

def readMetacont(date):
	if(type(date) == str):
		filename = date[0:4] +"_"+ str(int(date[4:])) + ".json"
	elif(type(date)==list):
		filename = str(date[0]) +"_"+ str(date[1]) + ".json"

	fdir = metarchstem+filename
	if filename in set(os.listdir(metarchdir)):
		with open(fdir) as zfile:
			metacont = json.load(zfile)
	else:
		print("Missing meta-content directory in "+metarchdir)
		return

	return metacont, filename


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


def saveMWarrSparse(MWarrSparse, wordarray, datelist, filename):
	fileword = open(tabledir+'words'+filename,'w')
	for word in wordarray:
		fileword.write('\t' + word)
	
	filedate = open(tabledir+'date'+filename,'w')
	for i in range(len(datelist)):
		filedate.write(str(datelist[i][0])+'\t'+str(datelist[i][1]))
	
	save_npz(tabledir+'bow'+filename, MWarrSparse)

# Reads MWarr from file_path and returns lists of year, month and wordarray, and MWarr.
def readMWarr(file_path):
	datelist = []
	MWarr = []

	with open(file_path) as tsv:
		for idx, line in enumerate( csv.reader(tsv, delimiter='\t') ):
			if(idx == 0):
				wordarray = line[2:]
			else:
				datelist.append([int(line[0]), int(line[1])])
				X = [int(i) for i in line[2:]]
				MWarr.append(X)
	
	MWarr = np.asarray(MWarr)

	return datelist, wordarray, MWarr



# Plots the top plotnum words of the with the top score from ChooseWords().
def plottopwords(topwords, MWtop, topscores, datelist, plotnum, shift):

	dates = [d[0]+d[1]/12 for d in datelist]
	fig = plt.figure()
	n = shift
	for i in range(plotnum):
		plt.subplot(4, 3, i+1)
		plt.plot(dates, MWtop[:,i+n])
		plt.ylabel(topwords[i+n] + '- scr: ' + str(topscores[i+n])[0:4])

	plt.show()

def saveDataSparse(tabledir, AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test, ftwords, \
	start_date, end_date, count_floor, tend, method, file_path, timerange):
	
	mldir = tabledir + 'ml_dir/'
	ensure_dir(mldir)
	fileint=[]
	dirlist = os.listdir(mldir)
	for fn in dirlist:
		try:
			int(fn)
		except:
			dirlist.remove(fn)

	if(len(dirlist)==0):
		os.makedirs(mldir+'1')
		outdir = '1'+'/'
	else:
		for filename in dirlist:
			fileint.append(int(filename))
		outdir = str( max(fileint) + 1 ) + '/'
		os.makedirs(mldir+outdir)

	outfile = mldir + outdir 

	save_npz(outfile +'AWarr_train.npz', csr_matrix(AWarr_train))
	save_npz(outfile +'AWarr_dev.npz', csr_matrix(AWarr_dev))
	save_npz(outfile +'AWarr_test.npz', csr_matrix(AWarr_test))

	np.savetxt(outfile +'Ylabels_train.txt', Ylabels_train, fmt='%d')
	np.savetxt(outfile +'Ylabels_dev.txt', Ylabels_dev, fmt='%d')
	np.savetxt(outfile +'Ylabels_test.txt', Ylabels_test, fmt='%d')

	np.savetxt(outfile +'Words.txt', ftwords, fmt='%s')


	f = open(outfile+'config.txt', 'w')
	f.write('Start Date: '+ start_date)
	f.write('\nEnd Date: '+ end_date)
	f.write('\nTraining Set Size = '+str(np.size(AWarr_train, axis=0)) )
	f.write('\nDev Set Size = '+str(np.size(AWarr_dev, axis=0)))
	f.write('\nTest Set Size = '+str(np.size(AWarr_test, axis=0)))
	f.write('\nNumber of feature words = '+ str(len(ftwords)))
	f.write('\nFloor on total number of words ='+ str(count_floor))
	f.write('\nWord selection method: '+ method)
	f.write('\nSource MonthWord File: '+file_path)
	f.write('\nComputational Time: '+ str(tend/60.0)+' minutes ')
	f.write('\nTime range: '+ timerange)
	f.close()


######################### MAIN FUNCTIONS ######################


# Maketable takes as input the feature words and returns an Article-vs-Word X table
# INPUT:
# - ftword: list of chosen feature space of size num_words. (output of ChooseWords)
# - start_date: format 'YYYYMM' of type str
# - end_date: format 'YYYYMM' of type str
# - trainsize: Number of training examples.
# OUTPUT:
# - AWarr: Article*Words int array (of size (trainsize*Months)x(len(ftword) ) 
# - Ylabels: List of integers [0 : len(ftword)] mapped from dates and used as labels.
def Maketable(ftword, start_date, end_date, trainsize, devsize):
	
	datelist = DateList(start_date, end_date)
	AWarr_train = np.zeros((trainsize*len(datelist), len(ftword) + 1), dtype=np.int32)
	AWarr_dev = np.array([], dtype=np.int32)
	AWarr_test = np.array([], dtype=np.int32)

	Ylabels_train = np.zeros(trainsize*len(datelist), dtype=np.int32)
	Ylabels_dev = np.array([], dtype=np.int32)
	Ylabels_test = np.array([], dtype=np.int32)

	datedict = MakeDictLabel(datelist)
	wordind = MakeDictIndex(ftword)
	ensure_dir(metarchdir)
	devsize0 = devsize

	print(set(wordind))
	for j in range(len(datelist)):
		date = datelist[j]
		print(date)
		metacont, filename = readMetacont(date)
		
		if len(metacont['docs'])>=1000:
			artlist = metacont['docs'][0:1000]
		else:
			artlist = metacont['docs']
			lenart = len(artlist)
			pdb.set_trace()
			devsize = np.int( np.round( devsize0 * (lenart-trainsize)/(1000-trainsize)  ) )


		row0train = trainsize*j
		artnum = len(artlist)
		AWarr_test_partial = np.zeros((artnum-(trainsize+devsize), len(ftword) ), dtype=np.int32)
		Ylabels_test_partial = np.zeros(artnum-(trainsize+devsize), dtype=np.int32)
		AWarr_dev_partial = np.zeros((devsize, len(ftword) ), dtype=np.int32)
		Ylabels_dev_partial = np.zeros(devsize, dtype=np.int32)

		for i in range(trainsize):
			wlist = artlist[i]["content"]
			Ylabels_train[row0train + i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				sword = ps.stem(word.lower())
				if sword in wordind:
					AWarr_train[ i + row0train, wordind[sword] ] += 1

		for i in range(devsize):
			wlist = artlist[i+trainsize]["content"]
			Ylabels_dev_partial[ i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				sword = ps.stem(word.lower())
				if sword in wordind:
					AWarr_dev_partial[ i, wordind[sword] ] += 1

		for i in range(artnum-devsize-trainsize):
			#pdb.set_trace()
			wlist = artlist[i+trainsize+devsize]["content"]
			Ylabels_test_partial[i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				sword = ps.stem(word.lower())
				if sword in wordind:
					AWarr_test_partial[i, wordind[sword] ] += 1

		if(np.size(AWarr_test)!=0):
			AWarr_test = np.concatenate((AWarr_test, AWarr_test_partial), axis=0)
			Ylabels_test = np.concatenate((Ylabels_test, Ylabels_test_partial), axis=0)
			AWarr_dev = np.concatenate((AWarr_dev, AWarr_dev_partial), axis=0)
			Ylabels_dev = np.concatenate((Ylabels_dev, Ylabels_dev_partial), axis=0)
		else:
			AWarr_test = AWarr_test_partial
			Ylabels_test = Ylabels_test_partial
			AWarr_dev = AWarr_dev_partial
			Ylabels_dev = Ylabels_dev_partial



	return AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test


def MaketableFast(ftword, start_date, end_date, trainsize, devsize, testsize, timerange):
	
	datelist = DateList(start_date, end_date)
	AWarr_train = np.zeros((trainsize*len(datelist), len(ftword) ), dtype=np.int16)
	AWarr_dev = np.zeros((devsize*len(datelist), len(ftword) ), dtype=np.int16)
	AWarr_test = np.zeros((testsize*len(datelist), len(ftword) ), dtype=np.int16)

	Ylabels_train = np.zeros(trainsize*len(datelist), dtype=np.int16)
	Ylabels_dev = np.zeros(devsize*len(datelist), dtype=np.int16)
	Ylabels_test = np.zeros(testsize*len(datelist), dtype=np.int16)

	if(timerange == "yearly"):
		datedict = MakeDictLabelYearly(datelist)
	elif(timerange == "monthly"):
		datedict = MakeDictLabel(datelist)
	else:
		print('Inexistent timerange')

	wordind = MakeDictIndex(ftword)
	ensure_dir(metarchdir)

	print(set(wordind))
	for j in range(len(datelist)):
		date = datelist[j]
		print(date)
		metacont, filename = readMetacont(date)
		
		artlist = metacont['docs']
		artnum = len(artlist)
		row0train = trainsize*j
		row0dev = devsize*j
		row0test = testsize*j

		for i in range(trainsize):
			wlist = artlist[i]["content"]
			Ylabels_train[row0train + i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				#sword = ps.stem(word.lower())
				if word in wordind:
					AWarr_train[ i + row0train, wordind[word] ] += 1

		for i in range(devsize):
			wlist = artlist[i+trainsize]["content"]
			Ylabels_dev[row0dev + i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				#sword = ps.stem(word.lower())
				if word in wordind:
					AWarr_dev[ i + row0dev, wordind[word] ] += 1

		for i in range(testsize):
			wlist = artlist[i+trainsize+devsize]["content"]
			Ylabels_test[row0test + i] = datedict[ str(date[0]) + str(int(date[1])) ]
			for word in wlist:
				#sword = ps.stem(word.lower())
				if word in wordind:
					AWarr_test[ i + row0test, wordind[word] ] += 1



	return AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test


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

	saveMWarr(MWarr, wordarray, datelist, 'MonthWord_'+start_date+'_'+end_date+'_'+str(trainsize)+'_2'+'.txt')

	return datelist, wordarray.tolist(), MWarr


# ChooseWords takes the full Month-Word array and generates the feature (words) space 
# INPUT:
# - MWarr: Month*Words array with integer entries counting occurence of words each month.
# - wordarray: vector of words (with type str) matching columns of MWarr
# - num_words: number of words to be chosen as feature space.
# - count_floor: lower limit on the total number of occurence of words.
# - method: measure to be used to choose the words (type str): options: ['sumvar', ...]
# OUTPUT:
# - topwords: list of chosen feature space of size num_words.
# - MWtop: portion of MWarr with only topwords as columns
# - topscores: scores of topwords.
def ChooseWords(MWarr, wordarray, num_words, count_floor, method):
	
	# Remove words with total occurence less than count_floor
	Mwordtot = np.sum(MWarr, axis=0)
	swind = []
	for index, value in enumerate(Mwordtot):
		if(value<count_floor or not AcceptableString(wordarray[index])):
			swind.append(index)
	
	wrdarray = wordarray
	# pdb.set_trace()
	for idx in sorted(swind, reverse=True):
		del wrdarray[idx]

	numvalwords = len(Mwordtot) - len(swind)
	print('number of rejected words (below floor) is: ', len(swind))
	print('number of accepted words (above floor) is: ', numvalwords)

	MWarr = np.delete(MWarr, swind, 1)
	Mwordtot = np.sum(MWarr, axis=0)

	#pdb.set_trace()
	# Filter words with the highest measure according to method (add methods in elif: statements)
	if(method=='logsumvar'):
		score = np.log(Mwordtot) * ( np.sum(np.abs(np.diff(MWarr, axis=0)), axis=0)  /  Mwordtot )
	elif(method=='sumvar'):
		score =  np.sum(np.abs(np.diff(MWarr, axis=0)), axis=0)  /  Mwordtot
	elif(method=='minmax'):
		# pdb.set_trace()
		score = (np.amax(MWarr, axis=0) - np.amin(MWarr, axis=0)) / Mwordtot
	elif(method=='std'):
		score = np.std(MWarr, axis=0)
	else:
		print('invalid measure')
		return


	# In case there are less valid words than desired num_words.
	nwords = num_words
	if(num_words>numvalwords):		
		nwords = numvalwords

	sortind = np.argsort(score)
	topscoreind = np.flip( sortind[-nwords:] , axis=0)
	topscores = [score[x] for x in topscoreind]
	topwords = np.take(wrdarray,  topscoreind)
	MWtop = np.take(MWarr, topscoreind, axis=1)

	return topwords, MWtop, topscores


def MakeData(start_date, end_date, MWfile, trainsize, devsize, testsize, num_words, count_floor, method, timerange):


	file_path = tabledir + MWfile
	datelist, wordarray, MWarr = readMWarr(file_path)
	ftwords, MWtop, topscores = ChooseWords(MWarr, wordarray, num_words, count_floor, method)
	
	t0 = time.time()
	AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test = \
	 	MaketableFast(ftwords, start_date, end_date, trainsize, devsize, testsize, timerange)
	tend = time.time() - t0
	print(tend)

	saveDataSparse(tabledir, AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test, ftwords, \
	 	start_date, end_date, count_floor, tend, method, file_path, timerange)

	# plottopwords(ftwords, MWtop, topscores, datelist, 12, 0)

	return AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test, ftwords

if __name__ == "__main__":


	start_date = '198701'
	end_date = '201612'
	trainsize = 100
	devsize = 100
	testsize = 10
	num_words = 4000
	count_floor = 400
	method = 'logsumvar'
	MWfile = 'MonthWord_198701_201612_700.txt'
	timerange = 'yearly'
	AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test= \
	MakeData(start_date, end_date, MWfile, trainsize, devsize, testsize, num_words, count_floor, method, timerange)

	# file_path = tabledir + 'MonthWord_198701_201612_750_2.txt'
	#datelist, wordarray, MWarr = MonthlyStat(start_date, end_date, trainsize)



	