import re

from scacchi.Entity.Pezzo import Pedone
from scacchi.Entity.Partita import Partita

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
        colore = 'bianco'
    elif turno_partenza == 1:
        colore = 'nero'
    
    pedone = Pedone(colore)

    if partita.get_stato_partita() == 1:
        print("Nessuna partita in corso." \
            " Scrivi /gioca per avviare una partita.")
    else:
        if re.match("^R", move_result):
            print("Gestione mossa Re non ancora implementata")
            # Inserire gestore mossa Re
        elif re.match("^0", move_result):
            print("Gestione arrocco non ancora implementata")
            # Inserire gestore arrocco
        elif re.match("^D", move_result):
            print("Gestione mossa Donna non ancora implementata")
            # Inserire gestore mossa Donna
        elif re.match("^C", move_result):
            print("Gestione mossa Cavallo non ancora implementata")
            # Inserire gestore mossa Cavallo
        elif re.match("^A", move_result):
            print("Gestione mossa Alfiere non ancora implementata")
            # Inserire gestore mossa Alfiere
        elif re.match("^T", move_result):
            print("Gestione mossa Torre non ancora implementata")
            # Inserire gestore mossa Torre
        elif "=" in move_result:
            print("Gestione promozione pedone non ancora implementata")
            # Inserire gestore promozione pedone
        else:
            pedone.mossa(move_result, scacchiera, partita)

        if partita.get_turno() != turno_partenza:
            scacchiera.stampa_scacchiera(scacchiera)
