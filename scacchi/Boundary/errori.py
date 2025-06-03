#Errori di cli.py

def errore_gioca():
    """Stampa un messaggio di errore se la partita è già in corso."""
    print("Errore: la partita è già iniziata. \
         Procedi con una mossa o digita /help per altre informazioni.")


def errore_risposta():
    """Stampa un messaggio di errore se la risposta non è valida."""
    print("Risposta non valida! Riprova")

def errore_nessuna_partita_abbandona():
    """Stampa un messaggio di errore se non c'è una partita da abbandonare."""
    print("Errore, nessuna partita in corso, impossibile abbandonare la partita.  \
        Usa /help per altre informazioni.")
    
def errore_nessuna_partita_patta():
    """Stampa un messaggio di errore se non c'è una partita da richiedere la patta."""
    print("Errore, nessuna partita in corso, impossibile richiedere la patta. \
        Usa /help per altre informazioni.")



#errori GestoreMosse.py

def errore_nessuna_partita():
    """Stampa un messaggio di errore se non c'è una partita in corso."""
    print("Errore, nessuna partita in corso. \
         Scrivi /gioca per avviare una partita.")


#errori di partita.py


def errore_stampa_mosse():
    """Stampa un messaggio di errore se non ci sono mosse da stampare."""
    print("Errore, nessuna mossa effettuata.")




#errori di Pedone.py




def errore_mossa_pedone():
    """Stampa un messaggio di errore se la mossa del pedone non è valida."""
    print("Errore, la mossa non è valida. Il pedone non può muoversi in quella \
        casella. Digita /help per altre informazioni.")





#errori di main.py




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

#errori per le mosse



def errore_mossa_illegale():
    """Stampa un messaggio di errore se la mossa è illegale."""
    print("Errore, la mossa è illegale. \
         Digita /help per altre informazioni.")


def erroe_mossa_ambigua():
    """Stampa un messaggio di errore se la mossa è ambigua."""
    print("Errore, la mossa è ambigua. \
         Digita /help per altre informazioni.")
    
def errore_cattura_vuota():
    """Stampa un messaggio di errore se si tenta di catturare una casa vuota."""
    print("Errore, la casa è vuota. \
         Digita /help per altre informazioni.")