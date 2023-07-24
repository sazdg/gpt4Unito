import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()
argomento = 'tesi_laurea'
# Leggi il contenuto del file di testo
with open(f'documenti/{argomento}.txt', 'r', encoding='utf-8') as file:
    raw_text = file.read()

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

query = "Come rinunciare all'esame di laurea"
print(query)
docs = docsearch.similarity_search(query)
print(docs)
