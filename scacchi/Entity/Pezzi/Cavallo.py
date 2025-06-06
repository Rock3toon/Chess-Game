import scacchi.Boundary.errori as errori      
from scacchi.Entity.Pezzo import Pezzo

class Cavallo(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un cavallo degli scacchi."""

    def __init__(self, colore):  # inizializza il cavallo
        super().__init__(colore, "C")
    

    def fattibilità(self, mossa_na, scacchiera, partita):
        righe_arrivo, colonne_arrivo = self.Algebrica_a_Matrice(mossa_na)               #righe e colonne di arrivo
        print(f"CAVALLOrighe_arrivo: {righe_arrivo}, colonne_arrivo: {colonne_arrivo}")
        filtri = scacchiera.filtra_istanze('C', partita.get_turno())                            # lista delle istanze dei pezzi sulla scacchiera
        #Controlla tutte le istanze dei cavalli presenti sulla scacchiera
        lista = []
        i = 0
        for istanza in filtri:
            righe_partenza = istanza.get_riga()                                         # riga di partenza
            colonne_partenza = istanza.get_colonna()                                    # colonna di partenza
            valida = self.movimento_cavallo(righe_partenza, righe_arrivo, colonne_partenza, colonne_arrivo)  # verifica se il movimento è valido
            if valida: #Pezzo che può muoversi trovato
               lista.append(istanza) 
            i += 1     
            print (i)                                                                                                                  
        if len(lista) == 0:                                                           
            errori.errore_cavallo_mossa_illegale()
            return -1        
        elif len(lista) == 1:                                                         
            return lista[0]                                                             # ritorna l'istanza del cavallo (Casa) 
        elif len(lista) > 1:
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
    def mossa(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)
        arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)             # recupera la casa di arrivo
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        print(f"arrivo: {arrivo.get_pezzo()}")
        if  partenza != -1:               # se la mossa è valida              
            if arrivo.get_pezzo() is None:
                pezzo = partenza.get_pezzo()
                scacchiera.aggiorna_lista_istanze(partenza, arrivo)
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo)  # aggiorna la scacchiera
                scacchiera.set_pezzo_scacchiera(partenza.get_riga(), partenza.get_colonna(), None)  # rimuove il pezzo dalla casa di partenza  
                partita.aggiungi_mossa(mossa_na)                    
                partita.cambiaturno()                                          
                                               
            
    def cattura(self, mossa_na, scacchiera, partita):
        pass

    # Logica di movimento del cavallo restituisce True se il movimento è valido, altrimenti False
    def movimento_cavallo(self, r_partenza, r_arrivo, c_partenza, c_arrivo):
        if 0 <= r_arrivo < 7 and 0 <= c_arrivo < 7:
            righe = abs(r_partenza - r_arrivo)
            colonne = abs(c_partenza - c_arrivo)
            print(f"righe: {righe}, colonne: {colonne}")
            if (righe == 2 and colonne == 1) or (righe == 1 and colonne == 2):
                return True
            else:
                print("illegale")
                return False # fuori dalla scacchiera 
        else:
            print("fuori dalla scacchiera")
            return False