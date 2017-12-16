import numpy as np  
import nltk 
import time
from config import *
from wordstat import readMetacont, readMWarr, ChooseWords
from helpfunc import DateList
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer 
from scipy.sparse import load_npz
from sklearn.naive_bayes import MultinomialNB  
from sklearn.metrics import classification_report
from sklearn.decomposition import NMF  
from sklearn.linear_model import LogisticRegression


def FilterNoContentArticle(AWarr, Ylabels, thresh):
	totfeat = np.sum(AWarr, axis=1)
	delind = [i for i in range(len(totfeat)) if totfeat[i]<=thresh]
	AWarr = np.delete(AWarr, delind, axis=0)
	Ylabels = np.delete(Ylabels, delind, axis=0)
	return AWarr, Ylabels

def HistContentSize(version, Range):
	AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev, ftwords = loadData(version)

	wordsperart = np.sum(AWarr_train, axis=1)

	fig = plt.figure()
	n, bins, patches = plt.hist(wordsperart, 80,  range=Range, facecolor='k', alpha=0.8)
	plt.show()

def loadData(version):
	AWarr_train = load_npz(tabledir + 'ml_dir/'+str(version)+'/AWarr_train.npz').toarray()
	AWarr_test = load_npz(tabledir + 'ml_dir/'+str(version)+'/AWarr_test.npz').toarray()
	AWarr_dev = load_npz(tabledir +'ml_dir/'+str(version)+'/AWarr_dev.npz').toarray()


	Ylabels_train = np.loadtxt(tabledir +'ml_dir/'+str(version)+'/Ylabels_train.txt', dtype = np.int16)
	Ylabels_test = np.loadtxt(tabledir +'ml_dir/'+str(version)+'/Ylabels_test.txt', dtype = np.int16)
	Ylabels_dev = np.loadtxt(tabledir +'ml_dir/'+str(version)+'/Ylabels_dev.txt', dtype = np.int16)

	ftwords = np.loadtxt(tabledir +'ml_dir/'+str(version)+'/Words.txt', dtype = np.str)

	return AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev, ftwords


def NaiveBayes(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev):

	#print(AWarr_train.shape, Ylabels_train.shape, AWarr_test.shape,Ylabels_test.shape, AWarr_dev.shape,Ylabels_dev.shape)

	class_nb = MultinomialNB() 
	class_nb.fit(AWarr_train, Ylabels_train)

	predictnb_train = class_nb.predict(AWarr_train)
	predictnb_test = class_nb.predict(AWarr_test)
	predictnb_dev = class_nb.predict(AWarr_dev)

	print("NB: Error on dev set")
	print(classification_report(Ylabels_dev, predictnb_dev)) 
	print("NB: Error on training set")
	print(classification_report(Ylabels_train, predictnb_train)) 



	return predictnb_train, predictnb_test, predictnb_dev

def LogisticReg(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev):

	class_lr = LogisticRegression()
	class_lr.fit(AWarr_train, Ylabels_train)

	predictlr_train = class_lr.predict(AWarr_train)
	predictlr_test = class_lr.predict(AWarr_test)
	predictlr_dev = class_lr.predict(AWarr_dev)

	print("LG: Error on dev set")
	print(classification_report(Ylabels_dev, predictlr_dev)) 
	print("LG: Error on training set")
	print(classification_report(Ylabels_train, predictlr_train)) 

	return  predictlr_train, predictlr_test,  predictlr_dev

def FeatWordsIndoc(AWarr, index, wordlist):
	indlist = []
	frq = []
	for i in range(len(AWarr[index,:])):
		if(AWarr[index,i] != 0):
			frq.append( AWarr[index,i] )
			indlist.append(i)
	words = [wordlist[i] for i in indlist]

	return words, frq


# Can be used on MWarr to make sure all topics are represented equally.
def sortTopic():
	nmf = NMF(n_components=10).fit(AWarr_train)
	feature_names = words

	for topic_idx, topic in enumerate(nmf.components_):  
		print('Topic #%d:' % topic_idx)
		print(' '.join([feature_names[i] for i in topic.argsort()[:-20 - 1:-1]]))
		print('')


def wrd2vec():

	Scorpus = MakeSentenceList('200101', '201501', 20)
	model = models.Word2Vec(Scorpus, size=100, window=5, min_count=5, workers=4)
	model.wv.most_similar(positive=['table'], negative=['chair'])
	model.wv.vocab

if __name__ == '__main__':
	version = 30
	AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev = loadData(version)
	predictions_train, predictions_test, predictions_dev = \
	NaiveBayes(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev)