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
python clsWebScrapingUnito.py
```


due script per avviare la chat con il modello
```shell
python clsAskHuggingFace.py
python Pinecone.py
```


modelli sperimentati con successo:
* google/flan-t5-xxl, temperature:0.1, max_new_tokens:512 (il migliore)
* google/flan-t5-large, temperature:0.9, max_new_tokens:250 
* google/flan-ul2, temperature:0.1, max_new_tokens:250
* tiiuae/falcon-7b-instruct, temperature:0.9, max_new_tokens:2000 (in inglese e prende da internet)
* EleutherAI/gpt-neox-20b, temperature:0.1, max_new_tokens: 200 (risponde male e troppo testo)

