class Casa:
    """Classe di tipo <<Entity>> per gestire una singola casella della scacchiera.

    Responsabilità:
        - Memorizzare la posizione (riga, colonna) della casella.
        - Contenere (o meno) il pezzo attualmente presente.
        - Fornire metodi di accesso e modifica del pezzo in essa posizionato.
    """

    def __init__(self, riga, colonna, pezzo=None):
        self._riga = riga
        self._colonna = colonna
        self._pezzo = pezzo  

    def get_pezzo(self):
        return self._pezzo

    def set_pezzo(self, pezzo):
        self._pezzo = pezzo

    def get_riga(self):
        return self._riga
    
    def set_riga(self, riga):
        self._riga = riga

    def get_colonna(self):
        return self._colonna
    
    def set_colonna(self, colonna):
        self._colonna = colonna
