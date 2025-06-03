from Pezzo import Pezzo


class Re(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un re degli scacchi."""

    def __init__(self, colore):  # inizializza il re
        self._prima_mossa = True
        # utile per l'arrocco, garantisce che il re non sia stato ancora mosso
        super().__init__(colore, "R")

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