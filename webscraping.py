from bs4 import BeautifulSoup
import requests
#install lxml


URL = "https://www.didattica-cps.unito.it/do/home.pl/View?doc=Laurearsi/tesi_laurea.html"

page = requests.get(URL)
soup = BeautifulSoup(page.text, 'lxml')
#print(soup.prettify()) #stampa tutto il file html
title = soup.find('title').get_text()
transcript = soup.get_text()
#print(title)
print(transcript)

with open('documenti/prova.txt', 'w', encoding='utf-8') as file:
    file.write(transcript)

