from multipledispatch import dispatch
from about_pdf import getObjDocuments
from dotenv import load_dotenv
import time
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

import langid
from Traduttore import Traduttore

class AskHuggingFace:

    def __init__(self, modello, temp, tokens, file):
        self._repo_id = modello
        self._query = ""
        self._temperatura = temp
        self._max_tokens = tokens
        self._nome_file = file
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
    def main(self):

        load_dotenv()
        # Split su numero di caratteri
        documents = getObjDocuments(self.NomeFile())
        text_splitter = CharacterTextSplitter(separator="\n", length_function=len, chunk_size=550, chunk_overlap=50, is_separator_regex=False)
        docs = text_splitter.split_documents(documents)
        # open source embeddings supportato da langchain
        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(docs, embeddings) ## faiss è molto buono per cercare nei documenti
        # database del documento, chunks in vectorstores

        huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

        llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                             repo_id=self.NomeModello(),
                             model_kwargs={"temperature": self.Temperatura(), "max_new_tokens": self.MaxTokens(), "num_return_sequences": 1})

  
        chain = load_qa_chain(llm, chain_type="stuff")

        keepAsking = True
        while keepAsking:
            domanda = input("Inserisci la domanda: ")
            self.Query(domanda)
            if self.Query() == "esci":
                break
            elif self.Query() != "":

                chunk = db.similarity_search(self.Query())
                print(chunk)
                inizio = time.time()
                risposta = chain.run(input_documents=chunk, question=self.Query())
                fine = time.time() - inizio
                lingua = langid.classify(risposta)
                if lingua[0] != 'it':
                    print(f'detected {lingua[0]}: ' + risposta)
                    t = Traduttore(lingua[0], 'it')
                    risposta = t.traduci(risposta)

                print(risposta)

                file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
                minuti, secondi = divmod(fine, 60)
                file_risposta.write(
                    f"Domanda: {self.Query()}\nRisposta: {risposta}\n({self.NomeModello()}, temperature:{self.Temperatura()}, max_new_tokens:{self.MaxTokens()}, tempo: {int(minuti)} minuti e {int(secondi)} secondi)\n\n")
                file_risposta.close()
                print('\n')
            else:
                print('Nessuna domanda a cui rispondere...')

        del chain



if __name__ == "__main__":
    try:
        hf = AskHuggingFace('google/flan-t5-xxl', 0.1, 200, "psicologia.txt")#'"psicologia.txt")+
        hf.main()
    except ValueError as ve:
        file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
        file_risposta.write(
            f"Domanda: {hf.Query()}\nERRORE: {ve}\n({hf.NomeModello()}, temperature:{hf.Temperatura()}, max_new_tokens:{hf.MaxTokens()})\n\n")
        file_risposta.close()
        print(ve)