from bs4 import BeautifulSoup
import requests
import json
import time
import tqdm

class WebScrapingUnito():

    def __init__(self):
        self.progressBar: tqdm = None

    def loading(self, tempo=5):
        time.sleep(tempo)
        self.progressBar.update(1)


    def start(self):
        file = open('./argomenti.json')
        documentazione = json.load(file)
        nLinks = self.countLinks(documentazione)
        self.progressBar = tqdm.tqdm(total=nLinks)


        for tema in documentazione["argomenti"]:
            argomento = tema["titolo"]
            for siti in tema["links"]:
                descrizione = siti["descrizione"]
                url = siti["link"]
                # decommentare per scraping
                #page = requests.get(url)
                #soup = BeautifulSoup(page.text, features='lxml')
                #file = open(f'documenti/{argomento}.txt', 'w', encoding='utf-8')
                #testo = soup.get_text().strip().replace(' ', ' ').replace('keyboard_arrow_down', '').replace('arrow_drop_down', '')
                #file.write(f"\n$${argomento}$$\n" + testo + "\n\n\n")
                #file.close()

                self.loading(1)

        self.progressBar.close()
        self.progressBar = None

    def countLinks(self, jsonLinks):
        l = 0
        for link in jsonLinks["argomenti"]:
            for siti in link["links"]:
                l+=1
        return l

if __name__ == "__main__":
    wbu = WebScrapingUnito()
    wbu.start()

#aggiungere delay per non rischiare di essere bloccati dal server

#otteniamo le informazioni su internet, pulisce il testo
# URL = "https://www.didattica-cps.unito.it/do/home.pl/View?doc=Laurearsi/tesi_laurea.html"

#argomento = 'tesi_laurea'
#page = requests.get(URL)
#soup = BeautifulSoup(page.text, features='lxml')


#file = open(f'documenti/{argomento}.txt', 'w', encoding='utf-8')
#for div in soup.findAll('div', class_='card'):
    #div = div.get_text().strip().replace(' ', ' ').replace('keyboard_arrow_down', '')
    #file.write(div)