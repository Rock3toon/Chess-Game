import re


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
        if re.match("^[RDTAC]?[a-h][1-8]$", input):
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