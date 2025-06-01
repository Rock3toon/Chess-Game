from Pezzo import Pezzo


class Donna(Pezzo):
    """Classe di tipo << Entity >> per rappresentare una donna degli scacchi."""

    def __init__(self, colore):  # inizializza la donna
        super().__init__(colore, "D")
    
    
    def mossa(self, mossa_na, scacchiera, partita):
        pass

    def fattibilità(self, mossa_na, scacchiera, partita):
        pass


    
    def cattura(self, mossa_na, scacchiera, partita):
        pass