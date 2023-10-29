import os
from bardapi import Bard
from dotenv import load_dotenv
import time

def main():
 load_dotenv()

 query = input("Inserisci la domanda: ")
 inizio = time.time()

 token = os.getenv("_BARD_API_KEY")
 bard = Bard(token=token)
 risposta = bard.get_answer(query)['content']
 fine = time.time() - inizio
 file_risposta = open("../documenti/risposte.txt", 'a', encoding='utf-8')
 minuti, secondi = divmod(fine, 60)
 file_risposta.write(f"domanda: {query}\nrisposta: {risposta}\nBARD\ntempo: {int(minuti)} minuti e {int(secondi)} secondi\n\n")
 file_risposta.close()
 print(risposta)

 # problemi di accesso all'api con il token


if __name__ == "__main__":
    main()