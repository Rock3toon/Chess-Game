from rich.align import Align
from rich.box import DOUBLE
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

"""
Modulo << Boundary >> per i messaggi di benvenuto e terminazione del gioco.

Descrizione:
Contiene tutte le funzioni per stampare schermate formattate utilizzando la
libreria Rich per una migliore esperienza utente.

"""

def print_benvenuto():
    """Visualizza una schermata di benvenuto per il gioco degli scacchi."""
    # Visualizza una bella schermata di benvenuto per il gioco degli scacchi,
    # utilizzando la libreria Rich per formattazione e colori.
    console = Console()
    
    # Titolo ASCII art con colori personalizzati
    title_art = Text("""
           ____     ____      _       ____    ____   _   _   ___             
░▒▓█▓▒░   / ___|   / ___|    / \     / ___|  / ___| | | | | |_ _|  ░▒▓█▓▒░ 
░▒▓█▓▒░   \___ \  | |       / _ \   | |     | |     | |_| |  | |   ░▒▓█▓▒░ 
░▒▓█▓▒░    ___) | | |___   / ___ \  | |___  | |___  |  _  |  | |   ░▒▓█▓▒░ 
░▒▓█▓▒░   |____/   \____| /_/   \_\  \____|  \____| |_| |_| |___|  ░▒▓█▓▒░ 
""" , style="bold cyan")
    
    # Messaggio di benvenuto formattato e multilinea
    welcome_message = Text(
        "\nBenvenuto nella nostra applicazione di scacchi\n"
        "Siamo felici di averti fra noi!\n",
        style="yellow italic",
        justify="center"
    )
    
    # Creazione di un pannello per il messaggio principale con larghezza e
    # padding ottimizzati
    main_panel = Panel(
        welcome_message,
        title="[bold]♙   SCACCHI   ♙[/]",
        border_style="bright_white",
        title_align="center",
        width=60,
        padding=(1, 2),
        expand=False
    )
    
    # Tabella per i suggerimenti
    tips_table = Table(show_header=False, box=DOUBLE, border_style="bright_green", \
                       expand=False)
    tips_table.add_column("Suggerimenti", style="bright_white", justify="center")
    
    tips_table.add_row("[bold magenta]Sfida un altro giocatore e affina le tue abilità"
                       "nel gioco degli scacchi[/]")
    tips_table.add_row("[bold blue]Osserva con attenzione, pianifica con pazienza e" 
                       "colpisci con precisione[/]")
    tips_table.add_row("🧩 [bold red]Scacco matto... o forse no? 🔥[/]")
    tips_table.add_row("[bold yellow]🏆 Buon gioco! Preparati a sfide " 
                       "emozionanti 🏆[/]")
    
    # Footer
    footer = Text(
        "Digita /gioca per iniziare subito una partita, oppure /help per vedere "
        "l’elenco completo dei comandi...",
        style="dim white",
        justify="center"
    )
    
    # Stampa tutto con l'allineamento appropriato
    console.print("\n")
    console.print(Align.center(title_art))
    console.print("\n")
    console.print(Align.center(main_panel))
    console.print("\n")
    console.print(Align.center(tips_table))
    console.print("\n")
    console.print(Align.center(footer))
    console.print("\n")
    
    # Opzionale: attendi che l'utente prema un tasto per continuare
    # input()

def print_abbandono_partita(vincitore):
    """Visualizza il messaggio di vittoria per abbandono dell'avversario."""
    console = Console()

    # Titolo semplice ma visivo
    titolo = Text("🏳️   PARTITA ABBANDONATA 🏳️", style="bold white", justify="center")

    # Messaggio centrale - CORREZIONE: rimuovi i tag markup e usa Text.append()
    messaggio = Text(justify="center")
    messaggio.append("\nIl giocatore ", style="bold white")
    messaggio.append(vincitore, style="bold cyan")
    messaggio.append(" vince la partita per abbandono dell'avversario.\n", \
                     style="bold white")

    # Pannello per evidenziare la situazione
    pannello_abbandono = Panel(
        messaggio,
        title="[bold blue]🏁 PARTITA TERMINATA 🏁[/]",
        border_style="bright_green",
        title_align="center",
        width=70,
        padding=(1, 2),
        expand=False,
        box=DOUBLE
    )

    # Footer per suggerimenti
    footer = Text(
        "Digita /gioca per iniziare una nuova partita, oppure /esci per uscire.",
        style="dim white",
        justify="center"
    )

    # Stampa finale
    console.print("\n")
    console.print(Align.center(titolo))
    console.print("\n")
    console.print(Align.center(pannello_abbandono))
    console.print("\n")
    console.print(Align.center(footer))
    console.print("\n")


def print_patta_accettata():
    """Stampa il messaggio di partita terminata in patta per accordo tra i giocatori."""
    console = Console()
    
    # Titolo semplice ma visivo
    titolo = Text("🤝  PATTA ACCETTATA 🤝", style="bold green", justify="center")
    
    # Messaggio centrale con notifica di pareggio
    messaggio = Text(justify="center")
    messaggio.append("La partita è terminata in ", style="bold white")
    messaggio.append("patta (pareggio) ", style="bold yellow")
    messaggio.append("\n", style="bold white")
    messaggio.append("Nessun vincitore... ma che sfida avvincente!\n", \
                     style="bold white")

    # Pannello per evidenziare la situazione
    pannello_stallo = Panel(
          messaggio,
          title="[bold blue]🏁 PARTITA TERMINATA 🏁 [/]",
          border_style="bright_magenta",
          title_align="center",
          width=70,
          padding=(1, 2),
          expand=False,
          box=DOUBLE
    )

    # Footer per suggerimenti
    footer = Text(
          "Digita /gioca per iniziare una nuova partita, oppure /esci per uscire.",
          style="dim white",
          justify="center"
    )

    # Stampa finale
    console.print("\n")
    console.print(Align.center(titolo))
    console.print("\n")
    console.print(Align.center(pannello_stallo))
    console.print("\n")
    console.print(Align.center(footer))
    console.print("\n")


def print_stallo_partita():
    """Visualizza il messaggio di partita terminata in stallo (patta tecnica)."""
    console = Console()

    # Titolo semplice ma visivo
    titolo = Text("⛔  STALLO! ⛔", style="bold red", justify="center")

    # Messaggio centrale con notifica di pareggio
    messaggio = Text(justify="center")
    messaggio.append("La partita è terminata in ", style="bold white")
    messaggio.append("patta (pareggio) ", style="bold yellow")
    messaggio.append("\n", style="bold white")
    messaggio.append("Nessun vincitore questa volta, ma che sfida avvincente!\n", \
                     style="bold white")

    # Pannello per evidenziare la situazione
    pannello_stallo = Panel(
        messaggio,
        title="[bold blue]🏁 PARTITA TERMINATA 🏁 [/]",
        border_style="bright_green",
        title_align="center",
        width=70,
        padding=(1, 2),
        expand=False,
        box=DOUBLE
    )

    # Footer per suggerimenti
    footer = Text(
        "Digita /gioca per iniziare una nuova partita, oppure /esci per uscire.",
        style="dim white",
        justify="center"
    )

    # Stampa finale
    console.print("\n")
    console.print(Align.center(titolo))
    console.print("\n")
    console.print(Align.center(pannello_stallo))
    console.print("\n")
    console.print(Align.center(footer))
    console.print("\n")


def print_scacco_matto(vincitore):
    """Visualizza il messaggio di vittoria per scacco matto."""
    console = Console()
    
    # Titolo con stile alternativo al rosso
    titolo = Text("♚  SCACCO MATTO! ♚", style="bold yellow", justify="center")

    # Messaggio principale - CORREZIONE: rimuovi i tag markup e usa Text.append()
    messaggio = Text(justify="center")
    messaggio.append("\nIl giocatore ", style="bright_white")
    messaggio.append(vincitore, style="bold yellow")
    messaggio.append(" ha vinto la partita per scacco matto!\n", style="bright_white")
    messaggio.append("Complimenti per la vittoria! 🏆\n", style="bold magenta")

    # Pannello contenente il messaggio
    pannello_vittoria = Panel(
        messaggio,
        title="[bold blue]🏁 PARTITA TERMINATA 🏁[/]",
        border_style="bright_green",
        title_align="center",
        width=70,
        padding=(1, 2),
        expand=False,
        box=DOUBLE
    )

    # Footer con suggerimento per continuare
    footer = Text(
        "Digita /gioca per iniziare una nuova partita, oppure /esci per uscire.",
        style="dim white",
        justify="center"
    )

    # Stampa allineata
    console.print("\n")
    console.print(Align.center(titolo))
    console.print("\n")
    console.print(Align.center(pannello_vittoria))
    console.print("\n")
    console.print(Align.center(footer))
    console.print("\n")