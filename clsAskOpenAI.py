import time
import os

from langchain import OpenAI
from multipledispatch import dispatch
from ExtractFromDocuments import getObjDocuments, getObjDirectory
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings

import langid
from clsTraduttore import Traduttore
from clsColors import Colors


class AskOpenAI:
	def __init__(self, modello, file, isTerminalMode):
		self._repo_id = modello
		self._query = ""
		self._nome_file = file
		self._risposta = ""
		self._terminalMode: bool = isTerminalMode
		self._keepAsking: bool = isTerminalMode
		self._db = None
		self._chain = None

	def NomeModello(self):
		return self._repo_id

	@dispatch()
	def Query(self):
		return self._query

	@dispatch(str)
	def Query(self, domanda):
		self._query = domanda

	def NomeFile(self):
		return self._nome_file

	def Risposta(self):
		return self._risposta

	def IsTerminalMode(self):
		return self._terminalMode

	def KeepAsking(self):
		return self._keepAsking

	def getObjectDocument(self):
		if self.NomeFile() != '':
			print('Digest file...')
			docs = getObjDocuments(self.NomeFile())
		else:
			print('Digest directory...')
			docs = getObjDirectory()
		return docs

	def digestDocuments(self):
		# Lista di chunks del documento
		documents = self.getObjectDocument()
		if not documents:
			print('Non sono stati trovati documenti da indicizzare')
			return None
		# Split su numero di caratteri
		text_splitter = CharacterTextSplitter(separator="\n", length_function=len, chunk_size=550, chunk_overlap=50,
											  is_separator_regex=False)
		docs = text_splitter.split_documents(documents)
		# open source embeddings supportato da langchain
		huggingfacehub_api_token = os.environ['OPENAI_API_KEY']
		embeddings = OpenAIEmbeddings(openai_api_key=huggingfacehub_api_token)
		self._db = FAISS.from_documents(docs, embeddings)
		# database del documento, chunks in vectorstores

	def Start(self):
		load_dotenv()

		self.digestDocuments()
		llm = OpenAI(model_name=self.NomeModello())

		self._chain = load_qa_chain(llm, chain_type="stuff")
		print(self.NomeModello() + ' ready')
		if self.IsTerminalMode():
			while self.KeepAsking():
				self.Query(input('Inserisci la domanda: '))
				self.Ask()

	def Ask(self):
		if self._db is None:
			return 'Inizializzare vector stores prima di cominciare'
		if self._chain is None:
			return 'Inizializzare il modello prima di cominciare'

		if self.Query() == 'esci' or self.Query() == 'exit' or self.Query() == 'quit':
			self._keepAsking = False
			return None

		elif self.Query() != "":
			# se la domanda non è in italiano la traduce perchè i documenti sono in italiano
			linguaDiRisposta = langid.classify(self.Query())
			print("Lingua della domanda: " + linguaDiRisposta[0])
			# queryTradotta = self.RilevaTraduci(self.Query(), 'it')
			# self.Query(queryTradotta)

			chunk = self._db.similarity_search(self.Query())
			if self.IsTerminalMode():
				print(f'{Colors.fg.cyan}Chunks: {chunk}')

			inizio = time.time()
			risposta = self._chain.run(input_documents=chunk, question=self.Query())
			fine = time.time() - inizio

			self._risposta = self.RilevaTraduci(risposta, linguaDiRisposta[0]).strip()
			print(Colors.reset + self.Risposta())

			valutazione = ''
			if self.IsTerminalMode():
				valutazione = input('Risposta corretta? y ⎪ n\n') or 'None'
			file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
			minuti, secondi = divmod(fine, 60)
			file_risposta.write(
				f"Domanda: {self.Query()}\nRisposta: {self.Risposta()}\n({self.NomeModello()}, tempo: {int(minuti)} minuti e {int(secondi)} secondi, valutazione:{valutazione})\n\n")
			file_risposta.close()
			print('\n')

			return self.Risposta()
		else:
			return 'Nessuna domanda a cui rispondere...'

	def RilevaTraduci(self, testo, linguaRichiesta) -> str:
		risposta = testo
		lingua = langid.classify(testo)
		print(f'{Colors.reset}Lingua rilevata: {lingua[0]}\nLingua richiesta: {linguaRichiesta}')
		if lingua[0] != linguaRichiesta:
			print(f'{Colors.fg.yellow}Detected {lingua[0]}: ' + testo)
			t = Traduttore(lingua[0], linguaRichiesta)
			if len(testo) > 500:
				risposte_lst = t.splitta(testo)
				risposta = t.traduci(risposte_lst)
			else:
				risposta = t.traduci(testo)
		return risposta

# if __name__ == "__main__":
#     try:
#         # se passato nome file vuoto verrà letta la cartella completa
#         modelName = 'HuggingFaceH4/zephyr-7b-beta'
#         documentName = '' # 'prova.odt'
#         temperature = 0.7
#         tokens = 250
#         isDebugMode = True
#
#         hf = AskHuggingFace(modelName, temperature, tokens, documentName, isDebugMode)
#         hf.Start()
#     except ValueError as ve:
#         file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
#         file_risposta.write(
#             f"Domanda: {hf.Query()}\nERRORE: {ve}\n({hf.NomeModello()}, temperature:{hf.Temperatura()}, max_new_tokens:{hf.MaxTokens()})\n\n")
#         file_risposta.close()
#           print(ve)
