# New York and Times
Machine Learning the relationship between publication date and content

# TO DO:
You can put your name next to the task you would like to do. I think for now the pri

- Building archive:
	* The code downloads html files but slowly (takes 2 hours per month). I'll try decreasing the wait time between loops, but for now each one of us can download a portion. For a start, let's download the last 30 years. I'll take 1987-1997, Dimitrios: 1997-2007, Sepehr: 2007-2017.
	* Store all files on a shared folder in google drive. We'll have to change the archive and fullarticles folder paths (I'll add __init__ for that)
	* Build Training, dev, and test sets.
- filtering articles and words:
	* Now I'm just taking everything ending with .html. Some links ending with "/" seem to be also valid
	* Remove stopwords with NLTK: http://www.geeksforgeeks.org/removing-stop-words-nltk-python/
	* Extract names of people and places: https://nlp.stanford.edu/software/CRF-NER.shtml, https://stackoverflow.com/questions/20290870/improving-the-extraction-of-human-names-with-nltk

- Function for building year-word count table for a set of words.

- Learning algorithms to test:
	* Naive Bayes
	* Linear Regression
	* Softmax
	* Deep Learning

	- Extra:
	* Use distributional similarity to capture meaning of words (by word cooccurence)
		^ Study the change of meaning of words by studying their dynamics in the semantic space (using unsupervised learning).
	* Extra: use reinforcement learning to add time-relevant articles to the training set.

- Feature Selection:
	* Use mutual information to assess importance of words.
	* Plot word frequency and come up with metric of fluctuation. 
	* Include the number of stop-words as a feature.

# Content

- The ipynote.ipynb is an ipython notebook file that has a sequence of examples to test the functions. Install ipython and jupyter notebook.
- In collectarchive.py: the function NYTmetaquery() downloads the .json metadata file from the archive in the date range [start\_date,end\_date].
- In queryarticles.py: the function QueryArticle downloads all the articles contained in the 'web\_url' links and saves them to the fullarticles directory
- In parsearticles.py: the function Parsehtml() takes opens an html file and finds the content and title (date and author should also be added).
