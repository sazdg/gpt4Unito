import requests

# Specifica l'URL dell'API del modello Llama
api_url = "https://api-inference.huggingface.co/models/TheBloke/Llama-2-7b-Chat-GGUF"

# Definisci la tua query
query = input("Inserisci la domanda: ")

# Esegui la richiesta API
response = requests.post(api_url, json={"question": query})

# Estrai la risposta
if response.status_code == 200:
    result = response.json()
    answer = result["answer"]
    print("Risposta generata da Llama2:", answer)
else:
    print("Errore nella richiesta API:", response.status_code)
