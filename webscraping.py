from bs4 import BeautifulSoup
import requests
import json

file = open('./argomenti.json')
documentazione = json.load(file)
for tema in documentazione["argomenti"]:
    argomento = tema["titolo"]

    for siti in tema["links"]:
        descrizione = siti["descrizione"]
        url = siti["link"]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features='lxml')
        file = open(f'documenti/{argomento}.txt', 'w', encoding='utf-8')
        testo = soup.get_text().strip().replace(' ', ' ').replace('keyboard_arrow_down', '').replace('arrow_drop_down', '')
        file.write(f"\n$${argomento}$$\n" + testo + "\n\n\n")
        file.close()

#otteniamo le informazioni su internet, pulisce il testo
# URL = "https://www.didattica-cps.unito.it/do/home.pl/View?doc=Laurearsi/tesi_laurea.html"

#argomento = 'tesi_laurea'
#page = requests.get(URL)
#soup = BeautifulSoup(page.text, features='lxml')


#file = open(f'documenti/{argomento}.txt', 'w', encoding='utf-8')
#for div in soup.findAll('div', class_='card'):
    #div = div.get_text().strip().replace(' ', ' ').replace('keyboard_arrow_down', '')
    #file.write(div)