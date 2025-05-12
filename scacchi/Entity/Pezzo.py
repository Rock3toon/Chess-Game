from abc import ABC, abstractmethod
from Entity.Scacchiera import Scacchiera
from Entity.Partita import Partita
import re

class Pezzo(ABC):
    """Classe di tipo <<Entity>>, per la gestione dei pezzi e delle relative mosse."""
    
    Conversione = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4,
        'e': 5, 'f': 6, 'g': 7, 'h': 8
    }

    def __init__(self, colore, tipo):
        self._colore = colore  # 'bianco' o 'nero'
        self._tipo = tipo      # 'R' = Re, 'D' = Donna, 'A' = Alfiere, 'C' = Cavallo, 'T' = Torre, 'P' = Pedone

    @abstractmethod
    def mossa(self, mossa_na, scacchiera):
        pass

    def Algebrica_a_Matrice(self, posizione):
        if re.match("^[RDTAC]", posizione):
            colonna = self.Conversione.get(posizione[1])
            riga = int(posizione[2])
        else:
            colonna = self.Conversione.get(posizione[0])
            riga = int(posizione[1])
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
    
    def MossaPedone(self, posizione_arrivo, scacchiera):
        # Converte la posizione di arrivo in coordinate della matrice
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(posizione_arrivo)
        # Verifica che la posizione di arrivo sia valida
        if not (0 <= riga_arrivo <= 7 and 0 <= colonna_arrivo <= 7):
            raise ValueError("La posizione di arrivo è fuori dai limiti della scacchiera.")

        # Determina la direzione del movimento in base al colore del pedone
        direzione = 1 if self._colore == 'bianco' else -1

        # Controlla la casella immediatamente prima della posizione di arrivo
        riga_partenza = riga_arrivo - direzione
        if 0 <= riga_partenza <= 7:
            pezzo = scacchiera.get_pezzo_scacchiera(riga_partenza, colonna_arrivo)
            print("preif")
            if isinstance(pezzo, self.__class__) and pezzo._colore == self._colore:
                # Effettua la mossa del pedone
                print("inif")
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo)
                scacchiera.set_pezzo_scacchiera(riga_partenza, colonna_arrivo)  # Libera la posizione di partenza          
                if not pezzo.get_prima_mossa():
                    pezzo.set_prima_mossa()  # Aggiorna lo stato del pedone
                print(f"Mossa effettuata: {pezzo.get_tipo()} da {pezzo.Matrice_a_Algebrica((riga_partenza, colonna_arrivo))} a {posizione_arrivo}")
                Partita.cambiaturno()  # Cambia il turno della partita
            else:
                raise ValueError("Nessun pedone può raggiungere la posizione specificata.")
                
        elif self.get_prima_mossa():
            # Controlla la casella due righe prima della posizione di arrivo (solo per la prima mossa)
            riga_partenza_due = riga_arrivo - 2 * direzione
            if 0 <= riga_partenza_due < 8:
                pezzo = scacchiera[riga_partenza_due][colonna_arrivo]
                if isinstance(pezzo, Pedone) and pezzo._prima_mossa and pezzo._colore == self._colore:
                    # Effettua la mossa del pedone
                    scacchiera[riga_arrivo][colonna_arrivo] = Scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo)
                    scacchiera[riga_partenza_due][colonna_arrivo] = None  # Libera la posizione di partenza
                    pezzo.set_prima_mossa()  # Aggiorna lo stato del pedone
                    print(f"Mossa effettuata: {pezzo.get_tipo()} da {pezzo.Matrice_a_Algebrica((riga_partenza_due, colonna_arrivo))} a {posizione_arrivo}")
                    Partita.cambiaturno()  # Cambia il turno della partita
        else:
            raise ValueError("Nessun pedone può raggiungere la posizione specificata.")
    
    def mossa(self, posizione_arrivo, scacchiera):
        return self.MossaPedone(posizione_arrivo, scacchiera)


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