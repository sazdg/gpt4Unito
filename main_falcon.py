
from about_pdf import getObjDocuments
from dotenv import load_dotenv
import time
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

class AskHuggingFace:

    def __init__(self, modello, temp, tokens, file):
        self._repo_id = modello
        self._query = ""
        self._temperatura = temp
        self._max_tokens = tokens
        self._nome_file = file

    def main(self):

        load_dotenv()
        # Split su numero di caratteri
        documents = getObjDocuments(self._nome_file)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        # open source embeddings supportato da langchain
        embeddings = HuggingFaceEmbeddings()
        db = FAISS.from_documents(docs, embeddings) ## faiss è molto buono per cercare nei documenti
        # database del documento, chunks in vectorstores

        huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

        llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                             repo_id=self._repo_id,
                             model_kwargs={"temperature": self._temperatura, "max_new_tokens": self._max_tokens, "num_return_sequences": 1})

        chain = load_qa_chain(llm, chain_type="stuff")

        keepAsking = True
        while keepAsking:
            self._query = input("Inserisci la domanda: ")
            if self._query == "esci":
                break
            elif self._query != "":
                docs = db.similarity_search(self._query)
                print(docs)
                inizio = time.time()
                risposta = chain.run(input_documents=docs, question=self._query)
                print(risposta)
                fine = time.time() - inizio

                file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
                minuti, secondi = divmod(fine, 60)
                file_risposta.write(
                    f"Domanda: {self._query}\nRisposta: {risposta}\n({self._repo_id}, temperature:{self._temperatura}, max_new_tokens:{self._max_tokens}, tempo: {int(minuti)} minuti e {int(secondi)} secondi)\n\n")
                file_risposta.close()
                print('\n')
            else:
                print('Nessuna domanda a cui rispondere...')

        del chain



if __name__ == "__main__":
    try:
        hf = AskHuggingFace('tiiuae/falcon-7b-instruct', 0.9, 2000, "tesi_laurea.txt")#'"psicologia.txt")
        hf.main()
    except ValueError as ve:
        file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
        file_risposta.write(
            f"Domanda: {hf._query}\nERRORE: {ve}\n({hf._repo_id}, temperature:{hf._temperatura}, max_new_tokens:{hf._max_tokens})\n\n")
        file_risposta.close()
        print(ve)