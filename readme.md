# DOcuBot

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

Per avviare il server:
```shell
python main.py
```

# Risoluzione problemi Word
in caso di errori dovuti alla lettura di documenti Word:
> [nltk_data] Error loading punkt: <urlopen error [SSL:
> [nltk_data]     CERTIFICATE_VERIFY_FAILED] certificate verify failed:
> 
cercare *'Install Certificates.command'* nella barra di ricerca e aprirlo
eseguire il comando

# Risoluzione problemi Odt
in caso di errori dovuti alla lettura di documenti Odt è necessario installare pandoc
Pandoc è un convertitore di documenti universale
Mac terminale:
```shell
brew install pandoc
```
Windows terminale oppure tramite zip:
```shell
choco install pandoc
```
Linux
```shell
sudo dpkg -i $DEB
ar p $DEB data.tar.gz | tar xvz --strip-components 2 -C $DEST
```


# Modelli sperimentati con successo
* google/flan-t5-xxl, temperature:0.1, max_new_tokens:512 (il migliore)
* HuggingFaceH4/zephyr-7b-beta', temperatura:0.7, max_new_tokens:256 (buono)
* google/flan-t5-large, temperature:0.9, max_new_tokens:250 
* google/flan-ul2, temperature:0.1, max_new_tokens:250
* tiiuae/falcon-7b-instruct, temperature:0.9, max_new_tokens:2000 (in inglese e prende da internet)
* EleutherAI/gpt-neox-20b, temperature:0.1, max_new_tokens: 200 (risponde male e troppo testo)

