import scacchi.Boundary.errori as errori      
from scacchi.Entity.Pezzo import Pezzo

class Cavallo(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un cavallo degli scacchi."""

    def __init__(self, colore):  # inizializza il cavallo
        super().__init__(colore, "C")
    

    def fattibilità(self, mossa_na, scacchiera, partita):
        righe_arrivo, colonne_arrivo = self.Algebrica_a_Matrice(mossa_na)               #righe e colonne di arrivo
        filtri = scacchiera.filtra('C', partita.get_turno())                            # lista delle istanze dei pezzi sulla scacchiera
        #Controlla tutte le istanze dei cavalli presenti sulla scacchiera
        
        for istanza in filtri:
            righe_partenza = istanza.get_riga()                                         # riga di partenza
            colonne_partenza = istanza.get_colonna()                                    # colonna di partenza
            valida = self.movimento_cavallo(righe_partenza, righe_arrivo, colonne_partenza, colonne_arrivo)  # verifica se il movimento è valido
            if valida is None: #Pezzo che può muoversi trovato
               filtri.remove(istanza)                                                                                                                        
        if len(filtri) == 0:                                                           
            errori.errore_cavallo_mossa_illegale()
            return -1        
        elif len(filtri) == 1:                                                         
            return filtri[0]                                                             # ritorna l'istanza del cavallo (Casa) 
        else:
            disambiguazione = self.riga_colonna_disambiguazione(mossa_na)               # restituisce array con riga e colonna di disambiguazione
            if disambiguazione[0] is not None or disambiguazione[1] is not None:
                for istanza in filtri:
                    if not (istanza.get_riga() == disambiguazione[0] or istanza.get_colonna() == disambiguazione[1]):
                        filtri.remove(istanza)  # rimuove l'istanza se non corrisponde alla disambiguazione                
                if len(filtri) == 1:
                    return filtri[0]
                elif len(filtri) > 1:
                    errori.errore.cavallo_errore_disambiguazione()
                    return -1  
            else:
                # Se non c'è disambiguazione, ma ci sono più cavalli, errore
                errori.errore_cavallo_mossa_ambigua()
                return -1   
                       
    # Metodo che gestisce la mossa del cavallo senza cattura
    def mossa_cavallo(self, mossa_na, scacchiera, partita):
        pass                                  
            
    def cattura(self, mossa_na, scacchiera, partita):
        pass

    # Logica di movimento del cavallo restituisce True se il movimento è valido, altrimenti False
    def movimento_cavallo(self, r_partenza, r_arrivo, c_partenza, c_arrivo):
        if 0 <= r_arrivo < 8 and 0 <= c_arrivo < 8:
            righe = abs(r_partenza - r_arrivo)
            colonne = abs(c_partenza - c_arrivo)
            return (righe, colonne) in [(1, 2), (2, 1)]
        else:
            return False # fuori dalla scacchiera 