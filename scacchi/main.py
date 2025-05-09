from scacchi.Control import parse_input
from rich import print

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
        RICH_COLORS: set[str] = {
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        }

        # If the user provides an accent color, then use it
        if accent_color in RICH_COLORS:
            self._ACCENT_COLOR = accent_color
        else:
            raise ValueError(
                f"Invalid accent color '{self._ACCENT_COLOR}'. "
                "Please choose a color supported by the Rich library."
            )

    def get_accent_color(self) -> str:
        """Get the accent color for the game's UI.

        Returns:
            accent color

        """
        return self._ACCENT_COLOR


def main():
    """Run the Scacchi game and activate the GH workflows."""
    p = parse_input.parse_input()
    ui = UI()
    ui.set_accent_color("blue")

    name = input("Benvenuto in Scacchi! Inserisci il tuo nome: ")
    print(
        f"Ciao [bold {ui.get_accent_color()}]{name}[/bold {ui.get_accent_color()}]! "
        "Iniziamo a giocare a [bold]scacchi[/bold]!"
        # Aggiungere la chiamata ad una funzione di benvenuto
    )

    while True:
        user_input = input("> ")
        if user_input.startswith("/"):
            if p.parseCommand(user_input) == -1:
                print("Comando non riconosciuto. " \
                "Digitare /help per altre informazioni.")
            elif p.parseCommand(user_input) == 1:
                #/help
                pass
            elif p.parseCommand(user_input) == 2:
                #/esci
                pass
            elif p.parseCommand(user_input) == 3:
                #/scacchiera
                pass
            elif p.parseCommand(user_input) == 4:
                #/gioca
                pass
            elif p.parseCommand(user_input) == 5:
                #/abbandona
                break
            elif p.parseCommand(user_input) == 6:
                #/patta
                pass
            elif p.parseCommand(user_input) == 7:
                #/mosse
                pass
        elif p.parseMove(user_input)== -1:
            print("La mossa non è scritta correttamente. " \
            "Scrivi /help per altre informazioni.")
        else:
            print(p.parseMove(user_input))
            # Gestione della mossa che chiama come paremetro p.parseMove(user_input)
            pass
            

if __name__ == "__main__":
    main()