import time
import os
from multipledispatch import dispatch
from ExtractFromDocuments import getObjDocuments, getObjDirectory
from dotenv import load_dotenv
#from langchain import HuggingFaceHub
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

import langid
from clsTraduttore import Traduttore
from clsColors import Colors


class AskHuggingFace:
    def __init__(self, modello, temp, tokens, file, isTerminalMode):
        self._repo_id = modello
        self._query = ""
        self._temperatura = temp
        self._max_tokens = tokens
        self._nome_file = file
        self._risposta = ""
        self._terminalMode: bool = isTerminalMode
        self._keepAsking: bool = isTerminalMode
        self._db = None
        self._chain = None

    def NomeModello(self):
        return self._repo_id

    @dispatch()
    def Query(self):
        return self._query

    @dispatch(str)
    def Query(self, domanda):
        self._query = domanda

    def Temperatura(self):
        return self._temperatura

    def MaxTokens(self):
        return self._max_tokens

    def NomeFile(self):
        return self._nome_file

    def Risposta(self):
        return self._risposta

    def IsTerminalMode(self):
        return self._terminalMode

    def KeepAsking(self):
        return self._keepAsking

    def getObjectDocument(self):
        if self.NomeFile() != '':
            print('Digest file...')
            docs = getObjDocuments(self.NomeFile())
        else:
            print('Digest directory...')
            docs = getObjDirectory()
        return docs

    def Start(self):
        load_dotenv()

        # Lista di chunks del documento
        documents = self.getObjectDocument()
        if documents is None:
            print('Non sono stati trovati documenti da indicizzare')
        # Split su numero di caratteri
        text_splitter = CharacterTextSplitter(separator="\n", length_function=len, chunk_size=550, chunk_overlap=50, is_separator_regex=False)
        docs = text_splitter.split_documents(documents)
        # open source embeddings supportato da langchain
        embeddings = HuggingFaceEmbeddings()
        self._db = FAISS.from_documents(docs, embeddings)
        # database del documento, chunks in vectorstores

        huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']
        print('Initializing Hugging Face Hub')
        llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                             repo_id=self.NomeModello(),
                             model_kwargs={"temperature": self.Temperatura(), "max_new_tokens": self.MaxTokens(), "num_return_sequences": 1})

        self._chain = load_qa_chain(llm, chain_type="stuff")
        print('Model ready')
        if self.IsTerminalMode():
            while self.KeepAsking():
                self.Query(input('Inserisci la domanda: '))
                self.Ask()

    def Ask(self):
        if self._db is None:
            return 'Inizializzare vectorstores prima di cominciare'
        if self._chain is None:
            return 'Inizializzare il modello prima di cominciare'

        if self.Query() == 'esci' or self.Query() == 'exit' or self.Query() == 'quit':
            self._keepAsking = False
            return None

        elif self.Query() != "":
            # se la domanda non è in italiano la traduce perchè i documenti sono in italiano
            linguaDiRisposta = langid.classify(self.Query())
            print("Lingua della domanda: " + linguaDiRisposta[0])
            #queryTradotta = self.RilevaTraduci(self.Query(), 'it')
            #self.Query(queryTradotta)

            chunk = self._db.similarity_search(self.Query())
            if self.IsTerminalMode():
                print(f'{Colors.fg.cyan}Chunks: {chunk}')

            inizio = time.time()
            risposta = self._chain.run(input_documents=chunk, question=self.Query())
            fine = time.time() - inizio

            if self.NomeModello() == "HuggingFaceH4/starchat-beta":
                print(f'{Colors.fg.green}Detected {self.nomeModello()} : {risposta}')
                if "<|system|>" in risposta:
                    fine_risposta = risposta.index("<|system|>")
                    risposta = risposta[0:fine_risposta].replace("<|end|>", "")

            if "Question" in risposta:
                print(f'{Colors.fg.red}Detected Question in risposta: {risposta}')
                fine_risposta = risposta.index("Question")
                risposta = risposta[0:fine_risposta]

            self._risposta = self.RilevaTraduci(risposta, linguaDiRisposta[0])
            print(Colors.reset + risposta)

            valutazione = 'None'
            if self.IsTerminalMode():
                valutazione = input('Risposta corretta? y ⎪ n\n')
            file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
            minuti, secondi = divmod(fine, 60)
            file_risposta.write(
                f"Domanda: {self.Query()}\nRisposta: {self.Risposta()}\n({self.NomeModello()}, temperature:{self.Temperatura()}, max_new_tokens:{self.MaxTokens()}, tempo: {int(minuti)} minuti e {int(secondi)} secondi, valutazione:{valutazione})\n\n")
            file_risposta.close()
            print('\n')

            return risposta
        else:
            return 'Nessuna domanda a cui rispondere...'

    def RilevaTraduci(self, testo, linguaRichiesta):
        risposta = testo
        lingua = langid.classify(testo)
        print(f'{Colors.reset}Lingua rilevata: {lingua[0]}\nLingua richiesta: {linguaRichiesta}')
        if lingua[0] != linguaRichiesta:
            print(f'{Colors.fg.yellow}Detected {lingua[0]}: ' + testo)
            t = Traduttore(lingua[0], linguaRichiesta)
            if len(testo) > 500:
                risposte_lst = t.splitta(testo)
                risposta = t.traduci(risposte_lst)
            else:
                risposta = t.traduci(testo)
        return risposta

# if __name__ == "__main__":
#     try:
#         # se passato nome file vuoto verrà letta la cartella completa
#         modelName = 'HuggingFaceH4/zephyr-7b-beta'
#         documentName = '' # 'prova.odt'
#         temperature = 0.7
#         tokens = 250
#         isDebugMode = True
#
#         hf = AskHuggingFace(modelName, temperature, tokens, documentName, isDebugMode)
#         hf.Start()
#     except ValueError as ve:
#         file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
#         file_risposta.write(
#             f"Domanda: {hf.Query()}\nERRORE: {ve}\n({hf.NomeModello()}, temperature:{hf.Temperatura()}, max_new_tokens:{hf.MaxTokens()})\n\n")
#         file_risposta.close()
#         print(ve)