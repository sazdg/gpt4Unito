from langchain.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import HuggingFaceHub
import os
from langchain.chains.question_answering import load_qa_chain
import pinecone
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
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

llm2 = HuggingFaceHub(huggingfacehub_api_token=api_huggingface_token,
                     repo_id="google/flan-t5-xxl",
                     model_kwargs={"temperature": 0.7, "max_new_tokens": 512,
                                   "num_return_sequences": 1})
docsearch = None

loader = TextLoader("psicologia.txt")
psicologia = loader.load()
txt = CharacterTextSplitter(separator="\n", chunk_size=600, chunk_overlap=100)
documents = txt.split_documents(psicologia)


docsearch = FAISS.from_documents(documents, embeddings)
query= input("Scrivi la domanda:")

print(query)
# Esegui una ricerca di similarità con Pinecone
docs = docsearch.similarity_search(query)
print(docs)

# Carica una catena di QA
chain = load_qa_chain(llm2, chain_type="stuff")

# Esegui la catena di QA con la query e i documenti trovati
results = chain.run(input_documents=docs, question=query)

# Stampa la risposta generata da Llama2
print("Risposta generata:", results)



