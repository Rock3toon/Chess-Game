from abc import ABC, abstractmethod


class Pezzo(ABC):
    """Classe di tipo << Entity >> per rappresentare un pezzo degli scacchi.

    Responsabilità:
      - Conservare il colore e il tipo del pezzo (Re, Donna, Torre, Alfiere, Cavallo,
        Pedone).
      - Fornire metodi di conversione tra notazione algebrica ('e4', 'Cf3', ecc.) e 
      coordinate di matrice.
      - Definire l' interfaccia astratta `mossa()` che ogni sottoclasse deve 
      implementare.
      - Consentire l' accesso controllato a colore e tipo tramite getter e setter.
    """  
    
    Conversione = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3,
        'e': 4, 'f': 5, 'g': 6, 'h': 7
    }

    def __init__(self, colore, tipo):
        self._colore = colore  
        # 0 = 'bianco' o 1 = 'nero'
        self._tipo = tipo      
        # 'R' = Re, 'D' = Donna, 'A' = Alfiere, 'C' = Cavallo, 'T' = Torre, 'P' = Pedone

    @abstractmethod
    def mossa(self, mossa_na, scacchiera, partita):
        pass

    @abstractmethod
    def fattibilità(self, mossa_na, scacchiera, partita):
        pass

    @abstractmethod
    def cattura(self, mossa_na, scacchiera, partita):
        pass
    
    def riga_colonna_disambiguazione(self, mossa_na):
        """Restituisce un array con la riga o colonna di disambiguazione, \
        se presenti. Altrimenti, le celle contengono None.
        """  # noqa: D205
        provenienza = [None, None]  # [riga, colonna]
        if "x" in mossa_na:
            mossa_na = mossa_na.replace("x", "")
        p = mossa_na[len(mossa_na) - 3]
        if p.isdigit():
            provenienza[0] = 8 - int(p) # riga
        elif p in self.Conversione:
            provenienza[1] = self.Conversione.get(p)  # colonna
        
        return provenienza
                   
    def Algebrica_a_Matrice(self, posizione):
        colonna = self.Conversione.get(posizione[len(posizione) - 2])
        riga = 8 - int(posizione[len(posizione) - 1])
        return riga, colonna

    def Algebrica_a_Matrice_promozione(self, posizione):
        colonna = self.Conversione.get(posizione[len(posizione) - 3])
        riga = 8 - int(posizione[len(posizione) - 2])
        return riga, colonna     

    def Matrice_a_Algebrica(self, posizione):   
        colonna = chr(posizione[1] + ord('a'))  # 0 -> 'a', 1 -> 'b', ..., 7 -> 'h'
        riga = str(8 - posizione[0])  # 7 -> '1', 6 -> '2', ..., 0 -> '8'
        return colonna + riga    
    
    def set_colore(self, colore):
        self._colore = colore

    def get_colore(self):
        return self._colore
    
    def get_tipo(self):
        return self._tipo   
    
    def set_tipo(self, tipo):
        self._tipo = tipo