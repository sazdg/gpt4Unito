from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from huggingface_hub import hf_hub_download
from langchain import HuggingFaceHub
import os
from langchain.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.question_answering import load_qa_chain
import pinecone
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# Inizializza Pinecone
api_huggingface_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

# Inizializza gli embeddings di Hugging Face
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

pinecone.init(
    api_key=PINECONE_API_KEY,  # Trovato su app.pinecone.io
    environment=PINECONE_API_ENV  # Vicino alla chiave API nella console
)
index_name = "langchainpinecone"

# Carica il testo dal file 'psicologia.txt'
with open('../documenti/psicologia.txt', 'r', encoding='utf-8') as file:
    testo_psicologia = file.read()

# Scarica il modello Llama2
model_name_or_path = "TheBloke/Llama-2-7b-Chat-GGUF"
model_basename = "llama-2-7b-chat.Q4_K_M.gguf"
model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

n_gpu_layers = 20  # Cambia questo valore in base al tuo modello e alla VRAM della tua GPU.
n_batch = 100  # Dovrebbe essere compreso tra 1 e n_ctx, considera la quantità di VRAM nella tua GPU.

# Carica il modello LlamaCpp
llm = LlamaCpp(
    model_path=model_path,
    max_tokens=256,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    n_ctx=1024,
    verbose=False,
)
docsearch = None
# Inizializza docsearch dopo la creazione del modello
#docsearch = Pinecone.from_texts(list(testo_psicologia), embeddings, index_name=index_name)  # Usa testo_psicologia direttamente
loader = TextLoader("../documenti/psicologia.txt")
psicologia = loader.load()
txt = CharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
documents = txt.split_documents(psicologia)
docsearch = FAISS.from_documents(documents, embeddings)
query = input("Inserisci la domanda: ")

# Esegui una ricerca di similarità con Pinecone
docs = docsearch.similarity_search(query)
print(docs)

# Carica una catena di QA
chain = load_qa_chain(llm, chain_type="stuff")

# Esegui la catena di QA con la query e i documenti trovati
results = chain.run(input_documents=docs, question=query)

# Stampa la risposta generata da Llama2
print("Risposta generata da Llama2:", results)
