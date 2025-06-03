from Pezzo import Pezzo


class Alfiere(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un alfiere degli scacchi."""

    def __init__(self, colore):  # inizializza l'alfiere
        super().__init__(colore, "A")


    def mossa(self, mossa_na, scacchiera, partita):
        pass

    def fattibilità(self, mossa_na, scacchiera, partita):
        pass

    def cattura(self, mossa_na, scacchiera, partita):
        pass