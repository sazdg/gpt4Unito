from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import UnstructuredODTLoader
from langchain.schema import Document


def getRawText(nome_file="") -> str:
	argomento = 'tesi_laurea.txt' if nome_file == "" else nome_file
	raw_text = ''

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

	return raw_text

def getObjDocuments(nome_file="") -> list[Document]:
	argomento = 'tesi_laurea.txt' if nome_file == "" else nome_file

	if ".txt" in argomento:
		loader = TextLoader(f'./documenti/{argomento}')
		documents = loader.load()
	elif ".pdf" in argomento:
		loader = PyPDFLoader(f'./documenti/{argomento}')
		documents = loader.load_and_split()
	elif ".doc" in argomento or ".docx" in argomento:
		loader = UnstructuredWordDocumentLoader(f'./documenti/{argomento}', mode='elements', strategy='fast')
		documents = loader.load_and_split()
	elif ".odt" in argomento:
		loader = UnstructuredODTLoader(f'./documenti/{argomento}')
		documents = loader.load_and_split()
	return documents

def getObjDirectory() -> list[Document]:
	path = './documenti/caricati'
	loader = DirectoryLoader(path, show_progress=True)
	documents = loader.load_and_split()
	return documents
