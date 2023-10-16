# AI 4 UNITO
GPT 4 Unito with LangChain

# Environment Setup
Prima di eseguire il codice installare le librerie richieste tramite il comando:

```shell
pip3 install -r requirements.txt
```
Creare una copia di "envprova.txt" e rinominarlo in ".env",
Inserire i token richiesti, al momento si utilizza solo HUGGINGFACEHUB_API_TOKEN

per ottenere l'API di hugging face andare sul sito > login utente
in alto a destra nel menù utente > Settings > Access Tokens
creare un uovo token con permesso di lettura


eseguire il seguente file python per ottenere file di testo con la documentazione unito 
```shell
python webscraping.py
```


script con modello
```shell
python main_falcon.py
```


modelli sperimentati:
* google/flan-t5-large, temperature:0.9, max_new_tokens:250 (il migliore)
* tiiuae/falcon-7b-instruct, temperature:0.9, max_new_tokens:2000

