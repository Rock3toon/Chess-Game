import re

import scacchi.Boundary.errori as errori
from scacchi.Entity.Pezzi.Alfiere import Alfiere
from scacchi.Entity.Pezzi.Cavallo import Cavallo
from scacchi.Entity.Pezzi.Donna import Donna
from scacchi.Entity.Pezzi.Pedone import Pedone
from scacchi.Entity.Pezzi.Re import Re
from scacchi.Entity.Pezzi.Torre import Torre

"""
Modulo di tipo << Control >> per gestire l’input di una mossa.

Responsabilità:
    - Determinare il colore del giocatore di turno.
    - Smistare la mossa al gestore del pezzo corretto (Re, Donna, Cavallo, Alfiere, \
        Torre o Pedone).
    - Aggiornare lo stato della partita e della scacchiera.
    - Ripristinare la stampa della scacchiera se il turno è passato all’avversario.
"""


def GestioneInput(move_result, scacchiera, partita):
    """Gestisce l'input dell'utente e smista la mossa al gestore del pezzo corretto."""
    turno_partenza = partita.get_turno()

    if turno_partenza == 0:
        colore = 0
    elif turno_partenza == 1:
        colore = 1
    
    pedone = Pedone(colore)
    alfiere = Alfiere(colore)
    cavallo = Cavallo(colore)
    torre = Torre(colore)
    king = Re(colore)

    donna = Donna(colore)

    if partita.get_stato_partita() == 1:
        errori.errore_nessuna_partita()
    else:
        if re.match("^R", move_result):
            if "x" in move_result:
                king.cattura(move_result, scacchiera, partita)
            else:
                king.mossa(move_result, scacchiera, partita)
        elif re.match("^0", move_result):
            king.arrocco(move_result, scacchiera, partita)
        elif re.match("^D", move_result):
            if "x" in move_result:
                donna.cattura(move_result, scacchiera, partita)  
            else:
                donna.mossa(move_result, scacchiera, partita)  
        elif re.match("^C", move_result):
            if "x" in move_result:
                cavallo.cattura(move_result, scacchiera, partita)  
            else:
                cavallo.mossa(move_result, scacchiera, partita)  
        elif re.match("^A", move_result):
            if "x" in move_result:
                alfiere.cattura(move_result, scacchiera, partita)
            else:
                alfiere.mossa(move_result, scacchiera, partita) 
        elif re.match("^T", move_result):
            if "x" in move_result:
                torre.cattura(move_result, scacchiera, partita)  
            else:
                torre.mossa(move_result, scacchiera, partita)  

        elif re.match("^[a-h][18][DTAC]$" , move_result) or\
             re.match("^[a-h][x][a-h][18][DTAC]$", move_result):
                pedone.promozione_pedone(move_result, scacchiera, partita)

        else:
            if "x" in move_result:
                pedone.cattura(move_result, scacchiera, partita)
            else:
                pedone.mossa(move_result, scacchiera, partita)

        if partita.get_turno() != turno_partenza:
            scacchiera.stampa_scacchiera(scacchiera)
            if partita.scacco_matto(scacchiera) or partita.stallo(scacchiera):
                partita.azzera_mosse()
                scacchiera.azzera_istanze()
                partita.set_turno()                                      
                partita.cambia_stato_partita()
