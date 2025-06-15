import scacchi.Error.errori as errori
from scacchi.Entity.Pezzo import Pezzo


class Re(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un re degli scacchi."""

    def __init__(self, colore):  # inizializza il re
        self._prima_mossa = True
        # utile per l'arrocco, garantisce che il re non sia stato ancora mosso
        super().__init__(colore, "R")

    def set_prima_mossa(self):
        if self._prima_mossa:
            self._prima_mossa = False

    def get_prima_mossa(self):
        return self._prima_mossa

    def mossa(self, mossa_na, scacchiera, partita):
        riga_destinazione, colonna_destinazione=self.Algebrica_a_Matrice(mossa_na)
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if partenza != -1:
            if not scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                .sotto_scacco(scacchiera, partita):
                if scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                .get_pezzo() is None:
                    partenza.get_pezzo().set_prima_mossa()
                    scacchiera.aggiorna_lista_istanze(partenza, \
                        scacchiera.get_casa(riga_destinazione, colonna_destinazione))
                    scacchiera.set_pezzo_scacchiera\
                    (riga_destinazione, colonna_destinazione, partenza.get_pezzo())
                    scacchiera.set_pezzo_scacchiera(partenza.get_riga(), partenza\
                    .get_colonna(), None)
                    partita.cambiaturno()
                    partita.aggiungi_mossa(mossa_na, scacchiera)
                    self.reset_en_passant(scacchiera, partita)
                elif scacchiera.get_pezzo_scacchiera(riga_destinazione, \
                colonna_destinazione) is not None and scacchiera.get_pezzo_scacchiera\
                (riga_destinazione, colonna_destinazione).get_colore() \
                == partita.get_turno() or scacchiera.get_pezzo_scacchiera\
                (riga_destinazione,colonna_destinazione) is not None \
                and scacchiera.get_pezzo_scacchiera\
                (riga_destinazione, colonna_destinazione).get_colore() \
                != partita.get_turno():
                    errori.errore_re_cattura_non_specificata()
            else:
                errori.errore_re_mossa_sotto_scacco()              
        else: 
            errori.errore_re_mossa_illegale()  


    def fattibilità(self, mossa_na, scacchiera, partita):
        riga_destinazione, colonna_destinazione = self.Algebrica_a_Matrice(mossa_na)
        lista_re = scacchiera.filtra_istanze("R", partita.get_turno())
        re = lista_re[0]
        if abs(re.get_riga() - riga_destinazione) <= 1 and \
         abs(re.get_colonna() - colonna_destinazione) <= 1:
            return re
        else:
            return -1

    
    def cattura(self, mossa_na, scacchiera, partita):
        riga_destinazione,colonna_destinazione=self.Algebrica_a_Matrice(mossa_na)
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if partenza != -1:
            if not scacchiera.simula(partenza, scacchiera.get_casa(riga_destinazione,\
                                                     colonna_destinazione), partita):
                if scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                .get_pezzo() is not None and scacchiera.get_casa(riga_destinazione,\
                colonna_destinazione).get_pezzo().get_colore() != partita.get_turno():
                    partenza.get_pezzo().set_prima_mossa()
                    scacchiera.discard_istanze(partenza)
                    scacchiera.set_pezzo_scacchiera\
                    (riga_destinazione, colonna_destinazione, partenza.get_pezzo())
                    scacchiera.set_pezzo_scacchiera(partenza.get_riga(), partenza\
                    .get_colonna(), None)
                    partita.cambiaturno()
                    partita.aggiungi_mossa(mossa_na, scacchiera)
                    self.reset_en_passant(scacchiera, partita)
                elif scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                .get_pezzo() is not None and scacchiera.\
                get_casa(riga_destinazione, colonna_destinazione)\
                .get_pezzo().get_colore() == partita.get_turno(): 
                        errori.errore_re_mossa_illegale()
                elif scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                    .get_pezzo() is None:
                        errori.errore_re_cattura_casa_vuota()
            else:
                errori.errore_re_mossa_sotto_scacco()
                    
        else: 
            errori.errore_re_mossa_illegale()

    def arrocco(self, mossa_na, scacchiera, partita):
        turno = partita.get_turno()
        re_lista = scacchiera.filtra_istanze("R", turno)
        re = re_lista[0]        
        #prende la riga di riferimento per l'arrocco 0 per il bianco, 7 per il nero
        riga = 0 if turno == 1 else 7
        #controlla se il re non è sotto scacco e se non ha ancora mosso
        if  re.get_pezzo().get_prima_mossa() and \
             not re.sotto_scacco(scacchiera, partita):
            if mossa_na == "0-0": #arrocco corto
                torre = scacchiera.get_casa(riga, 7)
                if (torre.get_pezzo() is not None and
                     torre.get_pezzo().get_tipo() == "T"):
                    re_arrivo = scacchiera.get_casa(riga, 6)
                    torre_arrivo = scacchiera.get_casa(riga, 5)
                    #controlla se la torre non è stata mossa
                    if torre.get_pezzo().get_prima_mossa():
                        #controlla se le case sono vuote
                        if scacchiera.get_casa(riga, 5).get_pezzo() is None and \
                         scacchiera.get_casa(riga, 6).get_pezzo() is None:     
                            #controlla se le case non sono sotto scacco
                            if not scacchiera.get_casa(riga, 5).\
                             sotto_scacco(scacchiera, partita) and \
                              not scacchiera.get_casa(riga, 6).\
                               sotto_scacco(scacchiera, partita):
                                # esegue l'arrocco corto
                                # Sposta il Re
                                scacchiera.set_pezzo_scacchiera(riga, 6, re.get_pezzo())
                                scacchiera.aggiorna_lista_istanze(re, re_arrivo)
                                re.get_pezzo().set_prima_mossa()
                                scacchiera.set_pezzo_scacchiera(riga, 4, None)
                                # Sposta la Torre
                                scacchiera.\
                                    set_pezzo_scacchiera(riga, 5, torre.get_pezzo())
                                scacchiera.aggiorna_lista_istanze(torre, torre_arrivo)
                                torre.get_pezzo().set_prima_mossa()
                                scacchiera.set_pezzo_scacchiera(riga, 7, None)
                                partita.aggiungi_mossa(mossa_na, scacchiera)
                                partita.cambiaturno()
                            else:
                                errori.errore_arrocco_attacco()
                        else:
                            errori.errore_arrocco_illegale()
                    else:
                        errori.errore_arrocco_illegale()
            elif mossa_na == "0-0-0": #arrocco lungo
                torre = scacchiera.get_casa(riga, 0)
                if (torre.get_pezzo() is not None and
                     torre.get_pezzo().get_tipo() == "T"):
                    re_arrivo = scacchiera.get_casa(riga, 2)
                    torre_arrivo = scacchiera.get_casa(riga, 3)
                    #controlla se la torre non è stata mossa
                    if torre.get_pezzo().get_prima_mossa():
                        #controlla se le case sono vuote
                        if scacchiera.get_casa(riga, 3).get_pezzo() is None and \
                         scacchiera.get_casa(riga, 2).get_pezzo() is None and \
                          scacchiera.get_casa(riga, 1).get_pezzo() is None:
                            #controlla se le case non sono sotto scacco
                            if not scacchiera.get_casa(riga, 3).\
                             sotto_scacco(scacchiera, partita) and \
                              not scacchiera.get_casa(riga, 2).\
                                sotto_scacco(scacchiera, partita):
                                # esegue l'arrocco lungo
                                # Sposta il Re
                                scacchiera.set_pezzo_scacchiera(riga, 2, re.get_pezzo())
                                scacchiera.aggiorna_lista_istanze(re, re_arrivo)  
                                re.get_pezzo().set_prima_mossa()
                                scacchiera.set_pezzo_scacchiera(riga, 4, None)
                                # Sposta la Torre
                                scacchiera.\
                                    set_pezzo_scacchiera(riga, 3, torre.get_pezzo())
                                scacchiera.aggiorna_lista_istanze(torre, torre_arrivo)
                                torre.get_pezzo().set_prima_mossa()
                                scacchiera.set_pezzo_scacchiera(riga, 0, None)
                                partita.aggiungi_mossa(mossa_na, scacchiera)
                                partita.cambiaturno()
                            else:
                                errori.errore_arrocco_attacco()
                        else:
                            errori.errore_arrocco_illegale()
                    else:
                        errori.errore_arrocco_illegale()
        else:
            errori.errore_arrocco_illegale()
