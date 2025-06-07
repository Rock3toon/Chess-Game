import argparse

import scacchi.Boundary.errori as errori
from scacchi.Boundary.cli import HelpCompleto, HelpRapido, abbandona, esci, gioca, patta
from scacchi.Boundary.welcome import visualizza_benvenuto
from scacchi.Control.GestoreMosse import GestioneInput
from scacchi.Control.parse_input import parse_input
from scacchi.Entity.Partita import Partita
from scacchi.Entity.Scacchiera import Scacchiera


def main():
    """Run the Scacchi game and activate the GH workflows."""
    # Initialize parser and UI
    p = parse_input()
    scacchiera = Scacchiera() 
    partita = Partita()
    
    # Show welcome screen
    visualizza_benvenuto()

    # Main loop
    while True:
        user_input = input("> ")
        if user_input.startswith("/"):
            cmd = p.parseCommand(user_input)
            if cmd == -1:
                errori.errore_comando_non_riconosciuto()
            elif cmd == 1:
                HelpCompleto()  # mostra help completo
            elif cmd == 2:
                esci()          # /esci 
            elif cmd == 3:
                if partita.get_stato_partita() == 1:
                    errori.errore_nessuna_partita_scacchiera()
                else:
                    scacchiera.stampa_scacchiera(scacchiera)  # mostra scacchiera    
            elif cmd == 4:
                gioca(scacchiera, partita)  # /gioca
            elif cmd == 5:
                abbandona(partita, scacchiera)  # /abbandona
            elif cmd == 6:
                patta(partita, scacchiera)  # /patta
            elif cmd == 7:
                partita.stampa_mosse()  # /mosse
        else:
            move_result = p.parseMove(user_input)
            if move_result == -1:
                errori.errore_mossa_non_valida()
            else:
                GestioneInput(move_result, scacchiera, partita)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("-h",    action="store_true")
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args()

    if args.help:
        HelpCompleto()
        main()
    elif args.h:
        HelpRapido()
        main()
    else:
        main()
        