"""Modulo boundary per l'interfaccia a riga di comando (CLI) del gioco degli scacchi.

Questo modulo gestisce:
- La configurazione del parser degli argomenti (-h, --help)
- La visualizzazione di guide rapide e complete tramite Rich Console
- I comandi di gioco: /gioca, /abbandona, /patta, /scacchiera, /mosse, /esci
- L'inizializzazione e il controllo dello stato della partita e della scacchiera
- L'interazione utente/gioco, incluse conferme e validazioni tramite ParseInput
"""

import argparse
import sys

from rich.console import Console
from rich.text import Text

import scacchi.Boundary.scacchi_ui as ui
import scacchi.Error.errori as errori
from scacchi.Control.parse_input import parse_input
from scacchi.Entity.Pezzi.Alfiere import Alfiere
from scacchi.Entity.Pezzi.Cavallo import Cavallo
from scacchi.Entity.Pezzi.Donna import Donna
from scacchi.Entity.Pezzi.Pedone import Pedone
from scacchi.Entity.Pezzi.Re import Re
from scacchi.Entity.Pezzi.Torre import Torre

console = Console()


def ConfigurazioneParser():
    """Configura il parser degli argomenti della riga di comando."""
    parser = argparse.ArgumentParser(
        usage="Nome del programma [--help] | [-h]",
        description=(
            "➤ Regole principali:\n"
            "- Inizia il giocatore con i pezzi bianchi, seguito dal giocatore con i"
            " pezzi neri.\n\n"
            "- Durante il proprio turno per effettuare una mossa,"
            " il giocatore deve specificare:\n"
            "  1. Se intende muovere un pezzo diverso dal pedone, indicarlo con:\n"
            "     - 'C' per Cavallo (es: 'Cf3')\n"
            "     - 'A' per Alfiere (es: 'Ac4')\n"
            "     - 'T' per Torre (es: 'Td1')\n"
            "     - 'D' per Donna (es: 'Dd3')\n"
            "     - 'R' per Re (es: 'Re2')\n"
            "  2. La coordinata di arrivo (es. e4).\n"
            "  Esempio pratico: Turno del bianco:\n"
            "    Input>> 'e4'\n"
            "          --Si muove il pedone bianco da e2 a e4\n"
            "           Turno del nero:\n"
            "    Input>> 'Cf3'\n"
            "          --Si muove il cavallo nero da g8 a f6\n\n"
            "- Durante il proprio turno per effettuare una cattura," \
            " il giocatore deve specificare:\n"
            "  1. Se intende effettuare una cattura con un pezzo diverso dal pedone,"
            " indicarlo con:\n"
            "     - 'C' per Cavallo\n"
            "     - 'A' per Alfiere\n"
            "     - 'T' per Torre\n"
            "     - 'D' per Donna\n"
            "     - 'R' per Re\n"
            "  [Per il pedone, deve specificare direttamente la colonna di partenza"
            " del pedone da utilizzare per la cattura]\n"
            "  2. Deve inserire 'x' tra il pezzo (o colonna per il pedone)"
            " e la casa di arrivo.\n"
            "   Esempio:\n"
            "     - Pedone: 'exd5' (il pedone sulla colonna 'e' cattura in d5)\n"
            "     - Cavallo: 'Cxf3' (il cavallo cattura in f3)\n\n"
            "- Se con la mossa o cattura vi è una situazione"
            " che permetta la promozione del pedone, il giocatore deve specificare:\n"
            "  1. La notazione di mossa o cattura del pedone (es: 'a1' | 'exd8').\n"
            "  2. Come carattere finale (escluso il Re, secondo le regole)"
            " rispettivamente:\n"
            "     - 'D' per promuovere a Donna\n"
            "     - 'T' per promuovere a Torre\n"
            "     - 'A' per promuovere ad Alfiere\n"
            "     - 'C' per promuovere a Cavallo\n"
            "   Esempio:\n"
            "   'e8D' per effettuare la mossa e promuovere a Donna\n"
            "   'bxa1T' per effettuare la cattura e promuovere a Torre\n"
            "- Per effettuare l'arrocco, il giocatore deve specificare:\n"
            "  1. '0-0' per l'arrocco corto (Re si sposta di due case verso la Torre in"
            " colonna h)\n"
            "  2. '0-0-0' per l'arrocco lungo (Re si sposta di due case verso la Torre"
            " in colonna a)\n"
            "  Attenzione! L'arrocco è possibile solo se:\n"
            "     i.   Il Re non è sotto scacco\n"
            "     ii.  Il Re e la Torre non sono stati mai mossi.\n"
            "     iii. Le case tra il Re e la Torre sono vuote e non sono sotto scacco."
            "\n"
            "- Il gioco termina con scacco matto, patta, abbandono o stallo.\n"
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
            "Progetto sviluppato per il corso di Ingegneria del Software\n"
            "Autori: Gruppo NAUR\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    parser.add_argument("-h", action="store_true", help="Mostra la guida rapida")
    parser.add_argument("--help", action="store_true", help="Mostra la guida completa")
    return parser


def HelpCompleto():
    """Visualizza la guida completa al gioco degli scacchi."""
    console.print("[bold cyan]♔  GUIDA COMPLETA AL GIOCO DEGLI SCACCHI  ♔[/]", 
                  justify="center")
    console.print()
    console.print(Text("➤ REGOLE PRINCIPALI", style="bold white on blue"))
    print(
            "➤ Regole principali:\n"
            "- Inizia il giocatore con i pezzi bianchi, seguito dal giocatore con i" \
            " pezzi neri.\n\n"
            "- Durante il proprio turno per effettuare una mossa," \
            " il giocatore deve specificare:\n"
            "  1. Se intende muovere un pezzo diverso dal pedone, indicarlo con:\n"
            "     - 'C' per Cavallo (es: 'Cf3')\n"
            "     - 'A' per Alfiere (es: 'Ac4')\n"
            "     - 'T' per Torre (es: 'Td1')\n"
            "     - 'D' per Donna (es: 'Dd3')\n"
            "     - 'R' per Re (es: 'Re2')\n"
            "  2. La coordinata di arrivo (es. e4).\n"
            "  Esempio pratico: Turno del bianco:\n"
            "    Input>> 'e4'\n"
            "          --Si muove il pedone bianco da e2 a e4\n"
            "           Turno del nero:\n"
            "    Input>> 'Cf3'\n"
            "          --Si muove il cavallo nero da g8 a f6\n\n"
            "- Durante il proprio turno per effettuare una cattura," \
            " il giocatore deve specificare:\n"
            "  1. Se intende effettuare una cattura con un pezzo diverso dal pedone," \
            " indicarlo con:\n"
            "     - 'C' per Cavallo\n"
            "     - 'A' per Alfiere\n"
            "     - 'T' per Torre\n"
            "     - 'D' per Donna\n"
            "     - 'R' per Re\n"
            "  [Per il pedone, deve specificare direttamente la colonna di partenza" \
            " del pedone da utilizzare per la cattura]\n"
            "  2. Deve inserire 'x' tra il pezzo (o colonna per il pedone)" \
            " e la casa di arrivo.\n"
            "   Esempio:\n"
            "     - Pedone: 'exd5' (il pedone sulla colonna 'e' cattura in d5)\n"
            "     - Cavallo: 'Cxf3' (il cavallo cattura in f3)\n\n"
            "- Se con la mossa o cattura vi è una situazione" \
            " che permetta la promozione del pedone, il giocatore deve specificare:\n"
            "  1. La notazione di mossa o cattura del pedone (es: 'a1' | 'exd8').\n"
            "  2. Come carattere finale (escluso il Re, secondo le regole)" \
            " rispettivamente:\n"
            "     - 'D' per promuovere a Donna\n"
            "     - 'T' per promuovere a Torre\n"
            "     - 'A' per promuovere ad Alfiere\n"
            "     - 'C' per promuovere a Cavallo\n"
            "   Esempio:\n"
            "   'e8D' per effettuare la mossa e promuovere a Donna\n"
            "   'bxa1T' per effettuare la cattura e promuovere a Torre\n"
            "- Per effettuare l'arrocco, il giocatore deve specificare:\n"
            "  1. '0-0' per l'arrocco corto (Re si sposta di due case verso la Torre in"
            " colonna h)\n"
            "  2. '0-0-0' per l'arrocco lungo (Re si sposta di due case verso la Torre"
            " in colonna a)\n"
            "  Attenzione! L'arrocco è possibile solo se:\n"
            "     i.   Il Re non è sotto scacco\n"
            "     ii.  Il Re e la Torre non sono stati mai mossi.\n"
            "     iii. Le case tra il Re e la Torre sono vuote e non sono sotto scacco."
            "\n"
            "- Il gioco termina con scacco matto, patta, abbandono o stallo.\n"
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
    console.print(Text("Progetto sviluppato per il corso di Ingegneria del Software.", 
                       style="italic dim"))
    console.print(Text("Autori: Gruppo NAUR", style="italic blue"))


def HelpRapido():
    """Visualizza la guida rapida al gioco degli scacchi."""
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


def gioca(Scacchiera, Partita):
    """Avvia una nuova partita di scacchi."""
    if Partita.get_stato_partita() != 0:
        Partita.azzera_mosse()  # Azzera le mosse della partita
        Partita.set_turno()  # Imposta il turno iniziale
        Scacchiera.azzera_istanze()  # Azzera le istanze della scacchiera
        # Inizializza la scacchiera
        for riga in range(2, 6):
            for colonna in range(8):
                Scacchiera.set_pezzo_scacchiera(riga, colonna, None)

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
        Scacchiera.inizializza_istanze()  
        # Popola la lista delle istanze con i pezzi iniziali
        text_start = "La partita è iniziata. Buona fortuna!"
        console.print(Text(text_start, style="bold yellow"), justify="center")
        text_turno = "TURNO DEL BIANCO: In attesa della mossa...\n"
        console.print(Text(text_turno, style="italic grey50"), justify="center")
        Scacchiera.stampa_scacchiera(Scacchiera)  # Stampa la scacchiera iniziale
        
    else:
        errori.errore_gioca()


def abbandona(partita, scacchiera):
    """Abbandona la partita corrente."""
    stato = partita.get_stato_partita()
    if stato == 0:
        # Controlla se la partita è in corso
        parse = parse_input()
        print("Confermi l'abbandono della partita? (si/no)")    
        risposta = parse.parseConfirm(input(">>>"))
        if risposta == 'si':
            turno_attuale = partita.get_turno()  # 0 = giocatore 1, 1 = giocatore 2
            vincitore = "NERO" if turno_attuale == 0 else "BIANCO"
            partita.cambia_stato_partita()
            ui.print_abbandono_partita(vincitore)
        elif risposta == 'no':
            print("Operazione annullata!")
        elif risposta == -1:
            # Errore di parsing
            errori.errore_risposta()
    else:        
        errori.errore_nessuna_partita_abbandona()


def esci():
    """Esce dal programma."""
    parse = parse_input()                                          
    print("Sei sicuro di voler uscire l'operazione sarà IRREVERSIBILE? (si/no)")   
    risposta = parse.parseConfirm(input(">>>"))                                    
    if risposta == 'si':          
        print("Uscita in corso...")
        sys.exit(0)                
    elif risposta == 'no':                                                   
        print("Operazione annullata!")
    elif risposta == -1:
        errori.errore_risposta()  


def patta(partita, scacchiera):
    """Richiede la patta nella partita corrente."""
    stato = partita.get_stato_partita()
    if stato == 0:                                                                     
        parse = parse_input()                                                          
        giocatore = partita.get_turno()         
        giocatore = "NERO" if giocatore == 0 else "BIANCO"    

        print("Sei sicuro di voler richiedere la PATTA l'operazione sarà"
              " IRREVERSIBILE? (si/no)")   
        risposta = parse.parseConfirm(input(">>>"))                                
        if risposta == 'si':                                     
            print(f"Giocatore {giocatore} vuoi accettare la patta? (si/no)")
            risposta = parse.parseConfirm(input(">>>"))                     
            if risposta == 'si':                                             
                ui.print_patta_accettata()
                partita.cambia_stato_partita()                                                                                                     

            elif risposta == 'no':                                           
                print("La richiesta di patta è stata rifiutata dal giocatore"
                      f"{giocatore}.")
            elif risposta == -1:                                             
                errori.errore_risposta()
        elif risposta == 'no':                                                   
            print("Operazione annullata.")
        elif risposta == -1:                                                     
            errori.errore_risposta()
    else:
        errori.errore_nessuna_partita_patta()                  


def partita_in_scacco_matto(partita):
    """Termina la partita in caso di scacco matto."""
    turno_attuale = partita.get_turno()  # 0 = giocatore 1, 1 = giocatore 2
    vincitore = "NERO" if turno_attuale == 0 else "BIANCO"
    ui.print_scacco_matto(vincitore)
