from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.document_loaders import UnstructuredODTLoader, UnstructuredPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from langchain.schema import Document
from costanti import PATH_DIR_DOCUMENTS, FILE_NAME_TEST

def getRawText(nome_file="") -> str:
	argomento = FILE_NAME_TEST if nome_file == "" else nome_file
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
	argomento = FILE_NAME_TEST if nome_file == "" else nome_file

	if ".txt" in argomento:
		loader = TextLoader(f'./documenti/{argomento}')
	elif ".pdf" in argomento:
		loader = UnstructuredPDFLoader(f'./documenti/{argomento}')
	elif ".doc" in argomento or ".docx" in argomento:
		loader = UnstructuredWordDocumentLoader(f'./documenti/{argomento}', mode='elements', strategy='fast')
	elif ".odt" in argomento:
		loader = UnstructuredODTLoader(f'./documenti/{argomento}')

	documents = loader.load_and_split()
	return documents

def getObjDirectory() -> list[Document]:
	path = PATH_DIR_DOCUMENTS
	loader = DirectoryLoader(path, show_progress=True)
	documents = loader.load_and_split()
	return documents
