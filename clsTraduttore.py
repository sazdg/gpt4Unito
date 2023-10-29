from translate import Translator
class Traduttore():
    def __init__(self):
        self._lingua_input = None
        self._lingua_output = None
        self.translator = Translator(to_lang=self._lingua_output, from_lang=self._lingua_input)

    def __init__(self, in_lingua, out_lingua):
        self._lingua_input = in_lingua
        self._lingua_output = out_lingua
        self.translator = Translator(to_lang=self._lingua_output, from_lang=self._lingua_input)

    def setLinguaInput(self, linguaInput):
        self._lingua_input = linguaInput

    def getLinguaInput(self):
        return self._lingua_input

    def setLinguaOutput(self, linguaOutput):
        self._lingua_output = linguaOutput

    def getLinguaOutput(self):
        return self._lingua_output

    def traduci(self, testo):
        translation = self.translator.translate(testo)
        return translation


