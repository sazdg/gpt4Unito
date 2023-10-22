from langchain.chains import RetrievalQA

from about_pdf import getObjDocuments
from dotenv import load_dotenv
import time
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
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
        text_splitter = CharacterTextSplitter(separator='\n', chunk_size=550, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        # open source embeddings supportato da langchain
        embeddings = HuggingFaceEmbeddings()
        db = Chroma.from_documents(docs, embeddings) ## faiss è molto buono per cercare nei documenti
        # database del documento, chunks in vectorstores

        huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']

        llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                             repo_id=self._repo_id,
                             model_kwargs={"temperature": self._temperatura, "max_new_tokens": self._max_tokens, "num_return_sequences": 1})



        #prompt = PromptTemplate(
        #    input_variables=["context"],
        #    template=template,
        #)
        #chain = load_qa_chain(llm, chain_type="stuff")

        keepAsking = True
        while keepAsking:
            self._query = input("Inserisci la domanda: ")
            if self._query == "esci":
                break
            elif self._query != "":

                docs = db.similarity_search(self._query)
                print(docs)
                inizio = time.time()
                #prompt = prompt.format(context=docs)ù
                print(docs[0].page_content)
                # prepare stuff prompt template
                template = f"""Answer the question as truthfully as possible using the provided text, and if the answer is not contained within the text below, say "Non lo so Sara"
                        Context:{docs[0].page_content}""".strip()
                prompt = PromptTemplate.from_template(template)
                #prompt.format(context=docs[0].page_content)
                chain = LLMChain(prompt=prompt, llm=llm)
                #risposta = chain.run(self._query)

                #print(p)
                #copingchain = load_qa_chain(llm, chain_type="stuff", verbose=True)

                risposta = chain.run(input_documents=docs, question=self._query, prompt=prompt)
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
        hf = AskHuggingFace('google/flan-t5-xxl', 0.9, 250, "psicologia.txt")#'"psicologia.txt")
        hf.main()
    except ValueError as ve:
        file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
        file_risposta.write(
            f"Domanda: {hf._query}\nERRORE: {ve}\n({hf._repo_id}, temperature:{hf._temperatura}, max_new_tokens:{hf._max_tokens})\n\n")
        file_risposta.close()
        print(ve)