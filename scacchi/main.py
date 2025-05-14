import argparse
from Boundary.welcome import visualizza_benvenuto
from Boundary.cli import esci, HelpCompleto, HelpRapido, abbandona, gioca, patta
from Control.GestoreMosse import GestioneInput
from Control.parse_input import parse_input
from Entity.Scacchiera import Scacchiera
from Entity.Partita import Partita
from Entity.Pezzo import Pezzo



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
                print("Comando non riconosciuto. Digitare /help per altre informazioni.")
            elif cmd == 1:
                HelpCompleto()  # mostra help completo
            elif cmd == 2:
                esci()          # /esci 
            elif cmd == 3:
                if partita.get_stato_partita() == 1:
                    print("La partita non è iniziata.")
                else:
                    scacchiera.stampa_scacchiera(scacchiera)  # mostra scacchiera    
            elif cmd == 4:
                gioca(scacchiera, partita)  # /gioca
            elif cmd == 5:
                abbandona(partita)  # /abbandona
            elif cmd == 6:
                patta(partita)  # /patta
            elif cmd == 7:
                partita.stampa_mosse()  # /mosse
        else:
            move_result = p.parseMove(user_input)
            if move_result == -1:
                print("La mossa non è scritta correttamente. Scrivi /help per altre informazioni.")
            else:
                GestioneInput(move_result, scacchiera, partita)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("-h",    action="store_true")
    parser.add_argument("--help", action="store_true")
    args = parser.parse_args()

    if args.help:
        HelpCompleto()
    elif args.h:
        HelpRapido()
    else:
        main()
        