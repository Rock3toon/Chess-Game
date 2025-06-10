from scacchi.Entity.Pezzo import Pezzo


class Re(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un re degli scacchi."""

    def __init__(self, colore):  # inizializza il re
        self._prima_mossa = True
        # utile per l'arrocco, garantisce che il re non sia stato ancora mosso
        super().__init__(colore, "R")

    def set_prima_mossa(self, prima_mossa):
        if prima_mossa:
            self._prima_mossa = False

    def get_prima_mossa(self):
        return self._prima_mossa

    def mossa(self, mossa_na, scacchiera, partita):
        riga_destinazione,colonna_destinazione=self.Algebrica_a_Matrice(mossa_na)
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if partenza != -1:
            if not scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                .sotto_scacco(scacchiera, partita):
                if scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                    .get_pezzo() is None:
                    scacchiera.aggiorna_lista_istanze(partenza,scacchiera\
                    .get_casa(riga_destinazione, colonna_destinazione))
                    scacchiera.set_pezzo_scacchiera\
                    (riga_destinazione, colonna_destinazione, partenza.get_pezzo())
                    scacchiera.set_pezzo_scacchiera(partenza.get_riga(), partenza\
                    .get_colonna(), None)
                    partita.aggiungi_mossa(mossa_na)
                    partita.cambiaturno()
            else:
                print("Mossa non valida: il re non può \
                muoversi in una casa sotto scacco.")
                    
        else: 
            print("Mossa illegale.")  


    def fattibilità(self, mossa_na, scacchiera, partita):
        riga_destinazione,colonna_destinazione=self.Algebrica_a_Matrice(mossa_na)
        lista_re=scacchiera.filtra_istanze("R",partita.get_turno)
        for re in lista_re:
            if abs(re.get_riga() - riga_destinazione) <= 1 and \
                abs(re.get_colonna() - colonna_destinazione) <= 1:
                return re
            else:
                return -1

    
    def cattura(self, mossa_na, scacchiera, partita):
        riga_destinazione,colonna_destinazione=self.Algebrica_a_Matrice(mossa_na)
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if partenza != -1:
            if not scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                .sotto_scacco(scacchiera, partita):
                if scacchiera.get_casa(riga_destinazione, colonna_destinazione)\
                    .get_pezzo() is not None:
                    scacchiera.discard_istanze(partenza)
                    scacchiera.set_pezzo_scacchiera\
                    (riga_destinazione, colonna_destinazione, partenza.get_pezzo())
                    scacchiera.set_pezzo_scacchiera(partenza.get_riga(), partenza\
                    .get_colonna(), None)

                    partita.aggiungi_mossa(mossa_na)
                    partita.cambiaturno()
                else:  
                    print("Errore, il Re non può catturare in una \
                    casa vuota.\nDigita /help per altre informazioni.")
            else:
                print("Mossa non valida: il re non può \
                muoversi in una casa sotto scacco.")
                    
        else: 
            print("Mossa illegale.")