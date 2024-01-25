from langchain import PromptTemplate, LLMChain
from langchain.callbacks.base import BaseCallbackManager
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from about_pdf import getRawText
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import time


raw_text = getRawText()

# Split su numero di caratteri
text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=1500,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)
print(f'numero di chunks: {len(texts)}')

#texts = text_splitter.split_text(raw_text)
#text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,chunk_overlap=64)
#texts = text_splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

faiss_index = FAISS.from_texts(texts, embeddings)
faiss_index.save_local("./faiss_index/")


faiss_index = FAISS.load_local("../faiss_index/", embeddings)


query = input("Inserisci la domanda: ")
matched_docs = faiss_index.similarity_search(query, 14)
context = ""
for doc in matched_docs:
    context = context + doc.page_content + " \n\n "

template = """Please use the following context to answer questions.

Question: {question}"""

local_path = ("") #percorso modello ...ggml-vic13b-q5_1

callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])
llm = GPT4All(model=local_path, callback_manager=callback_manager, verbose=True,repeat_last_n=0)
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


inizio = time.time()
risposta_finale = llm_chain.run(query)
fine = time.time() - inizio
file_risposta = open("../documenti/risposte.txt", 'a', encoding='utf-8')
minuti, secondi = divmod(fine, 60)
file_risposta.write(f"domanda: {query}\nrisposta: {risposta_finale}\nGPT4ALL\ntempo: {int(minuti)} minuti e {int(secondi)} secondi\n\n")
file_risposta.close()