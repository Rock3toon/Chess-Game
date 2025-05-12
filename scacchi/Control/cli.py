import argparse
import sys
from scacchi.Entity.Partita import Partita
from scacchi.Control import parse_input 
from scacchi.Entity.Pezzo import Torre, Cavallo, Alfiere, Donna, Re, Pedone 
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
def gioca(Scacchiera, Partita):  # Funzione per avviare una nuova partita
    
    if Partita.get_stato_partita() != 0:

        # Posizionamento pezzi neri
        Scacchiera.set_pezzo_scacchiera(0, 0, Torre(1))
        Scacchiera.set_pezzo_scacchiera(0, 1, Cavallo(1))
        Scacchiera.set_pezzo_scacchiera(0, 2, Alfiere(1))
        Scacchiera.set_pezzo_scacchiera(0, 3, Donna(1))
        Scacchiera.set_pezzo_scacchiera(0, 4, Re(1))
        Scacchiera.set_pezzo_scacchiera(0, 5, Alfiere(1))
        Scacchiera.set_pezzo_scacchiera(0, 6, Cavallo(1))
        Scacchiera.set_pezzo_scacchiera(0, 7, Torre(1))
        for col in range(8):
            Scacchiera.set_pezzo_scacchiera(1, col, Pedone(1))

        # Posizionamento pezzi bianchi
        Scacchiera.set_pezzo_scacchiera(7, 0, Torre(0))
        Scacchiera.set_pezzo_scacchiera(7, 1, Cavallo(0))
        Scacchiera.set_pezzo_scacchiera(7, 2, Alfiere(0))
        Scacchiera.set_pezzo_scacchiera(7, 3, Donna(0))
        Scacchiera.set_pezzo_scacchiera(7, 4, Re(0))
        Scacchiera.set_pezzo_scacchiera(7, 5, Alfiere(0))
        Scacchiera.set_pezzo_scacchiera(7, 6, Cavallo(0))
        Scacchiera.set_pezzo_scacchiera(7, 7, Torre(0))
        for col in range(8):
            Scacchiera.set_pezzo_scacchiera(6, col, Pedone(0))

        # Imposta lo stato della partita a "in corso"
    
        Partita.cambia_stato_partita()
        Scacchiera.stampa_scacchiera(Scacchiera)  # Stampa la scacchiera iniziale
        print("La partita è iniziata! Buona fortuna!")

    else:
        print("Errore: la partita è già iniziata." \
        " Procedi con una mossa o digita /help per assistenza.")
        
                

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

def patta(partita):
    stato = partita.get_stato_partita()
    if stato == 0:                                                                                      # recupera lo stato della partita
        parse = parse_input.parse_input()                                                               # Crea un'istanza della classe parse_input
        giocatore=partita.get_turno()                                                                   # recupera il turno del giocatore
        if giocatore == 0:                                                                              # controlla se il giocatore a richiedere la patta è bianco o nero
            giocatore = "Nero"                                                                          # i colori sono invertiti rispetto al turno                 
        else:
            giocatore = "Bianco"

        while True:
            print("Sei sicuro di voler richiedere la PATTA l'operazione sarà IRREVERSIBILE? (si/no)")   
            risposta = parse.parseConfirm(input(">>>"))                                                 # prende in input la risposta dell'utente e usa il parser
            if risposta == 'si':                                                                        # controlla che la risposta sia 'si' 
                
                while True:
                    print(giocatore, "Vuoi accettare la patta? (si/no)")
                    risposta = parse.parseConfirm(input(">>>"))                                         # prende in input la risposta dell'utente e usa il parser                                        
                    if risposta == 'si':                                                                # controlla che la risposta sia 'si'
                        print("La partita è terminata in patta.")                                       
                        partita.cambia_stato_partita()                                                  # termina la partita tornando al menu principale    
                        break                                                                          
                    elif risposta == 'no':                                                              # controlla che la risposta sia 'no'
                        print("Patta rifiutata. La partita continua.")                                      
                        break
                    elif risposta == -1:                                                                # controlla se la risposta non è valida (il parser restituisce -1 se ci sono errori)
                        print("Risposta non valida, riprovare.")
                break                                                                                       
            
            elif risposta == 'no':                                                                      # controlla che la risposta sia 'no'
                print("Operazione annullata.")
                break                                                                                   # esce dal ciclo
            elif risposta == -1:                                                                        # controlla se la risposta non è valida (il parser restituisce -1 se ci sono errori)
                print("Risposta non valida, riprovare.")
    else:
        print("Nssuna partita in corso, impossibile richiedere la patta. " \
        "Usa /help per vedere l'elenco dei comandi")                                                         # controlla se la partita è in corso
                        

# Exportable CLI wrapper

# Avvio diretto
if __name__ == "__main__":
    args = ConfigurazioneParser().parse_args()
    if args.help:
        HelpCompleto()
    elif args.h:
        HelpRapido()
