from Pezzo import Pezzo


class Torre(Pezzo):
    """Classe di tipo << Entity >> per rappresentare una torre degli scacchi."""

    def __init__(self, colore):  # inizializza la torre

        self._prima_mossa = True  
        #utile per l' arrocco, garantisce che la torre non sia stata ancora mossa
        super().__init__(colore, "T")
        

    def set_prima_mossa(self, prima_mossa):
        if prima_mossa:
            self._prima_mossa = False

    def get_prima_mossa(self):
        return self._prima_mossa

    def mossa(self, mossa_na, scacchiera, partita):
        pass

    def fattibilità(self, mossa_na, scacchiera, partita):
        pass

    def cattura(self, mossa_na, scacchiera, partita):
        pass

