# New York and Times
Machine Learning the relationship between publication date and content

# Usage:


- Building archive:
	* This package collects data from the NYTimes archive using an api key provided by NYT. You'd need to have this key to run the package. Place key in `config.py`.
	* To collect the metadata archive from `start_date` to `end_date` with `YYYYMM` string format, run `python collectarchive.py start_date end_date`. For example, `python collectarchive.py 199103 199102` The data will be save in the `metarch` folder.
	* To download `N` randomly selected articles from the metadata from `start_date` to `end_date`, run `python queryarticles.py start_date end_date N`. The articles will be saved in a the `fullarticles` folder.
	* To parse `M` HTML files (where `M<N`)  for dates from `start_date` to `end_date`, run `python queryarticles.py start_date end_date M`. The parsed JSON files will be stored in a dictionaries stored in the `metarch` folder. The dictionary contains a list of tokenized content `metacont['docs'][i]['content']`, tokenized title `metacont['docs'][i]['title']`, and tokenized date `metacont['docs'][i]['date']` for each article `i`.

- Building the Bag-of-words matrices:
	* The file `wordstat.py` contains all the functions needed to build a bag-of-words matrix for all training/dev/test sets per article and per month. The function `ChooseWords()` is the feature selection function that takes as input a monthly bag-of-words. See end of file of `wordstat.py` to adjust paramters.

- Learning algorithms to test:
	* `mllibs.py` contains functions using the SKLearn package for Naive Bayes and Softmax, along with test functions for Word2Vec and IDF topic categorization. Those functions are tested in `testfile.py`
	* Deep Learning + Softmax: The files `LearnMisc.py`, `LearnMisc2.py` and `LearnMisc3.py` contain functions for Softmax and Deep Learning using Tensorflow whose parameters can be adjusted at the end of the files.

- Extra helper files:
	* `helpfunc.py` contains helper functions for archive collection.
	* `mlexamples.py` contains functions that build the BOW in alternative ways using built-in libraries.
	* `fixarchive.py` runs through the archive and makes sure every articles is of the requires length and downloads new files if not only editing the metadata in the `metarch` folder.
	* `gettopwords.py` computes the relative success score of words and returns the top words for a given time range.
	* `findwords.py` will return the monthly frequency of a list of words provided in the input.
	* `makemap.py` will run through a lits of feature size and training size list computing the precision for each, for either NB or LogR.
