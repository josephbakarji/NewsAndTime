import json
import os
import time
import datetime
from collectarchive import DateList
import numpy as np

def Maketable(ftword, start_date, end_date, trainsize):
	
	datelist = DateList(start_date, end_date)
	direct = "./metarch/"
	Xtable = np.zeros((trainsize*len(datelist), len(ftword) + 1), dtype=np.int32)
	Ylabels = np.zeros(trainsize*len(datelist), dtype=np.int32)
	datedict = MakeDictLabel(datelist)
	wordict = MakeDictIndex(ftword)
	print(wordict)

	for j in range(len(datelist)):
		print(datelist[j])
		filename = str(datelist[j][0]) +"_"+ str(datelist[j][1]) + ".json"
		with open(direct+filename) as zfile:
			metacont = json.load(zfile)

		row0 = trainsize*j
		for i in range(trainsize):
			wlist = metacont["docs"][i]["content"]
			d = metacont["docs"][i]["date"]
			Ylabels[row0 + i] = datedict[d[0]+str(int(d[1]))]
			for word in wlist:
				if word in wordict:
					Xtable[ i + row0, wordict[word] ] += 1
		 
	return Xtable, Ylabels

def MakeDictIndex(ftword):
	wordict = dict() 
	for i in range(len(ftword)):
		wordict.update({ftword[i]: i})
	return wordict

def MakeDictLabel(dates):
	datedict = dict() 
	for i in range(len(dates)):
		datedict.update({str(dates[i][0])+str(dates[i][1]): i})
	return datedict 


if __name__ == "__main__":
	ftword = ['President', 'election', 'Trump', 'beauty', 'hope', 'january']
	start_date = '199101'
	end_date = '199504'
	trainsize = 700
	Xtable = Maketable(ftword, start_date, end_date, trainsize)
