from abc import ABC, abstractmethod

class Pezzo(ABC):
    """Classe di tipo <<  Entity >>, per la gestione dei pezzi e delle relative mosse."""
    
    def __init__(self, colore, tipo):
        self._colore = colore  # 0 = bianco, 1 = nero
        self._tipo = tipo      # 'R' = Re, 'D' = Donna, 'A' = Alfiere, 'C' = Cavallo, 'T' = Torre, 'P' = Pedone

    @abstractmethod
    def mossa(self, mossa_na, scacchiera):
        pass
    
    def set_colore(self, colore):
        self._colore = colore

    def get_colore(self):
        return self._colore
    
    def get_tipo(self):
        return self._tipo   
    
    def set_tipo(self, tipo):
        self._tipo = tipo


class Pedone(Pezzo):
    def __init__(self, colore):  # inizializza il pedone
        super().__init__(colore, "P")
        self._prima_mossa = True
    def mossa(self, mossa_na, scacchiera):
        pass
    def set_prima_mossa(self):
        self._prima_mossa = False

class Torre(Pezzo):
    def __init__(self, colore):  # inizializza la torre
        super().__init__(colore, "T")
    def mossa(self, mossa_na, scacchiera):
        pass


class Cavallo(Pezzo):
    def __init__(self, colore):  # inizializza il cavallo
        super().__init__(colore, "C")
    
    def mossa(self, mossa_na, scacchiera):
        pass


class Alfiere(Pezzo):
    def __init__(self, colore):  # inizializza l'alfiere
        super().__init__(colore, "A")
    def mossa(self, mossa_na, scacchiera):
        pass


class Donna(Pezzo):
    def __init__(self, colore):  # inizializza la donna
        super().__init__(colore, "D")
    def mossa(self, mossa_na, scacchiera):
        pass


class Re(Pezzo):
    def __init__(self, colore):  # inizializza il re
        super().__init__(colore, "R")
    def mossa(self, mossa_na, scacchiera):
        pass