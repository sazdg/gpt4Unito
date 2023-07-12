import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
load_dotenv()

doc_reader = PdfReader('./documenti/harry_potter_the_sorcerer_s_stone_removed.pdf')
#print(doc_reader)

#estrarre da pdf e salvare in variabile
raw_text = ''
for i, page in enumerate(doc_reader.pages):
	text = page.extract_text()
	if text:
		raw_text += text
#print(len(raw_text))
#print(raw_text[:1000])


#split su numero di caratteri
text_splitter = CharacterTextSplitter(
	separator='\n',
	chunk_size=1000,
	chunk_overlap=200,
	length_function=len,
)
texts=text_splitter.split_text(raw_text)

#print(len(texts))
print(texts[0])

#embedding
print('--------------------------')
embedding = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
docsearch = FAISS.from_texts(texts, embedding)
print(docsearch.embedding_function)

query = "Who was Mr. Dursley?"
docs = docsearch.similarity_search(query)
print(len(docs))
print(docs[0])

