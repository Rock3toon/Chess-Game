from Casa import Casa


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
        
    
        

    


    


