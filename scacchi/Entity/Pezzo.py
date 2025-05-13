from abc import ABC, abstractmethod
from Entity.Scacchiera import Scacchiera
from Entity.Partita import Partita
import re

class Pezzo(ABC):
    """Classe di tipo <<Entity>>, per la gestione dei pezzi e delle relative mosse."""
    
    Conversione = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3,
        'e': 4, 'f': 5, 'g': 6, 'h': 7
    }

    def __init__(self, colore, tipo):
        self._colore = colore  # 'bianco' o 'nero'
        self._tipo = tipo      # 'R' = Re, 'D' = Donna, 'A' = Alfiere, 'C' = Cavallo, 'T' = Torre, 'P' = Pedone

    @abstractmethod
    def mossa(self, mossa_na, scacchiera, partita):
        pass

    def Algebrica_a_Matrice(self, posizione):
        if re.match("^[RDTAC]", posizione):
            colonna = self.Conversione.get(posizione[1])
            riga = 8 - int(posizione[2])
        else:
            colonna = self.Conversione.get(posizione[0])
            riga = 8 - int(posizione[1])
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
        self._tipo 
class Pedone(Pezzo):
    def __init__(self, colore):  # inizializza il pedone
        super().__init__(colore, "P")
        self._prima_mossa = True

    def set_prima_mossa(self):
        self._prima_mossa = False

    def get_prima_mossa(self):
        return self._prima_mossa
    
    def out_of_bounds(self, riga, colonna):
        return riga < 0 or riga >= 8 or colonna < 0 or colonna >= 8
    
    def mossa(self, posizione_arrivo, scacchiera, partita):
        # Converte la posizione di arrivo in coordinate della matrice
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(posizione_arrivo)
        
        direzione = 1 if partita.get_turno() == 0 else -1 

        if not self.out_of_bounds(riga_arrivo + 2*direzione, colonna_arrivo) and not self.out_of_bounds(riga_arrivo + direzione, colonna_arrivo) and scacchiera.get_pezzo_scacchiera(riga_arrivo, colonna_arrivo) is None:
            # Determina la direzione del movimento in base al colore del pedone

            partenza_singola = scacchiera.get_pezzo_scacchiera(riga_arrivo + direzione, colonna_arrivo)
            partenza_doppia = scacchiera.get_pezzo_scacchiera(riga_arrivo + 2*direzione, colonna_arrivo)
            
            if scacchiera.get_casa(riga_arrivo + 2*direzione, colonna_arrivo).get_pezzo() is not None and scacchiera.get_casa(riga_arrivo + 2*direzione, colonna_arrivo).get_pezzo().get_tipo() == "P" and partenza_doppia.get_prima_mossa():
                if scacchiera.get_casa(riga_arrivo + direzione, colonna_arrivo).get_pezzo() is None:
                    scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, partenza_doppia) #sposto il pedone con doppia mossa
                    scacchiera.set_pezzo_scacchiera(riga_arrivo + 2*direzione, colonna_arrivo) #cancello il pedone in partenza
                    if partenza_doppia.get_prima_mossa():
                        partenza_doppia.set_prima_mossa()  
                    partita.cambiaturno()  # Cambia il turno dopo la mossa  
                else:
                    print("La mossa non è valida. Il pedone non può muoversi in quella casella. Digita /help per altre informazioni.")         
            elif scacchiera.get_casa(riga_arrivo + direzione, colonna_arrivo).get_pezzo() is not None and scacchiera.get_casa(riga_arrivo + direzione, colonna_arrivo).get_pezzo().get_tipo() == "P":    
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, partenza_singola) #sposto il pedona
                scacchiera.set_pezzo_scacchiera(riga_arrivo + direzione, colonna_arrivo) #cancello il pedone in partenza
                if partenza_singola.get_prima_mossa():
                    partenza_singola.set_prima_mossa()
                partita.cambiaturno()  # Cambia il turno dopo la mossa                      
            else:   
                print("La mossa non è valida. Il pedone non può muoversi in quella casella. Digita /help per altre informazioni.")
        else:   
            print("La mossa non è valida. Il pedone non può muoversi in quella casella. Digita /help per altre informazioni.")

class Torre(Pezzo):
    def __init__(self, colore):  # inizializza la torre
        super().__init__(colore, "T")
    def mossa(self, mossa_na, scacchier, partita):
        pass


class Cavallo(Pezzo):
    def __init__(self, colore):  # inizializza il cavallo
        super().__init__(colore, "C")
    def mossa(self, mossa_na, scacchiera, partita):
        pass


class Alfiere(Pezzo):
    def __init__(self, colore):  # inizializza l'alfiere
        super().__init__(colore, "A")
    def mossa(self, mossa_na, scacchiera, partita):
        pass


class Donna(Pezzo):
    def __init__(self, colore):  # inizializza la donna
        super().__init__(colore, "D")
    def mossa(self, mossa_na, scacchiera, partita):
        pass


class Re(Pezzo):
    def __init__(self, colore):  # inizializza il re
        super().__init__(colore, "R")
    def mossa(self, mossa_na, scacchiera, partita):
        pass