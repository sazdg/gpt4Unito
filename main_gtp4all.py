from langchain import PromptTemplate, LLMChain
from langchain.callbacks.base import BaseCallbackManager
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import time

argomento = 'tesi_laurea.txt'
raw_text = ''


print(f'lettura del file {argomento}...')
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

print('text splitting...')
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
print('fase di embedding...')
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

faiss_index = FAISS.from_texts(texts, embeddings)
faiss_index.save_local("./faiss_index/")

print("loading indexes...")
faiss_index = FAISS.load_local("./faiss_index/", embeddings)
print("index loaded...")


query = input("Inserisci la domanda: ")
matched_docs = faiss_index.similarity_search(query, 14)
context = ""
for doc in matched_docs:
    context = context + doc.page_content + " \n\n "

template = """Please use the following context to answer questions.

Question: {question}"""

local_path = ("/Volumes/ACAI_BOWL/LLM_models/ggml-vic13b-q5_1")
print('base call backmanager....')
callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])
print('nuovo oggetto gpt4all....')
llm = GPT4All(model=local_path, callback_manager=callback_manager, verbose=True,repeat_last_n=0)
print('nuovo oggetto prompt template....')
prompt = PromptTemplate(template=template, input_variables=["question"])
print('nuovo oggetto llmchain....')
llm_chain = LLMChain(prompt=prompt, llm=llm)


print('sto pensando....')
inizio = time.time()
risposta_finale = llm_chain.run(query)
fine = time.time() - inizio
file_risposta = open("documenti/risposte.txt",'a',encoding='utf-8')
minuti, secondi = divmod(fine, 60)
file_risposta.write(f"domanda: {query}\nrisposta: {risposta_finale}\ntempo: {int(minuti)} minuti e {int(secondi)} secondi\n\n")
file_risposta.close()