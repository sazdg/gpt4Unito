import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import time
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI

load_dotenv()
argomento = 'tesi_laurea.txt'
raw_text = ''


if ".txt" in argomento:
    # Leggi il contenuto del file di testo
    with open(f'./documenti/{argomento}', 'r', encoding='utf-8') as file:
        raw_text = file.read()

elif ".pdf" in argomento:
    doc_reader = PdfReader(f'./documenti/{argomento}')
    for i, page in enumerate(doc_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text


# Set your input text

inizio = time.time()

# caricare il file
from langchain.document_loaders import TextLoader
loader = TextLoader(f'./documenti/{argomento}')
documents = loader.load()

# Split su numero di caratteri
print("splitting text...")
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# open source embeddings supportato da langchain
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings()

print("vectoring chunks...")
from langchain.vectorstores import FAISS
db = FAISS.from_documents(docs, embeddings)
# database del documento, chunks in vectorstores

print('connecting to mind...')
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
llm = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature":0, "max_length":512})
chain = load_qa_chain(llm, chain_type="stuff")


query = input("Inserisci la domanda: ")
docs = db.similarity_search(query)
print("elaborating question...")
risposta = chain.run(input_documents=docs, question=query)

fine = time.time() - inizio

file_risposta = open("documenti/risposte.txt",'a',encoding='utf-8')
minuti, secondi = divmod(fine, 60)
file_risposta.write(f"domanda: {query}\nrisposta: {risposta}\nHUGGING FACE\ntempo: {int(minuti)} minuti e {int(secondi)} secondi\n\n")
file_risposta.close()



#
# # Split su numero di caratteri
# text_splitter = CharacterTextSplitter(
#     separator='\n',
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len,
# )
# texts = text_splitter.split_text(raw_text)
# print('Numero di chunks:', len(texts))
#
# # Embedding
# print('--------------------------')
# embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
# docsearch = FAISS.from_texts(texts, embedding)
# print(docsearch.embedding_function)
#
# query = input("Inserisci la domanda:")
# docs = docsearch.similarity_search(query)
# # print(docs)
#
# chain = load_qa_chain(OpenAI(),chain_type="stuff")
# # impostazioni template di risposta
# template_risposta = chain.llm_chain.prompt.template
# # print(template_risposta)
# risposta_finale = chain.run(input_documents=docs,question=query)
# print(risposta_finale)
#
# file_risposta = open("documenti/risposte.txt",'a',encoding='utf-8')
# file_risposta.write("domanda: "+query+"\n"+"risposta: "+risposta_finale+"\n"+"\n")
# file_risposta.close()
