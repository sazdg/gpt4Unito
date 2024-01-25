from http.server import HTTPServer, BaseHTTPRequestHandler
from clsAskHuggingFace import AskHuggingFace
import json

class Server(BaseHTTPRequestHandler):

	def initModello(self):
		self._askUnito = AskHuggingFace('HuggingFaceH4/zephyr-7b-beta', 0.7, 250, 'tesi_laurea.txt', False)
		self._askUnito.Start()

	def do_OPTIONS(self):
		self.send_response(200)
		self.send_header('Content-Type', 'application/json'),
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()
		self.do_GET()

	def set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()

	def do_GET(self):
		self.set_headers()
		api = self.path.split('/')
		match api[1]:
			case 'ping':
				self.wfile.write(json.dumps(({'response':'pong'})).encode())
			case 'question':
				# question/{domanda}
				if len(api) > 2:
					print(api[2].replace('%20',' '))
					self.wfile.write(json.dumps(({'response': api[2].replace('%20',' ')})).encode())
				else:
					self.wfile.write(json.dumps(({'response': 'Nessuna domanda'})).encode())

	def do_POST(self):
		self.set_headers()
		content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
		post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself
		print(post_data)
		api = self.path.split('/')
		match api[1]:
			case 'question':
				if post_data['domanda']:
					#if self._askUnito is None:
					#	self.initModello()
					self._askUnito.Query(post_data['domanda'])
					risposta = self._askUnito.Ask()
					#risposta = "L'esame finale e la tesi sono presentati utilizzando il servizio online fornito dall'ateneo, denominato tesi online. Per ulteriori informazioni su come completare il processo, si consiglia di consultare l'Informativa per l'invio online delle tesi. Gli abstract della prova finale e della tesi saranno pubblicati nell'archivio pubblico del servizio online di tesi.  Nota importante: non saranno più consentite sostituzioni di tesi che sono state caricate in modo errato o richiedono modifiche oltre latermini previsti, eventuali sostituzioni saranno consentite, tramite il servizio online tesi, solo entro i termini previsti.  In sintesi: - Una volta caricato il file, lo studente non può apportare ulteriori modifiche; - Il servizio online tesi può apportare modifiche al file, su richiesta dello studente, solo entro le scadenze specificate; - Dopo le scadenze specificate, non saranno consentite ulteriori modifiche.  Per l'a.a. 2016-17 la finestra per la richiesta del ricorsoai professori è dal 2 ottobre al 9 ottobre 2017, e gli esami si terranno dal 16 ottobre al 26 ottobre"

					self.wfile.write(json.dumps(({'question': post_data['domanda'], 'response': risposta})).encode())
				else:
					self.wfile.write(json.dumps(({'question': 'Nessuna domanda', 'response': 'Nessuna risposta'})).encode())
			case 'modello':
				if post_data['modello']:
					self.wfile.write(json.dumps(({'model': post_data['modello']})).encode())
				else:
					self.wfile.write(json.dumps(({'model': 'Nessun modello scelto'})).encode())
			case 'lingua':
				if post_data['lingua']:
					self.wfile.write(json.dumps(({'response': post_data['lingua']})).encode())
				else:
					self.wfile.write(json.dumps(({'response': 'Nessuna lingua scelta'})).encode())



if __name__ == "__main__":
	try:
		myServer = Server
		s = HTTPServer(('localhost', 8080), myServer)
		myServer.initModello(myServer) # TODO decommentare
		print('Started http server')
		s.serve_forever()
	except KeyboardInterrupt:
		print('^C received, shutting down server')
		s.socket.close()