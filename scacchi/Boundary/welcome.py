from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.box import DOUBLE

def visualizza_benvenuto():
    """
    Visualizza una bella schermata di benvenuto per il gioco degli scacchi,
    utilizzando la libreria Rich per formattazione e colori.
    """
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
    
    # Creazione di un pannello per il messaggio principale con larghezza e padding ottimizzati
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
    tips_table = Table(show_header=False, box=DOUBLE, border_style="bright_green", expand=False)
    tips_table.add_column("Suggerimenti", style="bright_white", justify="center")
    
    tips_table.add_row("[bold magenta]Sfida un altro giocatore e affina le tue abilità nel gioco degli scacchi[/]")
    tips_table.add_row("[bold blue]Osserva con attenzione, pianifica con pazienza e colpisci con precisione[/]")
    tips_table.add_row("🧩 [bold red]Scacco matto... o forse no? 🔥[/]")
    tips_table.add_row("[bold yellow]🏆 Buon gioco! Preparati a sfide emozionanti 🏆[/]")
    
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
