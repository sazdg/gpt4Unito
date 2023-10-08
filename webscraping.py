from bs4 import BeautifulSoup
import requests
import json
import time
import tqdm

class WebScrapingUnito():

    def __init__(self):
        self.progressBar: tqdm = None
        self.documentazione = None

    def loading(self, tempo=5):
        time.sleep(tempo)
        self.progressBar.update(1)


    def start(self):
        file = open('./argomenti.json')
        self.documentazione = json.load(file)
        nLinks = self.countLinks()

        self.resetFiles()
        self.progressBar = tqdm.tqdm(total=nLinks)


        for tema in self.documentazione["argomenti"]:
            argomento = tema["titolo"]
            for siti in tema["links"]:
                descrizione = siti["descrizione"]
                url = siti["link"]

                # self.saveTextFromUrl(argomento, descrizione, url) # TODO decommentare per scraping
                self.loading(1)

        self.progressBar.close()
        self.progressBar = None

    def countLinks(self):
        l = 0
        if self.documentazione is not None:
            for link in self.documentazione["argomenti"]:
                l += len(link["links"])
        return l

    def resetFiles(self):
        if self.documentazione is not None:
            for tema in self.documentazione["argomenti"]:
                argomento = tema["titolo"]
                file = open(f'documenti/{argomento}.txt', 'w')
                file.close()
            return True
        else:
            return False

    def saveTextFromUrl(self, myArgomento, myDescrizione, myUrl):
        page = requests.get(myUrl)
        soup = BeautifulSoup(page.text, features='lxml')
        file = open(f'documenti/{myArgomento}.txt', 'w', encoding='utf-8')
        testo = soup.get_text()
        file.write(f"\n$${myArgomento}$$\n" + self.cleanText(testo) + "\n\n\n")
        file.close()

    def cleanText(self, text):
        return text.strip().replace(' ', ' ').replace('keyboard_arrow_down', '').replace('arrow_drop_down', '')


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