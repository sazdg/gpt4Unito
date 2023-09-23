import os

from about_pdf import getRawTest
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

load_dotenv()

raw_text = getRawTest()

# Split su numero di caratteri
text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)
print('Numero di chunks:', len(texts))

# Embedding
print('--------------------------')
embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
docsearch = FAISS.from_texts(texts, embedding)
print(docsearch.embedding_function)

query = input("Inserisci la domanda:")
docs = docsearch.similarity_search(query)
# print(docs)

chain = load_qa_chain(OpenAI(),chain_type="stuff")
# impostazioni template di risposta
template_risposta = chain.llm_chain.prompt.template
# print(template_risposta)
risposta_finale = chain.run(input_documents=docs,question=query)
print(risposta_finale)

file_risposta = open("documenti/risposte.txt",'a',encoding='utf-8')
file_risposta.write("domanda: "+query+"\n"+"risposta: "+risposta_finale+"\nOPENAI\n")
file_risposta.close()
