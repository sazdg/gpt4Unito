import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from clsAskHuggingFace import AskHuggingFace
from costanti import DIR_LOADED_DOCUMENTS, FILE_NAME_TEST, CREDENZIALI
import json



class Server(BaseHTTPRequestHandler):
	def initModello(self, modelname, temperature, tokens, documentname):
		self._nomeModello = modelname
		self._temperatura = temperature
		self._tokens = tokens
		self._nomeDocumento = documentname
		self._askUnito = None
		self._askUnito = AskHuggingFace(modelname, temperature, tokens, documentname, False)
		self._askUnito.Start()

	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header('Content-Type', 'application/json, application/pdf, text/plain'),
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()
		api = self.path.split('/')
		if api == 'file':
			self.do_PUT()

	def set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()

	def set_file_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()

	def do_GET(self):
		self.set_headers()
		api = self.path.split('/')
		match api[1]:
			case 'ping':
				self.wfile.write(json.dumps(({'response': 'pong'})).encode('utf-8'))
			case 'files':
				files_caricati = self.getFilenamesFolder()
				self.wfile.write(json.dumps(({'response': files_caricati, 'conta': len(files_caricati)})).encode('utf-8'))
			case 'restart':
				self._askUnito = None
				self._askUnito = AskHuggingFace(self._nomeModello, self._temperatura, self._tokens, '', False)
				self._askUnito.Start()
				print('Hugging Face Hub ripartito')
				self.wfile.write(json.dumps(({'response': 'Restart completato'})).encode('utf-8'))

	def do_POST(self):
		self.set_headers()
		api = self.path.split('/')
		content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
		post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself
		match api[1]:
			case 'question':
				if post_data['domanda']:
					risposta = 'Modello LLM non inizializzato, controllare e riprovare'
					if self._askUnito is not None:
						self._askUnito.Query(post_data['domanda'])
						risposta = self._askUnito.Ask()

					self.wfile.write(
						json.dumps(({'question': post_data['domanda'], 'response': risposta})).encode('utf-8'))
				else:
					self.wfile.write(
						json.dumps(({'question': 'Nessuna domanda', 'response': 'Nessuna risposta'})).encode('utf-8'))
			case 'modello':
				if post_data['modello']:
					self.wfile.write(json.dumps(({'model': post_data['modello']})).encode('utf-8'))
				else:
					self.wfile.write(json.dumps(({'model': 'Nessun modello scelto'})).encode('utf-8'))
			case 'lingua':
				if post_data['lingua']:
					self.wfile.write(json.dumps(({'response': post_data['lingua']})).encode('utf-8'))
				else:
					self.wfile.write(json.dumps(({'response': 'Nessuna lingua scelta'})).encode('utf-8'))
			case 'login':
				username = post_data['usr']
				password = post_data['pwd']
				if self.checkCredenzialiLogin(username, password):
					self.wfile.write(json.dumps(({'response': 'true'})).encode('utf-8'))
				else:
					self.wfile.write(json.dumps(({'response': 'false'})).encode('utf-8'))

	def do_PUT(self):
		self.set_file_headers()
		api = self.path.split('/')
		leng_file = 0
		path_file = ''

		if len(api) >= 2:
			nome_file = api[2].replace('%20', '_') # <--- Gets the name of the file
			path_file = DIR_LOADED_DOCUMENTS + '/' + nome_file

		if type(self.headers['Content-Length']) is not type(None):  # <--- Gets the size of data sent
			leng_file = int(self.headers['Content-Length'])

		if leng_file > 0 and path_file != '':
			if os.path.exists(path_file):
				response = f'{path_file} esiste già'
				print(response)
			else:
				try:
					with open(path_file, 'wb') as output_file:
						output_file.write(self.rfile.read(leng_file))
					response = f'Salvato file {path_file} con successo!'
					print(response)
				except ValueError:
					response = f'{path_file} cancellato per errori'
					print( 	response)
					os.remove(path_file)
			self.wfile.write(json.dumps(({'response': response})).encode('utf-8'))

	def checkCredenzialiLogin(self, user, password):
		isUser = False
		if user.lower() in CREDENZIALI:
			if CREDENZIALI[user.lower()] == password:
				isUser = True
		return isUser

	def getFilenamesFolder(self, path=''):
		try:
			if path == '':
				path = DIR_LOADED_DOCUMENTS
			files = os.listdir(path)
		except:
			files = []
		return files


# if __name__ == "__main__":
# 	try:
# 		myServer = Server
# 		s = HTTPServer(('localhost', 8080), myServer)
# 		myServer.initModello(myServer)
# 		print('Started http server')
# 		s.serve_forever()
# 	except KeyboardInterrupt:
# 		print('^C received, shutting down server')
# 		s.socket.close()
