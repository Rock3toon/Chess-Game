from rich.console import Console
from rich.style import Style
from rich.text import Text

from scacchi.Entity.Casa import Casa

# Utilizziamo Rich per gestire i colori e il centraggio
console = Console(force_terminal=True, color_system="truecolor")

class Scacchiera:
    """Classe di tipo << Entity >> per gestire la scacchiera come una matrice 8×8.

    Responsabilità:
      - Inizializzare una matrice di oggetti Casa per ogni coordinata (riga, colonna).
      - Fornire metodi di accesso e modifica alle caselle e ai pezzi in esse contenuti.
      - Convertire i pezzi nel loro simbolo Unicode corrispondente.
      - Stampare la scacchiera formattata con colori alternati per le caselle
    """

    def __init__(self):
        self.__matrice = []  
        self._istanze = [] # Lista delle case dei presenti sulla scacchiera
        for riga in range(8):  # inizializza la matrice 8x8
            riga_corrente = []
            for colonna in range(8):
                casa = Casa(riga, colonna)
                riga_corrente.append(casa)
            self.__matrice.append(riga_corrente)

    def get_matrice(self):
        return self.__matrice

    def get_casa(self, riga, colonna):  # recupera una casa
        return self.__matrice[riga][colonna]

    def set_pezzo_scacchiera(self, riga, colonna, pezzo=None):
        self.__matrice[riga][colonna].set_pezzo(pezzo)

    def get_pezzo_scacchiera(self, riga, colonna):  # recupera il pezzo\        
        return self.__matrice[riga][colonna].get_pezzo()

    def set_casa(self, riga, colonna, pezzo):  # ricostruisce la casa con pezzo
        self.__matrice[riga][colonna] = Casa(riga, colonna, pezzo)

    def get_istanze(self):
        """Restituisce la lista dei pezzi presenti sulla scacchiera."""
        return self._istanze
    
    def set_istanze(self, pezzo):
        self._istanze.append(pezzo)

    def discard_istanze(self, pezzo):
        """Rimuove un pezzo dalla lista delle istanza."""
        self._istanze.remove(pezzo)

    def inizializza_istanze(self):      
        #popola la lista delle istanze con i pezzi iniziali
        for riga in [0, 1, 6, 7]:
            for colonna in range(8):
                pezzo = self.get_casa(riga, colonna)
                self.set_istanze(pezzo)
    
    def azzera_istanze(self):
        """Azzera la lista delle istanze."""
        self._istanze = []
    
    def filtra_istanze(self, tipo_pezzo, colore):
        #Tipi di pezzi: 'P' = Pedone, 'T' = Torre, 'C' = Cavallo,
        #               'A' = Alfiere, 'D' = Donna, 'R' = Re
        #Colore: 0 = Bianco, 1 = Nero
        """Restituisce una lista di pezzi dello stesso tipo e colore."""
        lista_pezzi_colore = []
        # Lista che contiene le case che contengono i pezzi giusti
        for istanza in self.get_istanze():
            pezzo = istanza.get_pezzo()
            if pezzo is not None and pezzo.get_tipo() ==\
                tipo_pezzo and pezzo.get_colore() == colore:
                lista_pezzi_colore.append(istanza)
                # Aggiunge l'istanza di casa che contine il pezzo alla lista
        return lista_pezzi_colore
    
    def filtra_istanze_tipo(self, tipo_pezzo):
        """Restituisce una lista di pezzi dello stesso tipo."""
        lista_tipo = []
        # Lista che contiene le case che contengono i pezzi giusti
        for istanza in self.get_istanze():
            pezzo = istanza.get_pezzo()
            if pezzo is not None and pezzo.get_tipo() == tipo_pezzo:
                lista_tipo.append(istanza)
                # Aggiunge l'istanza di casa che contine il pezzo alla lista
        return lista_tipo
    
    def aggiorna_lista_istanze(self, casa_partenza, casa_destinazione):
        """Aggiorna la lista delle istanze."""
        # Rimuove l'istanza della casa di partenza
        self.discard_istanze(casa_partenza)
        # Aggiunge l'istanza della casa di destinazione
        self.set_istanze(casa_destinazione)


    def converti_pezzo_unicode(self, pezzo):
        simboli = {
            'P': ("♙", "♟"),
            'T': ("♖", "♜"),
            'C': ("♘", "♞"),
            'A': ("♗", "♝"),
            'D': ("♕", "♛"),
            'R': ("♔", "♚")
        }
        tipo = pezzo.get_tipo()
        colore = pezzo.get_colore()
        return simboli[tipo][0] if colore == 0 else simboli[tipo][1]

    def stampa_scacchiera(self, scacchi):
        # Stili per caselle chiare e scure
        dark_sq = Style(bgcolor="#DEB887", color="white")   # burlywood
        light_sq = Style(bgcolor="#FFFFE0", color="black")  # light yellow

        # Intestazione colonne con spazi di padding (3 caratteri ciascuna)
        lettere_colonne = " a  b  c  d  e  f  g  h "
        console.print(Text(lettere_colonne), justify="center")

        for i in range(8):
            numero_riga = 8 - i
            cells = []
            # Numero di riga a inizio (3 caratteri)
            cells.append(Text(f"{numero_riga}  "))
            for j in range(8):
                casa = scacchi.get_casa(i, j)
                pezzo = casa.get_pezzo()
                style = light_sq if (i + j) % 2 == 0 else dark_sq

                if isinstance(pezzo, str):
                    simbolo = pezzo
                elif pezzo:
                    simbolo = scacchi.converti_pezzo_unicode(pezzo)
                else:
                    simbolo = " "

                # Ogni casella occupa 3 spazi con padding
                cells.append(Text(f" {simbolo} ", style=style))

            # Numero di riga a fine
            cells.append(Text(f"  {numero_riga}"))
            # Stampiamo la riga con sep="" per mantenere il padding
            console.print(*cells, sep="", justify="center")

        # Piè di pagina colonne identico all'intestazione
        console.print(Text(lettere_colonne), justify="center")

    def simula(self, casa_partenza, casa_arrivo, partita):
        """Simula il movimento di un pezzo sulla scacchiera."""
        salva_pezzo = casa_arrivo.get_pezzo()
        if salva_pezzo is None:
            # Simula movimento
            self.aggiorna_lista_istanze(casa_partenza, casa_arrivo)
            self.set_pezzo_scacchiera(casa_arrivo.get_riga(), \
                                casa_arrivo.get_colonna(), casa_partenza.get_pezzo())
            self.set_pezzo_scacchiera(casa_partenza.get_riga(), \
                                    casa_partenza.get_colonna(), None)
        elif salva_pezzo is not None:
            # Simula cattura
            self.discard_istanze(casa_partenza)
            self.set_pezzo_scacchiera(casa_arrivo.get_riga(),\
                                casa_arrivo.get_colonna(), casa_partenza.get_pezzo())
            self.set_pezzo_scacchiera(casa_partenza.get_riga(), \
                                    casa_partenza.get_colonna(), None)
        for re in self.filtra_istanze("R", partita.get_turno()):
            #Controllo lo scacco
            f = re.sotto_scacco(self, partita)
        # Ripristina stato precedente
        self.set_pezzo_scacchiera(casa_partenza.get_riga(), \
                                casa_partenza.get_colonna(), casa_arrivo.get_pezzo())
        self.set_pezzo_scacchiera(casa_arrivo.get_riga(), \
                                casa_arrivo.get_colonna(), salva_pezzo)
        self.set_istanze(casa_partenza)
        if casa_arrivo.get_pezzo() is None:
            self.discard_istanze(casa_arrivo)

        # True se causa scacco, False altrimenti
        return f
    
    def simula_en_passant(self, casa_partenza, casa_arrivo,\
                    cattura_aggiuntiva, partita):
        """Simula il movimento di un pezzo sulla scacchiera e cattura aggiuntiva."""
        salva_pezzo = cattura_aggiuntiva.get_pezzo()
        # Simula movimento
        self.discard_istanze(cattura_aggiuntiva)
        self.aggiorna_lista_istanze(casa_partenza, casa_arrivo)
        self.set_pezzo_scacchiera(casa_arrivo.get_riga(), \
                casa_arrivo.get_colonna(), casa_partenza.get_pezzo())
        self.set_pezzo_scacchiera(casa_partenza.get_riga(), \
                casa_partenza.get_colonna(), None)
        self.set_pezzo_scacchiera(cattura_aggiuntiva.get_riga(), \
                cattura_aggiuntiva.get_colonna(), None)
        for re in self.filtra_istanze("R", partita.get_turno()):
            #Controllo lo scacco
            f = re.sotto_scacco(self, partita)
        # Ripristina stato precedente
        self.set_pezzo_scacchiera(casa_partenza.get_riga(), \
                casa_partenza.get_colonna(), casa_arrivo.get_pezzo())
        self.set_pezzo_scacchiera(casa_arrivo.get_riga(), \
                casa_arrivo.get_colonna(), None)
        self.set_pezzo_scacchiera(cattura_aggiuntiva.get_riga(), \
                cattura_aggiuntiva.get_colonna(), salva_pezzo)
        self.set_istanze(cattura_aggiuntiva)
        self.set_istanze(casa_partenza)
        self.discard_istanze(casa_arrivo)

        # True se causa scacco, False altrimenti
        return f
    
    def simula_arrocco(self, casa_re, casa_torre, partita):
        """Simula l'arrocco sulla scacchiera."""
        # Determina il tipo di arrocco in base alla posizione della torre
        riga_re = casa_re.get_riga()
        colonna_torre = casa_torre.get_colonna()
        
        if colonna_torre == 0 and \
        not self.get_casa(riga_re, 2).sotto_scacco(self, partita) and\
        not self.get_casa(riga_re, 3).sotto_scacco(self, partita):
            casa_re_arrivo = self.get_casa(riga_re, 2)
            casa_torre_arrivo = self.get_casa(riga_re, 3)
        elif colonna_torre == 7 and \
        not self.get_casa(riga_re, 6).sotto_scacco(self, partita) and\
        not self.get_casa(riga_re, 5).sotto_scacco(self, partita):
            casa_re_arrivo = self.get_casa(riga_re, 6)
            casa_torre_arrivo = self.get_casa(riga_re, 5)
        
        # Simula movimento del re
        self.aggiorna_lista_istanze(casa_re, casa_re_arrivo)
        self.set_pezzo_scacchiera(casa_re_arrivo.get_riga(), 
                                casa_re_arrivo.get_colonna(), casa_re.get_pezzo())
        self.set_pezzo_scacchiera(casa_re.get_riga(), 
                                casa_re.get_colonna(), None)
        
        # Simula movimento della torre
        self.aggiorna_lista_istanze(casa_torre, casa_torre_arrivo)
        self.set_pezzo_scacchiera(casa_torre_arrivo.get_riga(), 
                                casa_torre_arrivo.get_colonna(), casa_torre.get_pezzo())
        self.set_pezzo_scacchiera(casa_torre.get_riga(), 
                                casa_torre.get_colonna(), None)
        
        # Controlla se il re è sotto scacco dopo l'arrocco
        for re in self.filtra_istanze("R", partita.get_turno()):
            f = re.sotto_scacco(self, partita)
        
        # Ripristina stato precedente
        # Ripristina il re
        self.set_pezzo_scacchiera(casa_re.get_riga(), 
                                casa_re.get_colonna(), casa_re_arrivo.get_pezzo())
        self.set_pezzo_scacchiera(casa_re_arrivo.get_riga(), 
                                casa_re_arrivo.get_colonna(), None)
        
        # Ripristina la torre
        self.set_pezzo_scacchiera(casa_torre.get_riga(), 
                                casa_torre.get_colonna(), casa_torre_arrivo.get_pezzo())
        self.set_pezzo_scacchiera(casa_torre_arrivo.get_riga(), 
                                casa_torre_arrivo.get_colonna(), None)
        
        # Ripristina le istanze
        self.set_istanze(casa_re)
        self.set_istanze(casa_torre)
        self.discard_istanze(casa_re_arrivo)
        self.discard_istanze(casa_torre_arrivo)
        
        # True se causa scacco, False altrimenti
        return f