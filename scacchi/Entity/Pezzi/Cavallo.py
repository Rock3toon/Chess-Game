import scacchi.Boundary.errori as errori
from scacchi.Entity.Pezzo import Pezzo


class Cavallo(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un cavallo degli scacchi."""

    def __init__(self, colore):  # inizializza il cavallo
        super().__init__(colore, "C")
    

    def fattibilità(self, mossa_na, scacchiera, partita):
        righe_arrivo, colonne_arrivo = self.Algebrica_a_Matrice(mossa_na)
        # lista delle istanze dei pezzi sulla scacchiera   
        filtri = scacchiera.filtra_istanze('C', partita.get_turno())      
        #Controlla tutte le istanze dei cavalli presenti sulla scacchiera
        lista = []
        arrivo = scacchiera.get_casa(righe_arrivo, colonne_arrivo)             
        for istanza in filtri:
            righe_partenza = istanza.get_riga()                                
            colonne_partenza = istanza.get_colonna()
            # verifica se il movimento è valido                                  
            valida = self.movimento_cavallo(righe_partenza, righe_arrivo, \
                                            colonne_partenza, colonne_arrivo)
            if valida == 1: #Pezzo che può muoversi trovato
                lista.append(istanza) 
        if len(lista) == 0:                                                           
            errori.errore_cavallo_mossa_illegale()
            return -1   
             
        elif len(lista) == 1: 
            if not scacchiera.simula\
                (scacchiera.get_casa(righe_partenza, colonne_partenza), \
                scacchiera.get_casa(righe_arrivo, colonne_arrivo), partita):
                return lista[0]
            elif scacchiera.simula\
                (scacchiera.get_casa(righe_partenza, colonne_partenza), \
                scacchiera.get_casa(righe_arrivo, colonne_arrivo), partita):
                errori.errore_cavallo_mossa_illegale_simulazione()
                return -1  

        elif len(lista) > 1:
            # restituisce array con riga e colonna di disambiguazione
            disambiguazione = self.riga_colonna_disambiguazione(mossa_na)
            if disambiguazione[0] is not None or disambiguazione[1] is not None:
                lista_disambiguazione = []
                for istanza in lista:
                    if ((disambiguazione[0] is not None and istanza.get_riga() == \
                         disambiguazione[0]) \
                        or (disambiguazione[1] is not None and istanza.get_colonna() ==\
                            disambiguazione[1])):
                   
                        lista_disambiguazione.append(istanza)                 
                if len(lista_disambiguazione) == 1:
                    if not scacchiera.simula\
                    (scacchiera.get_casa(righe_partenza, colonne_partenza), \
                    scacchiera.get_casa(righe_arrivo, colonne_arrivo), partita):
                        return lista_disambiguazione[0]
                    elif scacchiera.simula\
                    (scacchiera.get_casa(righe_partenza, colonne_partenza), \
                    scacchiera.get_casa(righe_arrivo, colonne_arrivo), partita):
                        errori.errore_cavallo_mossa_illegale_simulazione()
                        return -1
                elif len(lista_disambiguazione) > 1:
                    errori.errore_cavallo_errore_disambiguazione()
                    return -1  
            else:
                if arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore()\
                      == partita.get_turno():
                # Se non c'è disambiguazione, ma ci sono più cavalli, errore
                    errori.errore_cavallo_mossa_illegale()
                else:    
                    errori.errore_cavallo_mossa_ambigua()
                return -1   
                       
    # Metodo che gestisce la mossa del cavallo senza cattura
    def mossa(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)
        arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if  partenza != -1:               # se la mossa è valida 
            pezzo = partenza.get_pezzo()             
            if arrivo.get_pezzo() is None:
                scacchiera.aggiorna_lista_istanze(partenza, arrivo)
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo) 
                scacchiera.set_pezzo_scacchiera(partenza.get_riga(),\
                                                 partenza.get_colonna(), None)
                partita.cambiaturno()
                partita.aggiungi_mossa(mossa_na, scacchiera)                    
                self.reset_en_passant(scacchiera, partita)
            elif arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore() ==\
                  pezzo.get_colore():
                errori.errore_cavallo_mossa_illegale()
                
            elif arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore() !=\
                  pezzo.get_colore():
                errori.errore_cavallo_cattura_non_specificata()
                                                
            
    def cattura(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)
        arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if  partenza != -1:               # se la mossa è valida 
            pezzo = partenza.get_pezzo()             
            if arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore()\
                    != pezzo.get_colore():
                scacchiera.discard_istanze(partenza)
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo)
                scacchiera.set_pezzo_scacchiera(partenza.get_riga(),
                                                partenza.get_colonna(), None)
                partita.cambiaturno()
                partita.aggiungi_mossa(mossa_na, scacchiera)                    
                self.reset_en_passant(scacchiera, partita)        
            elif arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore() ==\
                  pezzo.get_colore():
                # Se il pezzo nella casa di arrivo è dello stesso colore, errore
                errori.errore_cavallo_mossa_illegale()
            elif arrivo.get_pezzo() is None:
                errori.errore_cavallo_cattura_vuota()

# Logica di movimento del cavallo restituisce 1 se è valido, altrimenti False
    def movimento_cavallo(self, r_partenza, r_arrivo, c_partenza, c_arrivo):
        if 0 <= r_arrivo < 8 and 0 <= c_arrivo < 8:
            righe = abs(r_partenza - r_arrivo)
            colonne = abs(c_partenza - c_arrivo)
            if (righe == 2 and colonne == 1) or\
                 (righe == 1 and colonne == 2):
                return 1
            else:
                return False
        else:
            return False