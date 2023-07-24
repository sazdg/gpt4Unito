from bs4 import BeautifulSoup
import requests

URL = "https://www.didattica-cps.unito.it/do/home.pl/View?doc=Laurearsi/tesi_laurea.html"

argomento = 'tesi_laurea'
page = requests.get(URL)
soup = BeautifulSoup(page.text, features='lxml')


file = open(f'documenti/{argomento}.txt', 'w', encoding='utf-8')
for div in soup.findAll('div', class_='card'):
    div = div.get_text().strip().replace(' ', ' ').replace('keyboard_arrow_down', '')
    file.write(div)


