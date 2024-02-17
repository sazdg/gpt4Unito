from translate import Translator
from textwrap import wrap
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
        translation = ''
        if type(testo) == str:
            translation = self.translator.translate(testo)
        elif type(testo) == list:
            for t in testo:
                translation += self.traduci(t)
        return translation

    def splitta(self, testoLungo):
        lista = wrap(testoLungo, 500)
        return lista


if __name__ == "__main__":
    foo = Traduttore('it', 'en')
    testo = "Eccoti un testo casuale di circa 1000 caratteri:Laria era fresca e vibrante di promesse mentre camminavo lungo il sentiero costeggiato da alberi secolari. Il vento carezzava dolcemente le foglie, creando un sussurro melodioso che sembrava danzare con il canto degli uccelli. Il cielo, dipinto di sfumature di blu e rosa al tramonto, sembrava un dipinto vivente. Mi avventurai più in profondità nel bosco, catturato dall'incanto della natura che mi circondava. Le fronde degli alberi si intrecciavano sopra di me formando un'arcata di verde, filtrando i raggi dorati del sole che penetravano tra i rami. Ogni passo era un'esperienza di scoperta, ogni respiro un'immersione nella vita pulsante della foresta. Mi sedetti su una radice sporgente e chiusi gli occhi, lasciando che i suoni e i profumi mi avvolgessero completamente. Il tempo sembrava dilatarsi, sospeso tra la tranquillità del presente e la promessa di avventure future. Era come se il bosco stesso parlasse al mio cuore, svelando segreti antichi e sussurrando speranze per il domani. E così rimasi lì, immerso nella magia del momento, grato per la bellezza che mi circondava e per il dono prezioso della vita stessa."
    print(len(testo))
    print(foo.traduci(testo))
    # prove testo di 1000 caratteri per limitazione traduzione
