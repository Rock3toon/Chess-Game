from Pezzo import Pezzo


class Cavallo(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un cavallo degli scacchi."""

    def __init__(self, colore):  # inizializza il cavallo
        super().__init__(colore, "C")


    def mossa(self, mossa_na, scacchiera, partita):
        pass
    

    def fattibilità(self, mossa_na, scacchiera, partita):
        pass


    
    def cattura(self, mossa_na, scacchiera, partita):
        pass