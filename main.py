from http.server import HTTPServer

from clsAskHuggingFace import AskHuggingFace
from clsServer import Server

if __name__ == "__main__":

	# se passato nome file vuoto verrà letta la cartella "documenti/caricati"
	modelName = 'HuggingFaceH4/zephyr-7b-beta'
	documentName = ''
	temperature = 0.7
	tokens = 250
	isDebugMode = True
	portaServer = 8080

	if not isDebugMode:
		try:
			myServer = Server
			s = HTTPServer(('localhost', portaServer), myServer)
			myServer.initModello(myServer, modelName, temperature, tokens, documentName)
			print('Started http server')
			s.serve_forever()
		except KeyboardInterrupt:
			print('^C received, shutting down server')
			s.socket.close()
	else:
		try:
			hf = AskHuggingFace(modelName, temperature, tokens, documentName, isDebugMode)
			hf.Start()
		except ValueError as ve:
			file_risposta = open("documenti/risposte.txt", 'a', encoding='utf-8')
			file_risposta.write(
				f"Domanda: {hf.Query()}\nERRORE: {ve}\n({hf.NomeModello()}, temperature:{hf.Temperatura()}, max_new_tokens:{hf.MaxTokens()})\n\n")
			file_risposta.close()
			print(ve)
