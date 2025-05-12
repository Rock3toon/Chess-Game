from Entity.Scacchiera import Scacchiera
from Entity.Pezzo import Pedone
import re


def GestioneInput(move_result, scacchiera):
    try:
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
            Pedone.MossaPedone(move_result, scacchiera)
    except ValueError as e:
        print(f"Errore: {e}")