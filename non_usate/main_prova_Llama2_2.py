from langchain.callbacks.manager import CallbackManager
from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from sentence_transformers import SentenceTransformer
from langchain.chains.question_answering import load_qa_chain
import pinecone
import os
from langchain.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import  StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download
from langchain.llms import HuggingFaceHub


loader = TextLoader('../documenti/tesi_laurea.txt')
data = loader.load()

text_Splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

docs=text_Splitter.split_documents(data) #o split.text
api_huggingface_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
index_name = "langchainpinecone"

docsearch = Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=index_name)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"

model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
n_batch = 256  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# Loading model,
llm = LlamaCpp(
    model_path=model_path,
    max_tokens=256,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    callback_manager=callback_manager,
    n_ctx=1024,
    verbose=False,
)
query = input("Inserisci la domanda: ")
docs = docsearch.similarity_search(query)

chain = load_qa_chain(llm, chain_type="stuff")

chain.run(input_documents=docs, question=query)