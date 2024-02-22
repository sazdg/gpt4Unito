import os
import time
from ExtractFromDocuments import getRawText
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

load_dotenv()

raw_text = getRawText("caricati/DocumentazioneUnito.pdf")

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

# print(docs)
nomeModello = 'gpt-3.5-turbo-instruct'
llm = OpenAI(model_name=nomeModello)
chain = load_qa_chain(llm, chain_type="stuff")
# impostazioni template di risposta
keepAsking = True
while keepAsking:
    query = input("Inserisci la domanda:")
    if query == 'esci' or query == 'exit' or query == 'quit':
        keepAsking = False
        break

    docs = docsearch.similarity_search(query)

    # print(template_risposta)
    inizio = time.time()
    risposta_finale = chain.run(input_documents=docs,question=query)
    fine = time.time() - inizio
    print(risposta_finale)
    valutazione = 'None'
    valutazione = input('Risposta corretta? y ⎪ n\n')
    minuti, secondi = divmod(fine, 60)

    path_file_risposte = 'documenti/risposte.txt'
    file_risposta = open(path_file_risposte, 'a', encoding='utf-8')
    file_risposta.write("domanda: "+query+"\n"+"risposta: "+risposta_finale )
    file_risposta.write(
        f"Domanda: {query}\nRispsota: {risposta_finale}\n({nomeModello}, temperature:NULL, max_new_tokens:NULL), tempo: {int(minuti)} minuti e {int(secondi)} secondi, valutazione:{valutazione})\n\n")

    file_risposta.close()