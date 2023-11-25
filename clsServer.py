from http.server import HTTPServer, BaseHTTPRequestHandler
from clsAskHuggingFace import AskHuggingFace
import json
class Server(BaseHTTPRequestHandler):
	def __init__(self):
		self._askUnito = AskHuggingFace()
		self._askUnito.Run()
	def set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
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
					self.wfile.write(json.dumps(({'question': api[2].replace('%20',' ')})).encode())
				else:
					self.wfile.write(json.dumps(({'question': 'Nessuna domanda'})).encode())

	def do_POST(self):
		self.set_headers()
		content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
		post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself
		print(post_data)
		api = self.path.split('/')
		match api[1]:
			case 'question':
				if post_data['domanda']:
					#self._askUnito.Run()
					self.wfile.write(json.dumps(({'question': post_data['domanda'], 'risposta': 'TODO'})).encode())
				else:
					self.wfile.write(json.dumps(({'question': 'Nessuna domanda'})).encode())
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
		s = HTTPServer(('localhost', 8080), Server)
		print('Started http server')
		s.serve_forever()
	except KeyboardInterrupt:
		print('^C received, shutting down server')
		s.socket.close()