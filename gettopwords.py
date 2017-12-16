from wordstat import *
from config import *
from nptest import NaiveBayes, FeatWordsIndoc, loadData, LogisticReg, FilterNoContentArticle
import pdb
from helpfunc import ensure_dir
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.naive_bayes import MultinomialNB  
from sklearn.metrics import classification_report


start_date = '198701'
end_date = '201612'
trainsize = 600
devsize = 60
testsize = 2
num_words = 12000
count_floor = 200
method = 'sumvar'
MWfile = 'MonthWord_198701_201612_700.txt'
timerange = 'yearly'
load = 0
version = 51
debug = 0
save=0
plot=1
ML = 'NB'
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


if load==0:
	AWarr_train, AWarr_dev, AWarr_test, Ylabels_train, Ylabels_dev, Ylabels_test, ftwords = \
	MakeData(start_date, end_date, MWfile, trainsize, devsize, testsize, num_words, count_floor, method, timerange)
else:
	AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev, ftwords = loadData(version)

AWarr_train, Ylabels_train = FilterNoContentArticle(AWarr_train, Ylabels_train, thresh)
AWarr_dev, Ylabels_dev = FilterNoContentArticle(AWarr_dev, Ylabels_dev, thresh)
AWarr_test, Ylabels_test = FilterNoContentArticle(AWarr_test, Ylabels_test, thresh)


AWarr_trainN = normalize(AWarr_train, axis=1)
AWarr_devN = normalize(AWarr_dev, axis=1)
AWarr_testN = normalize(AWarr_test, axis=1)
#pdb.set_trace()


class_nb = MultinomialNB() 
class_nb.fit(AWarr_trainN, Ylabels_train)

predictnb_train = class_nb.predict(AWarr_trainN)
predictnb_test = class_nb.predict(AWarr_testN)
predictnb_dev = class_nb.predict(AWarr_devN)

err_train = predictnb_train - Ylabels_train 
err_test = predictnb_test - Ylabels_test
err_dev= predictnb_dev - Ylabels_dev

#p = class_nb.predict_proba(AWarr_dev)

print("NB: Error on dev set")
print(classification_report(Ylabels_dev, predictnb_dev)) 
print("NB: Error on training set")
print(classification_report(Ylabels_train, predictnb_train)) 



years = set(Ylabels_dev)
yearlist = list(years)
Score = np.zeros((len(yearlist), len(ftwords)), dtype = np.float32)

for k in range(len(yearlist)):
	indyears = np.where(Ylabels_dev == yearlist[k])[0]
	
	err_year = np.take(err_dev, indyears)
	err_predind = np.where(err_year == 0)[0]
	err_nonpredind = np.where(err_year != 0)[0]
	
	AWyear = np.take(AWarr_dev, indyears, axis=0)
	predictart = np.take(AWyear, err_predind, axis=0)
	nonpredictart = np.take(AWyear, err_nonpredind, axis=0)
	pdb.set_trace()
	for i in range(len(ftwords)):
		pwgivenpred =  len( np.where(predictart[:,i] != 0)[0] ) / len(indyears)
		pwgivennonpred = len( np.where(nonpredictart[:,i] != 0)[0] ) / len(indyears)
		Score[k,i] = np.log( (pwgivenpred +.01) / (pwgivennonpred +.01) )

ftword_top = []
for j in range(len(yearlist)):
	topind = np.argsort(Score[:,j])[-10:-1]
	ftword_top.append( np.take(ftwords, topind) )
	pdb.set_trace()

print(ftword_top)





acc_train = []
acc_dev = []

acc_train = 1 - len(np.nonzero(err_train)[0])/len(err_train)  
acc_dev = 1 - len(np.nonzero(err_dev)[0])/len(err_dev) 


# for i in range(np.size(AWarr_train, 0)):
# 	words, frq = FeatWordsIndoc(AWarr_train, i, ftwords)
# 	print('words in doc : ', words)
# 	print('freq of words: ', frq)
# 	print('months error: ', err_train[i])

for i in range(len(err_dev)):
	if(i>10000):
		pdb.set_trace()
		words, frq = FeatWordsIndoc(AWarr_dev, i, ftwords)
		print('words in doc : ', words)
		print('freq of words: ', frq)
		print('months error: ', err_dev[i])

		artind = i % devsize
		ind = np.int( np.floor(i/devsize) )
		month = ind % 12
		year = 1987 + np.int( np.floor(ind/12) )

		metacont, filename = readMetacont([year, month])
		tit = metacont['docs'][artind]['title']
		print(tit)