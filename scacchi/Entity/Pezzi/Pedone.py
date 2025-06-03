from Pezzo import Pezzo

import scacchi.Boundary.errori as errori


class Pedone(Pezzo):
    """Classe di tipo << Entity >> per rappresentare un pedone degli scacchi.
    
    Responsabilità:
      - Inizializzare il pedone con il suo colore e tipo.
      - Gestire la prima mossa del pedone (doppia mossa).
      - Implementare la logica di movimento del pedone, inclusa la cattura.
      - Controllare se la mossa è valida e se il pedone può muoversi in una certa
        posizione.
    """

    def __init__(self, colore):  # inizializza il pedone
        super().__init__(colore, "P")
        self._prima_mossa = True           # indica se il pedone ha fatto la prima mossa

        self._en_passant = False            # indica se il pedone può essere
                                            #catturato in en passant


    def set_en_passant(self, en_passant):
        if not en_passant:
            self._en_passant = True


    def get_en_passant(self):
        return self._en_passant

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

        if not self.out_of_bounds(riga_arrivo + 2*direzione, colonna_arrivo) \
            and not self.out_of_bounds(riga_arrivo + direzione, colonna_arrivo) \
                and scacchiera.get_pezzo_scacchiera(riga_arrivo, colonna_arrivo) \
                    is None:
            # Determina la direzione del movimento in base al colore del pedone

            partenza_singola = \
                scacchiera.get_pezzo_scacchiera(riga_arrivo + direzione, colonna_arrivo)
            partenza_doppia = \
                scacchiera.get_pezzo_scacchiera(riga_arrivo + 2*direzione, \
                                                colonna_arrivo)
            
            if scacchiera.get_casa(riga_arrivo + 2*direzione, colonna_arrivo)\
                .get_pezzo() is not None and scacchiera.get_casa\
                    (riga_arrivo + 2*direzione, colonna_arrivo).get_pezzo()\
                        .get_tipo() == "P" and partenza_doppia.get_prima_mossa():
                if scacchiera.get_casa(riga_arrivo + direzione, colonna_arrivo)\
                    .get_pezzo() is None:
                    scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo,\
                        partenza_doppia) #sposto il pedone con doppia mossa
                    scacchiera.set_pezzo_scacchiera(riga_arrivo + 2*direzione,\
                        colonna_arrivo) #cancello il pedone in partenza
                    if partenza_doppia.get_prima_mossa():
                        partenza_doppia.set_prima_mossa() 
                    partita.aggiungi_mossa(posizione_arrivo) 
                    partita.cambiaturno()  # Cambia il turno dopo la mossa  
                else:
                    errori.errore_mossa_pedone()       
            elif scacchiera.get_casa(riga_arrivo + direzione, colonna_arrivo)\
                .get_pezzo() is not None and scacchiera\
                    .get_casa(riga_arrivo + direzione, colonna_arrivo).get_pezzo()\
                        .get_tipo() == "P":    
                scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, \
                                                partenza_singola)
                #sposto il pedona
                scacchiera.set_pezzo_scacchiera(riga_arrivo + direzione, colonna_arrivo)
                #cancello il pedone in partenza
                if partenza_singola.get_prima_mossa():
                    partenza_singola.set_prima_mossa()
                partita.aggiungi_mossa(posizione_arrivo) 
                partita.cambiaturno()  # Cambia il turno dopo la mossa
            else:   
                errori.errore_mossa_pedone()
        else:   
            errori.errore_mossa_pedone()