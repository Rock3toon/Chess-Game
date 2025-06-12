import scacchi.Boundary.errori as errori
from scacchi.Entity.Pezzi.Alfiere import Alfiere
from scacchi.Entity.Pezzi.Cavallo import Cavallo
from scacchi.Entity.Pezzi.Donna import Donna
from scacchi.Entity.Pezzi.Torre import Torre
from scacchi.Entity.Pezzo import Pezzo


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
        self._prima_mossa = True  # indica se il pedone ha fatto la prima mossa

        self._en_passant = False  # indica se il pedone può essere
        # catturato in en passant

    def set_en_passant(self):
        if not self._en_passant:
            self._en_passant = True

    def get_en_passant(self):
        return self._en_passant

    def set_prima_mossa(self):
        self._prima_mossa = False

    def get_prima_mossa(self):
        return self._prima_mossa

    def out_of_bounds(self, riga, colonna):
        return riga < 0 or riga >= 8 or colonna < 0 or colonna >= 8
    
    def reset_en_passant(self, scacchiera, partita):
        for pedone in scacchiera.filtra_istanze("P", partita.get_turno()):
            pedone.get_pezzo()._en_passant = False

    def promozione_pedone(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice_promozione(mossa_na)
        casa_arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
        mossa = mossa_na[:-1]
        casa_partenza = self.fattibilità(mossa, scacchiera, partita)
        if casa_partenza != -1:
            # Controlla l' ultima riga per la promozione
            if (partita.get_turno() == 0 and riga_arrivo != 0) or \
            (partita.get_turno() == 1 and riga_arrivo != 7):
                errori.errore_promozione_non_valida()
                return
            # Controlla il colore del pezzo nuovo
            colore = 0 if partita.get_turno() == 0 else 1
            if mossa_na[-1] == "D":
                nuovo_pezzo = Donna(colore)
            elif mossa_na[-1] == "T":
                nuovo_pezzo = Torre(colore)
            elif mossa_na[-1] == "A":
                nuovo_pezzo = Alfiere(colore)
            elif mossa_na[-1] == "C":
                nuovo_pezzo = Cavallo(colore)
            else:
                errori.errore_promozione_non_valida()
                return
            # Aggiorna le istanze
            scacchiera.discard_istanze(casa_partenza)
            casa_arrivo.set_pezzo(nuovo_pezzo)
            casa_partenza.set_pezzo(None)
            # Aggiunge la mossa alla lista delle mosse e cambia il turno
            partita.aggiungi_mossa(mossa_na)
            partita.cambiaturno()
        else:
            errori.errore_promozione_non_valida()

    def fattibilità(self, mossa_na, scacchiera, partita):
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)

        direzione = -1 if partita.get_turno() == 0 else 1

        posizioni_candidate = scacchiera.filtra_istanze("P", partita.get_turno())

        if "x" not in mossa_na:
            # Mossa semplice (non cattura)
            for pedone in posizioni_candidate:
                riga_pedone = pedone.get_riga()
                colonna_pedone = pedone.get_colonna()
                # Mossa singola
                if (riga_arrivo == riga_pedone + direzione and \
                    colonna_arrivo == colonna_pedone and \
                    scacchiera.get_pezzo_scacchiera(riga_arrivo, colonna_arrivo) \
                    is None):
                    return scacchiera.get_casa(riga_pedone, colonna_pedone)
                # Doppia mossa dalla posizione iniziale
                if (pedone.get_pezzo().get_prima_mossa() and \
                    riga_arrivo == riga_pedone + 2 * direzione and \
                    colonna_arrivo == colonna_pedone and \
                    scacchiera.get_pezzo_scacchiera \
                    (riga_pedone + direzione, colonna_pedone) is None and \
                    scacchiera.get_pezzo_scacchiera(riga_arrivo, colonna_arrivo) \
                    is None):
                    return scacchiera.get_casa(riga_pedone, colonna_pedone)

        elif "x" in mossa_na:
            # Cattura (normale o en passant)
            temp = self.riga_colonna_disambiguazione(mossa_na)
            colonna_partenza_cattura = temp[1]

            for pedone in posizioni_candidate:
                riga_pedone = pedone.get_riga()
                colonna_pedone = pedone.get_colonna()
                if (
                    riga_arrivo == riga_pedone + direzione and \
                    (colonna_arrivo == colonna_pedone - 1 or \
                    colonna_arrivo == colonna_pedone + 1) and \
                    (colonna_partenza_cattura is None or \
                    colonna_pedone == colonna_partenza_cattura)):
                    return scacchiera.get_casa(riga_pedone, colonna_pedone)

        return -1

    def mossa(self, mossa_na, scacchiera, partita):
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if partenza != -1:
            riga_partenza = partenza.get_riga()
            colonna_partenza = partenza.get_colonna()
            riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)

            pedone = partenza.get_pezzo()

            # Controlla che il pedone sia sull'ultima riga
            if (partita.get_turno() == 0 and riga_arrivo == 0) or \
               (partita.get_turno() == 1 and riga_arrivo == 7):
                errori.errore_pedone_mancata_promozione()
                return
            # Spostamento del pedone
            scacchiera.set_pezzo_scacchiera(riga_arrivo, colonna_arrivo, pedone)
            scacchiera.set_pezzo_scacchiera(riga_partenza, colonna_partenza, None)

            # Aggiorna la lista delle istanze
            scacchiera.aggiorna_lista_istanze \
                (partenza, scacchiera.get_casa(riga_arrivo, colonna_arrivo))
            # Aggiunge la mossa alla lista delle mosse e cambia il turno
            partita.aggiungi_mossa(mossa_na)
            partita.cambiaturno()
            # Reset di en passant in base al turno
            self.reset_en_passant(scacchiera, partita)

            pedone.set_prima_mossa()
            if abs(riga_arrivo - partenza.get_riga()) == 2:
                pedone.set_en_passant()
        else:
            errori.errore_mossa_pedone()

    def cattura(self, mossa_na, scacchiera, partita):
        partenza = self.fattibilità(mossa_na, scacchiera, partita)
        if partenza == -1:
            errori.errore_cattura_non_valida()
            return

        riga_partenza = partenza.get_riga()
        colonna_partenza = partenza.get_colonna()
        riga_arrivo, colonna_arrivo = self.Algebrica_a_Matrice(mossa_na)

        casa_arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
        pezzo_arrivo = casa_arrivo.get_pezzo()
        pedone = partenza.get_pezzo()

        # Cattura normale
        if (pezzo_arrivo is not None and \
            pezzo_arrivo.get_colore() != partita.get_turno()):
            # Controlla che il pedone sia sull'ultima riga
            if (partita.get_turno() == 0 and riga_arrivo == 0) or \
               (partita.get_turno() == 1 and riga_arrivo == 7):
                errori.errore_pedone_mancata_promozione()
                return
            # Rimossa istanza della casa di partenza
            scacchiera.discard_istanze(partenza)
            # Sposta il pedone (cattura)
            casa_arrivo.set_pezzo(pedone)
            scacchiera.set_pezzo_scacchiera(riga_partenza, colonna_partenza, None)
            # Aggiunge la mossa alla lista delle mosse e cambia il turno
            partita.aggiungi_mossa(mossa_na)
            partita.cambiaturno()
            # Reset di en passant in base al turno
            self.reset_en_passant(scacchiera, partita)
            return

        # Cattura en passant
        riga_enpassant = 3 if partita.get_turno() == 0 else 4

        casa_pedone_catturato = scacchiera.get_casa(riga_enpassant, colonna_arrivo)
        pedone_catturato = casa_pedone_catturato.get_pezzo()

        if (pezzo_arrivo is None
            and pedone_catturato is not None
            and pedone_catturato.get_tipo() == "P"
            and pedone_catturato.get_colore() != partita.get_turno()
            and pedone_catturato.get_en_passant()):   
            # Sposta il pedone (cattura)
            casa_arrivo.set_pezzo(pedone)
            scacchiera.set_pezzo_scacchiera(riga_partenza, colonna_partenza, None)
            # Aggiorna le istanze
            scacchiera.discard_istanze(casa_pedone_catturato)
            # Rimuovi il pedone catturato
            casa_pedone_catturato.set_pezzo(None)
            # Aggiorna le istanze
            scacchiera.aggiorna_lista_istanze(partenza, casa_arrivo)
            partita.cambiaturno()
            self.reset_en_passant(scacchiera, partita)
            partita.aggiungi_mossa(mossa_na + " e.p.")
            return

        if casa_arrivo is None:
            errori.errore_cattura_vuota()
        else:
            errori.errore_cattura_non_valida()