from wordstat import *
from config import *
from nptest import NaiveBayes, FeatWordsIndoc, loadData, LogisticReg, FilterNoContentArticle
import pdb
from helpfunc import ensure_dir
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

# num_words = 2000
# count_floor = 300
# shift = 0
# method = 'minmax'

# file_path = tabledir + 'MonthWord_198701_201612_700.txt'
# datelist, wordarray, MWarr = readMWarr(file_path)
# ftwords, MWtop, topscores = ChooseWords(MWarr, wordarray, num_words, count_floor, 'minmax')
# ftwords2, MWtop2, topscores2 = ChooseWords(MWarr, wordarray, num_words, count_floor, 'logsumvar')

# plottopwords(ftwords, MWtop, topscores, datelist, 12, shift)
# plottopwords(ftwords2, MWtop2, topscores2, datelist, 12, shift)

start_date = '198701'
end_date = '201612'
trainsize = 800
devsize = 60
testsize = 2
num_words = 30000
count_floor = 300
method = 'logsumvar'
MWfile = 'MonthWord_198701_201612_700.txt'
timerange = 'yearly'
load = 1
version = 40
debug = 0
save=0
plot=1
ML = 'NB'
trainsizelist = [100, 200, 300, 400, 500, 600, 700]
num_wordlist = [6000]
#thresh = 30
threshlist = [0, 10, 20, 30 ,40, 50]
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

print(str(trainsize))
for thresh in threshlist:
	print('thresh is ', thresh)
	if load==0:
		AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test, ftwords = \
		MakeData(start_date, end_date, MWfile, trainsize, devsize, testsize, num_words, count_floor, method, timerange)
	else:
		AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev, ftwords = loadData(version)

	# Normalize
	
	# AWarr_test
	# AWarr_dev
	# Ylabels_train
	# Ylabels_test
	# Ylabels_dev


	AWarr_train, Ylabels_train = FilterNoContentArticle(AWarr_train, Ylabels_train, thresh)
	AWarr_dev, Ylabels_dev = FilterNoContentArticle(AWarr_dev, Ylabels_dev, thresh)
	AWarr_test, Ylabels_test = FilterNoContentArticle(AWarr_test, Ylabels_test, thresh)


	AWarr_train = normalize(AWarr_train, axis=1)
	AWarr_dev = normalize(AWarr_dev, axis=1)
	AWarr_test = normalize(AWarr_test, axis=1)
	#pdb.set_trace()

	nullarticles_train.append( np.size(AWarr_train, axis=0) - len( np.nonzero(np.sum(AWarr_train, axis=1))[0] ) )
	nullarticles_dev.append( np.size(AWarr_dev, axis=0) - len( np.nonzero(np.sum(AWarr_dev, axis=1))[0] ) )


	if(ML == 'LR'):
		predictnb_train, predictnb_test, predictnb_dev = \
		LogisticReg(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev)
	elif(ML=='NB'):
		predictnb_train, predictnb_test, predictnb_dev = \
		NaiveBayes(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev)

	# ptr.append( predictnb_train )
	# pte.append( predictnb_test)
	# pdv.append( predictnb_dev)
	# ytr.append(Ylabels_train)
	# yte.append(Ylabels_test)
	# ydv.append(Ylabels_dev)

	err_train.append( predictnb_train - Ylabels_train )
	err_test.append( predictnb_test - Ylabels_test)
	err_dev.append( predictnb_dev - Ylabels_dev)

print(nullarticles_train)
print(nullarticles_dev)

acc_train = []
acc_dev = []
for i in range(len(err_train)):
	acc_train.append( 1 - len(np.nonzero(err_train[i])[0])/len(err_train[i])  )
	acc_dev.append( 1 - len(np.nonzero(err_dev[i])[0])/len(err_dev[i]) )

if save:
	f = open(statdir+ 'acc_with_numwords_yearly.txt', 'w')
	f.write('ML algorithm: '+ ML)
	f.write('\nTraining Set size: ' + str(trainsize))
	f.write('\nDev set size: ' + str(devsize))
	f.write('\nFloor of word count: ' + str(count_floor))
	f.write('\nTime range: ' + timerange)
	f.write('\nMethod: ' + method)
	f.write('\nThreshold: '+ str(thresh))
	f.write('\nNum_words \t Train_accuracy \t Dev_accuracy \t no-feature train \t no-feat dev')
	for i in range(len(acc_train)):
		f.write('\n' + str(num_wordlist[i]) + '\t' + str(acc_train[i]) + '\t' + str(acc_dev[i])+ '\t' + str(nullarticles_train[i]) +'\t' + str(nullarticles_dev[i]))
	f.close()

if plot:
	fig = plt.figure()
	plt.plot(threshlist, acc_train)
	plt.plot(treshlist, acc_dev)
	plt.title('Accuracy with number of words')
	plt.xlabel('Number of words')
	plt.ylabel('Accuracy')
	plt.legend(['Train-set Accuracy', 'Dev-set Accuracy'])
	plt.show()

fig2 = plt.figure()
n1, bins1, patches1 = plt.hist(err_train, 30, normed=1, facecolor='g', alpha=0.5)
n, bins, patches = plt.hist(err_dev, 30, normed=1, facecolor='b', alpha=0.5)
plt.show()

if debug==1:
	for i in range(len(err_train)):
		pdb.set_trace()
		words, frq = FeatWordsIndoc(AWarr_train, i, ftwords)
		print('words in doc : ', words)
		print('freq of words: ', frq)
		print('months error: ', err_train[i])

	for i in range(len(err_dev)):
		pdb.set_trace()
		words, frq = FeatWordsIndoc(AWarr_dev, i, ftwords)
		print('words in doc : ', words)
		print('freq of words: ', frq)
		print('months error: ', err_dev(i))