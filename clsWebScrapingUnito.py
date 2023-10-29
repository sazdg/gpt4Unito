from bs4 import BeautifulSoup
import requests
import json
import time
import tqdm

class WebScrapingUnito():

    def __init__(self):
        self._progressBar: tqdm = None
        self._documentazione = None

    def loading(self, tempo=5):
        time.sleep(tempo)
        self._progressBar.update(1)


    def start(self):
        file = open('./argomenti.json')
        self._documentazione = json.load(file)
        nLinks = self.countLinks()

        self.resetFiles()
        self._progressBar = tqdm.tqdm(total=nLinks)


        for tema in self._documentazione["argomenti"]:
            argomento = tema["titolo"]
            for siti in tema["links"]:
                descrizione = siti["descrizione"]
                url = siti["link"]

                # self.saveTextFromUrl(argomento, descrizione, url) # TODO decommentare per scraping
                # vedi elenco siti su argomenti.json
                self.loading(1)

        self._progressBar.close()
        self._progressBar = None

    def countLinks(self):
        l = 0
        if self._documentazione is not None:
            for link in self._documentazione["argomenti"]:
                l += len(link["links"])
        return l

    def resetFiles(self):
        if self._documentazione is not None:
            for tema in self._documentazione["argomenti"]:
                argomento = tema["titolo"]
                file = open(f'documenti/{argomento}.txt', 'w')
                file.close()
            return True
        else:
            return False

    def saveTextFromUrl(self, myArgomento, myDescrizione, myUrl):
        page = requests.get(myUrl)
        soup = BeautifulSoup(page.text, features='lxml')
        for menu in soup.find('div', class_='pageBody'):
            try:
                menu.extract()
            except:
                pass
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

