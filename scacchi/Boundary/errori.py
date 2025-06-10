# Errori di cli.py

def errore_gioca():
    """Stampa un messaggio di errore se la partita è già in corso."""
    print("Errore: la partita è già iniziata. \
         \nProcedi con una mossa o digita /help per altre informazioni.")


def errore_risposta():
    """Stampa un messaggio di errore se la risposta non è valida."""
    print("Risposta non valida! Riprova")

def errore_nessuna_partita_abbandona():
    """Stampa un messaggio di errore se non c'è una partita da abbandonare."""
    print("Errore, nessuna partita in corso, impossibile abbandonare la partita.  \
        \nUsa /help per altre informazioni.")
    
def errore_nessuna_partita_patta():
    """Stampa un messaggio di errore se non c'è una partita da richiedere la patta."""
    print("Errore, nessuna partita in corso, impossibile richiedere la patta. \
        \nUsa /help per altre informazioni.")



# Errori GestoreMosse.py

def errore_nessuna_partita():
    """Stampa un messaggio di errore se non c'è una partita in corso."""
    print("Errore, nessuna partita in corso. \
         \nScrivi /gioca per avviare una partita.")


# Errori di partita.py


def errore_stampa_mosse():
    """Stampa un messaggio di errore se non ci sono mosse da stampare."""
    print("Errore, nessuna mossa effettuata.")





# Errori di Pedone.py


def errore_mossa_pedone():
    """Stampa un messaggio di errore se la mossa del pedone non è valida."""
    print("Errore, la mossa è illegale. Il pedone non può muoversi in quella casella. \
        \nDigita /help per altre informazioni.")

def errore_cattura_non_valida():
    """Stampa un messaggio di errore se la cattura non è valida."""
    print("Errore, la cattura non è valida. \
        \nDigita /help per altre informazioni.")

def errore_cattura_enpassant_non_valida():
    """Stampa un messaggio di errore se la cattura in en passant non è valida."""
    print("Errore, la cattura in en passant non è valida. \
        \nDigita /help per altre informazioni.")

def errore_nessuna_cattura_valida():
    """Stampa un messaggio di errore se non ci sono catture valide."""
    print("Errore, nessuna cattura valida. \
        \nDigita /help per altre informazioni.")


# Errori di Cavallo.py

def errore_cavallo_mossa_illegale():
    """Stampa un messaggio di errore se la mossa del cavallo non è valida."""
    print("Errore, la mossa del cavallo è illegale. \
        \nDigita /help per altre informazioni.")
def errore_cavallo_mossa_ambigua():
    """Stampa un messaggio di errore se la mossa del cavallo è ambigua."""
    print("Errore, la mossa del cavallo è ambigua. \
        \nDigita /help per altre informazioni.")
def errore_cavallo_errore_disambiguazione():
    """Stampa un messaggio di errore se c'è un errore di disambiguazione del cavallo."""
    print("Errore, la disambiguazione del cavallo non è corretta. \
        \nDigita /help per altre informazioni.")
def errore_cavallo_cattura_vuota():
    """Stampa un messaggio d'errore se il cavallo cerca di catturare una casa vuota."""
    print("Errore, il cavallo non può catturare una casa vuota. \
        \nDigita /help per altre informazioni.")
def errore_cavallo_cattura_non_specificata():
    """Stampa un messaggio di errore se la cattura del cavallo non è specificata."""
    print("Errore, la cattura del cavallo non è specificata. \
        \nDigita /help per altre informazioni.")

   
# Errori di Alfiere.py

def errore_alfiere_mossa_illegale():
    """Stampa un messaggio di errore se la mossa dell'alfiere non è valida."""
    print("Errore, la mossa dell'alfiere è illegale. \
        \nDigita /help per altre informazioni.")

def errore_alfiere_mossa_ambigua():
    """Stampa un messaggio di errore se la mossa dell'alfiere è ambigua."""
    print("Errore, la mossa dell'alfiere è ambigua. \
        \nDigita /help per altre informazioni.")

def errore_alfiere_errore_disambiguazione():
    """Stampa un messaggio di errore in caso di disambiguazione dell'alfiere."""
    print("Errore, la disambiguazione dell'alfiere non è corretta. \
        \nDigita /help per altre informazioni.")

def errore_alfiere_cattura_vuota():
    """Stampa un messaggio di errore se l'alfiere tenta di catturare una casa vuota."""
    print("Errore, l'alfiere non può catturare una casa vuota. \
        \nDigita /help per altre informazioni.")

def errore_alfiere_cattura_non_specificata():
    """Stampa messaggio di errore se la cattura dell'alfiere non è stata specificata."""
    print("Errore, la cattura dell'alfiere non è stata specificata. \
        \nDigita /help per altre informazioni.")

    

# Errori di Torre.py

def errore_torre_mossa_illegale():
    """Stampa un messaggio di errore se la mossa della torre non è valida."""
    print("Errore, la mossa della torre è illegale. \
        \nDigita /help per altre informazioni.")

def errore_torre_mossa_ambigua():
    """Stampa un messaggio di errore se la mossa della torre è ambigua."""
    print("Errore, la mossa della torre è ambigua. \
        \nDigita /help per altre informazioni.")

def errore_torre_errore_disambiguazione():
    """Stampa un messaggio di errore se c'è un errore di disambiguazione della torre."""
    print("Errore, la disambiguazione della torre non è corretta. \
        \nDigita /help per altre informazioni.")

def errore_torre_cattura_vuota():
    """Stampa un messaggio d'errore se la torre cerca di catturare una casa vuota."""
    print("Errore, la torre non può catturare una casa vuota. \
        \nDigita /help per altre informazioni.")

def errore_torre_cattura_non_specificata():
    """Stampa un messaggio di errore se la cattura della torre non è specificata."""
    print("Errore, la cattura della torre non è specificata. \
        \nDigita /help per altre informazioni.")
    
# Errori di main.py

def errore_comando_non_riconosciuto():
    """Stampa un messaggio di errore se il comando non è riconosciuto."""
    print("Comando non riconosciuto. \
        Digitare /help per altre informazioni.")

def errore_nessuna_partita_scacchiera():
    """Stampa un messaggio di errore se non c'è una partita in corso."""
    print("Errore, la partita non è iniziata, impossibile mostrare la scacchiera")

def errore_mossa_non_valida():
    """Stampa un messaggio di errore se la mossa non è valida."""
    print("Errore, la mossa non è scritta correttamente. \
        Scrivi /help per altre informazioni.")

# Errori per le mosse

def erroe_mossa_ambigua():
    """Stampa un messaggio di errore se la mossa è ambigua."""
    print("Errore, la mossa è ambigua. \
        Digita /help per altre informazioni.")
    

# Errori per le catture

def errore_cattura_vuota():
    """Stampa un messaggio di errore se si tenta di catturare una casa vuota."""
    print("Errore, la casa è vuota. \
        Digita /help per altre informazioni.")