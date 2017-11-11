from parsearticles import Parsehtml
from bs4 import BeautifulSoup

filename = "education-its-methods-and-aim.html"
path = "./fullarticles/1860_11/"
title, content = Parsehtml(path+filename)
