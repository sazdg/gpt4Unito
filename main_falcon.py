
from about_pdf import getObjDocuments
from dotenv import load_dotenv
import time
from langchain import HuggingFaceHub, PromptTemplate, LLMChain
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

def main():

    load_dotenv()
    # Split su numero di caratteri
    documents = getObjDocuments()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # open source embeddings supportato da langchain
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    # database del documento, chunks in vectorstores


    huggingfacehub_api_token = os.environ['HUGGINGFACEHUB_API_TOKEN']
    repo_id = "tiiuae/falcon-7b-instruct"
    llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                         repo_id=repo_id,
                         model_kwargs={"temperature":0.6, "max_new_tokens":2000})

    chain = load_qa_chain(llm, chain_type="stuff")

    query = input("Inserisci la domanda: ")
    docs = db.similarity_search(query)


    inizio = time.time()
    risposta = chain.run(input_documents=docs, question=query)
    print(risposta)
    fine = time.time() - inizio

    file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
    minuti, secondi = divmod(fine, 60)
    file_risposta.write(
        f"domanda: {query}\nrisposta: {risposta}\nFALCON {repo_id} model_kwargs='temperature':0.95, 'max_new_tokens':32)\ntempo: {int(minuti)} minuti e {int(secondi)} secondi\n\n")
    file_risposta.close()


if __name__ == "__main__":
    main()