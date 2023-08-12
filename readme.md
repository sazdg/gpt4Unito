# Argomento
GPT 4 Unito with LangChain

# Environment Setup
Prima di eseguire il codice installare le librerie richieste tramite il comando:

```shell
pip3 install -r requirements.txt
```
Creare una copia di "envprova.txt" e rinominarlo in ".env",
Inserire i token richiesti, al momento è necessario solo OPENAI_API_KEY

eseguire il seguente file python per ottenere file di testo con la documentazione unito 
```shell
python webscraping.py
python main_openai.py
```
oppure
```shell
python main_gpt4all.py
```