import requests
from bs4 import BeautifulSoup
import pprint

s = requests.Session()
base = "http://undergrad.cs.umd.edu/home"

s.get(base)
r = s.get(base+"?date=2018-09")
soup = BeautifulSoup(r.text, 'html.parser')

pprint.pprint(soup.find_all('a'))
