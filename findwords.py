from config import *
from wordstat import *
import pdb
import matplotlib.pyplot as plt


MWfile = 'MonthWord_198701_201612_700.txt'
file_path = tabledir + MWfile
datelist, wordarray, MWarr = readMWarr(file_path)

words = ['caesarean', 'stanford', 'louisvil', 'softbal', 'tobi', 'cardin']

dd = []
for date in datelist:
	dd.append(date[0])

f = list(set(dd))

wordplot = []
for word in words:
	wind = wordarray.index(word)
	wordplot.append( MWarr[:,wind] )
	pdb.set_trace()

for i, wordsig in enumerate(wordplot):
	fig = plt.figure(i)
	plt.plot(range(len(datelist)), wordsig)
	plt.title(words[i])
	plt.show()

