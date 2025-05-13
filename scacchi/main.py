import argparse
from scacchi.Boundary.welcome import visualizza_benvenuto
from scacchi.Control.cli import esci, HelpCompleto, HelpRapido, abbandona, gioca, patta
from scacchi.Control.GestoreMosse import GestioneInput
from scacchi.Control.parse_input import parse_input
from scacchi.Entity.Scacchiera import Scacchiera
from scacchi.Entity.Partita import Partita
from scacchi.Entity.Pezzo import Pezzo


class UI:
    """Defines the configuration of the game's UI."""

    def __init__(self):
        """Initialize the game's UI with default settings."""
        self._ACCENT_COLOR: str = "red"

    def set_accent_color(self, accent_color: str):
        """Set the accent color for the game's UI.

        List of valid colors supported by the Rich library:
            - `black`
            - `red`
            - `green`
            - `yellow`
            - `blue`
            - `magenta`
            - `cyan`
            - `white`
            - `bright_black`
            - `bright_red`
            - `bright_green`
            - `bright_yellow`
            - `bright_blue`
            - `bright_magenta`
            - `bright_cyan`
            - `bright_white`

        Args:
            accent_color (str): the accent color to be used in the game's UI

        Raises:
            ValueError: if the accent color is not supported by the Rich library
        """
        RICH_COLORS = {
            "black", "red", "green", "yellow", "blue",
            "magenta", "cyan", "white", "bright_black",
            "bright_red", "bright_green", "bright_yellow",
            "bright_blue", "bright_magenta", "bright_cyan",
            "bright_white",
        }

        if accent_color in RICH_COLORS:
            self._ACCENT_COLOR = accent_color
        else:
            raise ValueError(
                f"Invalid accent color '{accent_color}'. "
                "Choose a color supported by the Rich library."
            )

    def get_accent_color(self) -> str:
        """Get the accent color for the game's UI."""
        return self._ACCENT_COLOR


def main():
    """Run the Scacchi game and activate the GH workflows."""
    # Initialize parser and UI
    p = parse_input()
    ui = UI()
    ui.set_accent_color("blue")
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
        