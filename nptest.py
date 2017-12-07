import numpy as np  
import nltk 
import time
from wordstat import readMetacont, readMWarr, ChooseWords
from helpfunc import DateList
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer 
from scipy.sparse import load_npz
from sklearn.naive_bayes import MultinomialNB  
from sklearn.metrics import classification_report

version = 5

def loadData(version, file_path):
	AWarr_train = load_npz('tabledir/ml_dir/'+str(version)+'/AWarr_train.npz').toarray()
	AWarr_test = load_npz('tabledir/ml_dir/'+str(version)+'/AWarr_test.npz').toarray()
	AWarr_dev = load_npz('tabledir/ml_dir/'+str(version)+'/AWarr_dev.npz').toarray()


	Ylabels_train = np.loadtxt('tabledir/ml_dir/'+str(version)+'/Ylabels_train.txt', dtype = np.int16)
	Ylabels_test = np.loadtxt('tabledir/ml_dir/'+str(version)+'/Ylabels_test.txt', dtype = np.int16)
	Ylabels_dev = np.loadtxt('tabledir/ml_dir/'+str(version)+'/Ylabels_dev.txt', dtype = np.int16)

return AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev


def NaiveBayes(AWarr_train, AWarr_test, AWarr_dev, Ylabels_train, Ylabels_test, Ylabels_dev):

	print(AWarr_train.shape, Ylabels_train.shape, AWarr_test.shape,Ylabels_test.shape, AWarr_dev.shape,Ylabels_dev.shape)

	classifier = MultinomialNB()  
	classifier.fit(AWarr_train, Ylabels_train)

	predictions_train = classifier.predict(AWarr_train)
	predictions_test = classifier.predict(AWarr_test)
	predictions_dev = classifier.predict(AWarr_dev)

	print("Error on dev set")
	print(classification_report(Ylabels_dev, predictions_dev)) 

	print("Error on training set")
	print(classification_report(Ylabels_train, predictions_train)) 

	print("Error on test set")
	print(classification_report(Ylabels_test, predictions_test))  

