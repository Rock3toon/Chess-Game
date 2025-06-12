import scacchi.Boundary.errori as errori
from scacchi.Entity.Pezzo import Pezzo


class Torre(Pezzo):
    """Classe di tipo << Entity >> per rappresentare una torre degli scacchi."""

    def __init__(self, colore):  # inizializza la torre
        self._prima_mossa = True 
        #utile per l' arrocco, garantisce che la torre non sia stata ancora mossa
        super().__init__(colore, "T")
        
    def set_prima_mossa(self):
        self._prima_mossa = False

    def get_prima_mossa(self):
        return self._prima_mossa
    
    def movimento_Torre(self, r_partenza, r_arrivo, c_partenza, c_arrivo, scacchiera):
        if c_partenza == c_arrivo:
            direzione = 1 if r_arrivo > r_partenza else -1
            for j in range(r_partenza + direzione, r_arrivo, direzione):
                casa = scacchiera.get_casa(j, c_partenza).get_pezzo()
                if casa is not None:
                    return  0
            return 1
        elif r_partenza == r_arrivo:
            direzione = 1 if c_arrivo > c_partenza else -1
            for k in range(c_partenza + direzione, c_arrivo, direzione):
                casa = scacchiera.get_casa(r_partenza, k).get_pezzo()
                if casa is not None:
                    return 0
            return 1
        return 0
    

    def fattibilità(self, mossa_na, scacchiera, partita):
        lista_filtrata = scacchiera.filtra_istanze('T', partita.get_turno())
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)
        lista = []
        for istanza in lista_filtrata:
            righe_partenza = istanza.get_riga()                                
            colonne_partenza = istanza.get_colonna()
            # verifica se il movimento è valido                                  
            valida = self.movimento_Torre(righe_partenza, riga_arrivo,colonne_partenza,\
                                        colonna_arrivo, scacchiera)
            if valida == 1: #Pezzo che può muoversi trovato
                lista.append(istanza) 
        
        if len(lista) == 0:
            errori.errore_torre_mossa_illegale()
            return -1
        
        elif len(lista) == 1:
            return lista[0]
                        
        elif len(lista) > 1:
            # Estrai la disambiguazione [riga, colonna]
            disamb = self.riga_colonna_disambiguazione(mossa_na)
        
            
            if disamb[0] is not None or disamb[1] is not None:
                lista_disambiguazione = []
                for istanza in lista:
                    r = istanza.get_riga()
                    c = istanza.get_colonna()
                    if ((disamb[0] is not None and r == disamb[0]) or\
                        (disamb[1] is not None and c == disamb[1])):
                       lista_disambiguazione.append(istanza)
                    
                if len(lista_disambiguazione) == 1:
                    return lista_disambiguazione[0]
                elif len(lista_disambiguazione) > 1 or len(lista_disambiguazione) == 0:
                    errori.errore_torre_errore_disambiguazione()
                    return -1
                else:   
                    errori.errore_torre_mossa_ambigua()
                    return -1  
    
    def mossa(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)
        arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
        casa_partenza = self.fattibilità(mossa_na, scacchiera, partita)

        if  casa_partenza != -1:               # se la mossa è valida 
            pezzo = casa_partenza.get_pezzo()             
            if arrivo.get_pezzo() is None:
                scacchiera.aggiorna_lista_istanze(casa_partenza, arrivo)
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo) 
                scacchiera.set_pezzo_scacchiera(casa_partenza.get_riga(),\
                                                 casa_partenza.get_colonna(), None)
                partita.cambiaturno()
                partita.aggiungi_mossa(mossa_na, scacchiera)                    
                self.reset_en_passant(scacchiera, partita)
            elif arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore() ==\
                  pezzo.get_colore():
                errori.errore_torre_mossa_illegale()

            elif arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore() !=\
                  pezzo.get_colore():
                errori.errore_torre_cattura_non_specificata()


    def cattura(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)
        arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
        casa_partenza = self.fattibilità(mossa_na, scacchiera, partita)

        if casa_partenza != -1:              # se la mossa è valida
            pezzo = casa_partenza.get_pezzo()
            if arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore()\
                    != pezzo.get_colore():
                scacchiera.discard_istanze(arrivo)
                scacchiera.aggiorna_lista_istanze(casa_partenza, arrivo)
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pezzo)
                scacchiera.set_pezzo_scacchiera(casa_partenza.get_riga(),\
                    casa_partenza.get_colonna(), None)
                partita.cambiaturno()
                partita.aggiungi_mossa(mossa_na, scacchiera)                    
                self.reset_en_passant(scacchiera, partita)        
            elif arrivo.get_pezzo() is not None and arrivo.get_pezzo().get_colore() ==\
                pezzo.get_colore():
            # Se il pezzo nella casa di arrivo è dello stesso colore, errore
                errori.errore_torre_mossa_illegale()
            elif arrivo.get_pezzo() is None:
                errori.errore_torre_cattura_vuota()