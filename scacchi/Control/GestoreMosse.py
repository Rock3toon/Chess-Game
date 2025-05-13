from scacchi.Entity.Scacchiera import Scacchiera
from scacchi.Entity.Pezzo import Pedone
from scacchi.Entity.Partita import Partita
import re


def GestioneInput(move_result, scacchiera, partita):
    
    turno_partenza = partita.get_turno()

    if turno_partenza == 0:
        colore = 'bianco'
    elif turno_partenza == 1:
        colore = 'nero'
    
    pedone = Pedone(colore)

    if re.match("^R", move_result):
        pass # Inserire gestore mossa Re
    elif re.match("^D", move_result):
        pass # Inserire gestore mossa Donna
    elif re.match("^C", move_result):
        pass # Inserire gestore mossa Cavallo
    elif re.match("^A", move_result):
        pass # Inserire gestore mossa Alfiere
    elif re.match("^T", move_result):
        pass # Inserire gestore mossa Torre
    else:
        pedone.mossa(move_result, scacchiera, partita)

    if partita.get_turno() != turno_partenza:
        scacchiera.stampa_scacchiera(scacchiera)