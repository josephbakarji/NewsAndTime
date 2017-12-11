from wordstat import *
from config import *
from nptest import NaiveBayes, FeatWordsIndoc, loadData, LogisticReg, FilterNoContentArticle
import pdb
from helpfunc import ensure_dir
import matplotlib.pyplot as plt
from matplotlib import colors


start_date = '198701'
end_date = '201612'
trainsize = 750
devsize = 70
testsize = 2
#num_words = 30000
count_floor = 200
method = 'logsumvar'
MWfile = 'MonthWord_198701_201612_700.txt'
timerange = 'yearly'
load = 0
debug = 0
save=0
plot=0
ML = 'NB'
trainsizelist = [100, 200, 300, 400, 500, 600, 700, 800]
num_wordlist = [1000, 3000, 5000, 7000, 9000,11000,13000,15000]
thresh = 30
statdir = gdrive_dir + 'statdir/'
ensure_dir(statdir)

err_train = []
err_test = []
err_dev = []
ptr = []
pte = []
pdv = []
ytr = []
yte = []
ydv = []
nullarticles_train = []
nullarticles_dev = []


for num_words in num_wordlist:
	for trainsize in trainsizelist:
		print('num_words is ', num_words)
		print('trainsize is ', trainsize)
		if load==0:
			AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test, ftwords = \
			MakeData(start_date, end_date, MWfile, trainsize, devsize, testsize, num_words, count_floor, method, timerange)
		else:
			version = 26
			AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev, ftwords = loadData(version)




		AWarr_train, Ylabels_train = FilterNoContentArticle(AWarr_train, Ylabels_train, thresh)
		AWarr_dev, Ylabels_dev = FilterNoContentArticle(AWarr_dev, Ylabels_dev, thresh)
		AWarr_test, Ylabels_test = FilterNoContentArticle(AWarr_test, Ylabels_test, thresh)

		AWarr_train = normalize(AWarr_train, axis=1)
		AWarr_dev = normalize(AWarr_dev, axis=1)
		AWarr_test = normalize(AWarr_test, axis=1)

		if(ML == 'LR'):
			predictnb_train, predictnb_test, predictnb_dev = \
			LogisticReg(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev)
		elif(ML=='NB'):
			predictnb_train, predictnb_test, predictnb_dev = \
			NaiveBayes(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev)


		err_train.append( predictnb_train - Ylabels_train )
		err_test.append( predictnb_test - Ylabels_test)
		err_dev.append( predictnb_dev - Ylabels_dev)

		param.append( [num_words, trainsize])


f = open(statdir+ 'mapNB.txt', 'w')
f.write('ML algorithm: '+ ML)
f.write('\nDev set size: ' + str(devsize))
f.write('\nFloor of word count: ' + str(count_floor))
f.write('\nTime range: ' + timerange)
f.write('\nMethod: ' + method)
f.write('\nThreshold: '+ str(thresh))
f.write('\nNum_words \t trainsize \t Train_accuracy \t Dev_accuracy')
for i, vec in enumerate(param):
	f.write('\n' + str(vec[0]) + '\t' + str(vec[1]) + '\t' + str(err_train[i]) '\t' + str(err_dev[i]))
f.close()

cmap = colors.ListedColormap(['red', 'blue'])
bounds = [0,10,20]