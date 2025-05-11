class Casa:
    """Classe di tipo <<  Entity >>, per la gestione della singola casa della scacchiera."""
    
    def __init__(self, riga, colonna, pezzo=None):
        self._riga = riga            
        self._colonna = colonna      
        self._pezzo = pezzo  

    def get_pezzo(self):
        return self._pezzo

    def set_pezzo(self, pezzo):
        self._pezzo = pezzo
