import re

"""
Classe di tipo <<Control>> per la gestione e validazione degli input utente.

Responsabilità:
    - Tradurre comandi testuali (/help, /gioca, /patta, ecc.) in codici interni.
    - Validare le mosse nel formato scacchistico (es. e4, Cf3, Dd8).
    - Interpretare conferme sì/no da risposte libere dell’utente.

"""


class parse_input:
    """Classe di tipo <<  Control >>, per la gestione dei comandi di input."""
    
    # Dizionario di tipo string int per la gestione dei comandi
    COMMANDS = { 
        "/help": 1,    
        "/esci": 2,
        "/scacchiera": 3,
        "/gioca": 4,    
        "/abbandona": 5,
        "/patta": 6,
        "/mosse": 7
        }
    def __init__(self):
        pass

    def parseCommand(self, input):
        inputProcessed = input.lower().replace(" ", "")
        if inputProcessed in self.COMMANDS:
            return self.COMMANDS.get(inputProcessed) 
            #ritorna il valore associato alla chiave in COMMANDS
        else:
            return -1
        
    def parseMove(self, input):
        input = input.replace(" ", "")
        if re.match("^[RDTAC]?[a-h][1-8]$", input) or\
            re.match("^[DTAC][a-h][a-h][1-8]$", input) or \
            re.match("^[DTAC][1-8][a-h][1-8]$", input) or input in {"0-0", "0-0-0"} or \
            re.match("^[a-h][18][DTAC]$", input) or\
            re.match("^[a-h][x][a-h][18][DTAC]$", input) or \
            re.match("^[RDTAC][x][a-h][1-8]$", input) or\
            re.match("^[a-h][x][a-h][1-8]$", input) or \
            re.match("^[DTAC][a-h][x][a-h][1-8]$", input) or\
            re.match("^[DTAC][1-8][x][a-h][1-8]$", input):
            return input
        else:
            return -1

    def parseConfirm(self, input):
        if input.lower() in {"s", "si", "y", "ys", "yes"}:
            return "si"
        elif input.lower() in {"n", "no", "nop", "nope"}:
            return "no"
        else:
            return -1   