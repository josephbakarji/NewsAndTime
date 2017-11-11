from bs4 import BeautifulSoup
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
t, d = MosesTokenizer(), MosesDetokenizer()

def Parsehtml(file_path):

	myfile = open(file_path, 'r').read()
	soup = BeautifulSoup(myfile, "html5lib")
	title = soup.title
	
	body1 = soup.find_all("p", class_="story-body-text story-content")
	body0 = soup.find_all("p", itemprop="articleBody")
	if (len(body1)!=0):
		content = body1
	elif(len(body0)!=0):
		content = body0
	else:
		print("Content not found")

	purecontent = [c.string for c in content]
	


	return title, purecontent

def Tokenizer(mystrings):
	
	tokstr = t.tokenize(mystring)


if __name__ == "__main__":
	filename = "education-its-methods-and-aim.html"
	path = "./fullarticles/1860_11/"
	title, content = Parsehtml(path+filename)


