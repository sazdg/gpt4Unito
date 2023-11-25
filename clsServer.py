from http.server import HTTPServer, BaseHTTPRequestHandler
import json
class Server(BaseHTTPRequestHandler):
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
				if len(api) > 2:
					self.wfile.write(json.dumps(({'question': api[2].replace('%20',' ')})).encode())
				else:
					self.wfile.write(json.dumps(({'question': 'Nessuna domanda'})).encode())
	def do_POST(self):
		self.set_headers()

if __name__ == "__main__":
	try:
		s = HTTPServer(('localhost', 8080), Server)
		print('Started http server')
		s.serve_forever()
	except KeyboardInterrupt:
		print('^C received, shutting down server')
		s.socket.close()