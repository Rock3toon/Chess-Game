import argparse
import sys
from scacchi.Entity.Partita import Partita
from scacchi.Control import parse_input  
from rich.console import Console
from rich.text import Text

console = Console()

def ConfigurazioneParser():
    parser = argparse.ArgumentParser(
        usage="Nome del programma [--help] | [-h]",
        description=(
            "➤ Regole principali:\n"
            "- Inizia il giocatore con i pezzi bianchi, seguito dal giocatore con i pezzi neri.\n"
            "- Durante il proprio turno, il giocatore deve specificare:\n"
            "  1. Se intende muovere un pezzo diverso dal pedone, indicarlo con:\n"
            "     - 'C' per Cavallo\n"
            "     - 'A' per Alfiere\n"
            "     - 'T' per Torre\n"
            "     - 'D' per Donna\n"
            "     - 'R' per Re\n"
            "  2. La coordinata di partenza (es. e2).\n"
            "  3. Uno spazio per separare la coordinata di partenza da quella di arrivo.\n"
            "  4. La coordinata di arrivo (es. e4).\n"
            "  Esempio: 'Cg1 f3' per muovere il cavallo da g1 a f3.\n"
            "           'e2 e4' per muovere un pedone da e2 a e4.\n"
            "- Il gioco termina con scacco matto, patta o abbandono.\n"
        ),
        epilog=(
            "➤ Comandi in gioco:\n"
            "  /help          # Mostra la guida dei comandi in gioco\n"
            "  /gioca         # Avvia una nuova partita\n"
            "  /abbandona     # Abbandona la partita corrente\n"
            "  /patta         # Chiede la patta all'avversario\n"
            "  /scacchiera    # Mostra la scacchiera attuale\n"
            "  /mosse         # Mostra le mosse effettuate\n"
            "  /esci          # Esce dal programma\n\n"
            "Progetto sviluppato per il corso di Ingegneria del Software.\n"
            "Autori: Gruppo NAUR\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument("-h", action="store_true", help="Mostra la guida rapida")
    parser.add_argument("--help", action="store_true", help="Mostra la guida completa")
    return parser

def HelpCompleto():
    console.print("[bold cyan]♔  GUIDA COMPLETA AL GIOCO DEGLI SCACCHI  ♔[/]", justify="center")
    console.print()
    console.print(Text("➤ REGOLE PRINCIPALI", style="bold white on blue"))
    print(
        "- Inizia il giocatore con i pezzi bianchi, seguito dal giocatore con i pezzi neri.\n"
        "- Durante il proprio turno, il giocatore deve specificare:\n"
        "  1. Se intende muovere un pezzo diverso dal pedone, indicarlo con:\n"
        "     - 'C' per Cavallo\n"
        "     - 'A' per Alfiere\n"
        "     - 'T' per Torre\n"
        "     - 'D' per Donna\n"
        "     - 'R' per Re\n"
        "  2. La coordinata di partenza (es. e2).\n"
        "  3. Uno spazio per separare la coordinata di partenza da quella di arrivo.\n"
        "  4. La coordinata di arrivo (es. e4).\n"
        "  Esempio: 'Cg1 f3' per muovere il cavallo da g1 a f3.\n"
        "           'e2 e4' per muovere un pedone da e2 a e4.\n"
        "- Il gioco termina con scacco matto, patta o abbandono.\n"
    )
    console.print(Text("➤ COMANDI UTILI IN GIOCO", style="bold white on green"))
    print(
        "  /gioca          - Avvia una nuova partita\n"
        "  /abbandona      - Abbandona la partita corrente\n"
        "  /patta          - Chiede la patta all'avversario\n"
        "  /scacchiera     - Mostra la scacchiera attuale\n"
        "  /mosse          - Mostra le mosse effettuate\n"
        "  /esci           - Esce dal programma\n"
    )
    console.print()
    console.print(Text("Progetto sviluppato per il corso di Ingegneria del Software.", style="italic dim"))
    console.print(Text("Autori: Gruppo NAUR", style="italic blue"))

def HelpRapido():
    console.print("[bold cyan]♔  GUIDA RAPIDA AI COMANDI  ♔[/]", justify="center")
    console.print(Text("➤ COMANDI UTILI IN GIOCO", style="bold white on green"))
    print(
        "  /gioca          - Avvia una nuova partita\n"
        "  /abbandona      - Abbandona la partita corrente\n"
        "  /patta          - Chiede la patta all'avversario\n"
        "  /scacchiera     - Mostra la scacchiera attuale\n"
        "  /mosse          - Mostra le mosse effettuate\n"
        "  /esci           - Esce dal programma\n"
    )


def abbandona(partita):
        parse=parse_input.parse_input()                                                     # Crea un'istanza della classe parse_input
        while True:
            print("Confermi l'abbandono della partita? (si/no)")    
            risposta = parse.parseConfirm(input(">>>"))                                     #prende in input la risposta dell'utente e usa il parser
            if risposta == 'si':
                #controlla che la risposta sia 'si' e determina il vincitore in base al turno attuale
                turno_attuale = partita.get_turno()  # 0 = giocatore 1, 1 = giocatore 2
                vincitore = 2 if turno_attuale == 0 else 1
                print(f"Partita abbandonata... GIOCATORE {vincitore} ha vinto!")
                partita.cambia_stato_partita()  # Imposta lo stato della partita come terminato
                print("Per effettuare una nuova partita digita '/gioca'")
                break
                                              
            elif risposta == 'no':                                                          #controlla che la risposta sia 'no'
                print("Operazione annullata!")
                break                                                                      #esce dal ciclo e continua la partita  
                                              
            elif risposta == -1:                                                           #controlla se la risposta non è valida (il parser restituisce -1 se ci sono errori) 
                print("Risposta non valida! Riprova")

def esci():                                                                                 # Funzione che permette di uscire dal programma restituendo il controllo al sistema operativo
        parse=parse_input.parse_input()                                                     # Crea un'istanza della classe parse_input
        while True:
            print("Sei sicuro di voler uscire l'operazione sarà IRREVERSIBILE? (si/no)")    #chiede all'utente di confermare l'uscita
            risposta = parse.parseConfirm(input(">>>"))                                     #prende in input la risposta dell'utente e usa il parser
            if risposta == 'si':                                                            #controlla che la risposta sia 'si'
                print("Uscita in corso...")
                sys.exit(0)                                                                 #esce dal programma    

            elif risposta == 'no':                                                          #controlla che la risposta sia 'no'
                print("Operazione annullata!")
                break                                                                      #esce dal ciclo   

            elif risposta == -1:                                                            #controlla se la risposta non è valida (il parser restituisce -1 se ci sono errori) 
                print("Risposta non valida! Riprova")
                

# Exportable CLI wrapper

# Avvio diretto
if __name__ == "__main__":
    args = ConfigurazioneParser().parse_args()
    if args.help:
        HelpCompleto()
    elif args.h:
        HelpRapido()
