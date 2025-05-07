import re


class ParseInput:
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
        if input.lower().replace(" ", "") in self.COMMANDS:
            return self.COMMANDS.get(input) 
            #ritorna il valore associato alla chiave in COMMANDS
        else:
            return -1
        
    def parseMove(self, input):
        if re.match("[RDTAC][a-h][1-8]\s[a-h][1-8]", input) or re.match("[a-h][1-8]\s"
        "[a-h][1-8]", input):
            return input
        else:
            return -1