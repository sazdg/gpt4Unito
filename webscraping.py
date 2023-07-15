from bs4 import BeautifulSoup
import requests

descrizioniLaurea = []
URL = "https://www.didattica-cps.unito.it/do/home.pl/View?doc=Laurearsi/tesi_laurea.html"

page = requests.get(URL)
soup = BeautifulSoup(page.text, features="html.parser")

# estrarre tutte le occorrenze di un certo tag html
for p in soup.findAll('div', class_='card'):
	descrizioniLaurea.append(p)
	print(p)
	print("-----------")