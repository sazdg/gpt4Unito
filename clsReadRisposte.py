
class clsReadRisposte():
    def __init__(self):
        self._modelli = {}

    def getNumModelli(self):
        return len(self._modelli)

    def GetNomeModelli(self, orderByKey):
        if orderByKey:
            modelli = dict(sorted(self._modelli.items()))
        else:
            modelli = dict(sorted(self._modelli.items(), key=lambda t: t[1]))
        lista = '\n'
        for mll in modelli.keys():
            lista += mll + ' ' + str(modelli[mll]) + '\n'
        return lista

    def GetAffidabilitaModelli(self):
        # TODO calcolo risposte corrette/scorrette
        return -1

    def conta(self):
        file = open(f'documenti/risposte.txt', 'r')
        for risp in file:
            if "(" in risp:
                if 'temperature' in risp:
                    i = risp.index('temperature')
                    nome_modello = risp[1:i-2]
                    if nome_modello not in self._modelli.keys():
                        self._modelli[nome_modello] = 1
                    else:
                        self._modelli[nome_modello] += 1


if __name__ == "__main__":
    try:
        rr = clsReadRisposte()
        rr.conta()
        print("Modelli testati: " + str(rr.getNumModelli()))
        print("Elenco modelli: " + str(rr.GetNomeModelli(False)))
    except ValueError as ve:
        print(ve)