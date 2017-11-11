# New York and Time 
Machine Learning the relationship between publication date and content

# TO DO:
You can put your name next to the task you would like to do. I think for now the pri

- filtering articles and words:
	* Now I'm just taking everything ending with .html. Some links ending with "/" seem to be also valid
	* Remove stopwords with NLTK: http://www.geeksforgeeks.org/removing-stop-words-nltk-python/

- Function for building year-word count table for a set of words.
- Store all files on a shared folder in google drive.

- Learning algorithms to test:
	* Naive Bayes
	* Linear Regression
	* Softmax
	* Deep Learning
	* Use distributional similarity to capture meaning of words (by word cooccurence)

- Feature Selection:
	* Use mutual information to assess importance of words.
	* Plot word frequency and come up with metric of fluctuation. 

# Content

- In collectarchive.py: the function NYTmetaquery() downloads the .json metadata file from the archive in the date range [start\_date,end\_date].
- In queryarticles.py: the function QueryArticle downloads all the articles contained in the 'web\_url' links and saves them to the fullarticles directory
- In parsearticles.py: the function Parsehtml() takes opens an html file and finds the content and title (date and author should also be added).
