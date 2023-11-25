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
from clsTraduttore import Traduttore
from clsColors import Colors

class AskHuggingFace:

    def __init__(self, modello, temp, tokens, file):
        self._repo_id = modello
        self._query = ""
        self._temperatura = temp
        self._max_tokens = tokens
        self._nome_file = file
        self._risposta = ""
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
    def Run(self):
        print("Digest knowledge...")
        # TODO: si può rendere più efficiente? Se già c'è in cache non fare il digest???
        load_dotenv()
        # Lista di documenti
        documents = getObjDocuments(self.NomeFile())
        # Split su numero di caratteri
        text_splitter = CharacterTextSplitter(separator="\n", length_function=len, chunk_size=550, chunk_overlap=50, is_separator_regex=False)
        docs = text_splitter.split_documents(documents)
        # open source embeddings supportato da langchain
        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(docs, embeddings) ## faiss è molto buono per cercare nei documenti
        # database del documento, chunks in vectorstores

        huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']
        print("Initializing Hugging Face Hub")
        llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                             repo_id=self.NomeModello(),
                             model_kwargs={"temperature": self.Temperatura(), "max_new_tokens": self.MaxTokens(), "num_return_sequences": 1})

        chain = load_qa_chain(llm, chain_type="stuff")

        keepAsking = True
        while keepAsking:
            domanda = input("Inserisci la domanda: ")
            self.Query(domanda)
            if self.Query() == "esci" or self.Query() == "exit" or self.Query() == "quit":
                break
            elif self.Query() != "":

                chunk = db.similarity_search(self.Query())
                print(f'{Colors.fg.cyan}Chunks: {chunk}')
                inizio = time.time()
                risposta = chain.run(input_documents=chunk, question=self.Query())
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

                lingua = langid.classify(risposta)
                if lingua[0] != 'it':
                    print(f'{Colors.fg.yellow}Detected {lingua[0]}: ' + risposta)
                    t = Traduttore(lingua[0], 'it')
                    if len(risposta) > 500:
                        risposte_lst = t.splitta(risposta)
                        risposta = t.traduci(risposte_lst)
                    else:
                        risposta = t.traduci(risposta)
                self._risposta = risposta
                print(Colors.reset + risposta)

                valutazione = input('Risposta corretta? y ⎪ n\n')
                file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
                minuti, secondi = divmod(fine, 60)
                file_risposta.write(
                    f"Domanda: {self.Query()}\nRisposta: {self.Risposta()}\n({self.NomeModello()}, temperature:{self.Temperatura()}, max_new_tokens:{self.MaxTokens()}, tempo: {int(minuti)} minuti e {int(secondi)} secondi, valutazione:{valutazione})\n\n")
                file_risposta.close()
                print('\n')
            else:
                print('Nessuna domanda a cui rispondere...')

        del chain



if __name__ == "__main__":
    try:
        hf = AskHuggingFace('HuggingFaceH4/zephyr-7b-beta', 0.7, 250, 'appunti_psicologia_del_lavoro_2023.pdf')#'"psicologia.txt")+ "tesi_laurea.txt"
        hf.Run()
    except ValueError as ve:
        file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
        file_risposta.write(
            f"Domanda: {hf.Query()}\nERRORE: {ve}\n({hf.NomeModello()}, temperature:{hf.Temperatura()}, max_new_tokens:{hf.MaxTokens()})\n\n")
        file_risposta.close()
        print(ve)