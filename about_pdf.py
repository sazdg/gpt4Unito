from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
def getRawText(nome_file=""):
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

def getObjDocuments(nome_file=""):
	argomento = 'tesi_laurea.txt' if nome_file == "" else nome_file
	if ".txt" in argomento:
		loader = TextLoader(f'./documenti/{argomento}')
		documents = loader.load()
	elif ".pdf" in argomento:
		loader = PyPDFLoader(f'./documenti/{argomento}')
		documents = loader.load_and_split()

	return documents
