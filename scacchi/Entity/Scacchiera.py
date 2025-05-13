from Entity.Casa import Casa

BIANCO = "\033[48;5;15m"  # Sfondo BIANCO
BEIGE = "\033[48;5;180m"    # Sfondo beige
RESET = "\033[0m"           # Reset colori


class Scacchiera:
    """Classe di tipo <<  Entity >>, per la gestione della matrice che rappresenta la scacchiera."""
    
    def __init__(self):
        self.__matrice = []  
        for riga in range(8):                                               # inizializza la matrice 8x8
            riga_corrente = []  
            for colonna in range(8):
                casa = Casa(riga, colonna)  
                riga_corrente.append(casa)     
            self.__matrice.append(riga_corrente)

    def get_matrice(self):
        return self.__matrice

    def get_casa(self, riga, colonna):                                      # metodo per recuperare una casa dati indici di riga e colonna
        return self.__matrice[riga][colonna]
    
    def set_pezzo_scacchiera(self, riga, colonna, pezzo=None):
        self.__matrice[riga][colonna].set_pezzo(pezzo)

    def get_pezzo_scacchiera(self, riga, colonna):                          # metodo per recuperare il pezzo che occupa una determinata casa
        return self.__matrice[riga][colonna].get_pezzo()
    
    def set_casa(self, riga, colonna, pezzo):                               # metodo che chiama il costruttore di casa 
        self.__matrice[riga][colonna] = Casa(riga, colonna, pezzo)

    def converti_pezzo_unicode(self,pezzo):
        simboli = {
            'P': ("♙", "♟"),
            'T': ("♖", "♜"),
            'C': ("♘", "♞"),
            'A': ("♗", "♝"),
            'D': ("♕", "♛"),
            'R': ("♔", "♚")
        }
        tipo = pezzo.get_tipo()
        colore = pezzo.get_colore()
        return simboli[tipo][0] if colore == 0 else simboli[tipo][1]
        
    def stampa_scacchiera(self, scacchi):
        lettere_colonne = "a  b  c  d  e  f  g  h"
        print("   " + lettere_colonne)

        for i in range(8):
            numero_riga = 8 - i
            riga_str = f"{numero_riga} "
            for j in range(8):
                casa = scacchi.get_casa(i, j)
                pezzo = casa.get_pezzo()
                sfondo = BIANCO if (i + j) % 2 == 0 else BEIGE

                if isinstance(pezzo, str):
                    simbolo = pezzo
                elif pezzo:
                    simbolo = scacchi.converti_pezzo_unicode(pezzo)
                else:
                    simbolo = " "

                riga_str += f"{sfondo} {simbolo} {RESET}"
            print(riga_str + f" {numero_riga}")

        print("   " + lettere_colonne)
            
