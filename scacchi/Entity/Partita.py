from rich.console import Console
from rich.text import Text


console = Console()

class Partita:
    """Classe di tipo << Entity >> per la gestione dello stato di una partita di scacchi.

    Responsabilità:
    - Memorizzare se la partita è in corso o meno.
    - Tenere traccia del turno corrente (0 = bianco, 1 = nero).
    - Registrare le mosse effettuate in ordine.
    - Stampare il cambio di turno all’utente via Rich Console.
    - Fornire accesso controllato a stato e turno tramite metodi getter.
    """
    
    def __init__(self):
        self.__stato_partita = 1  # 0 = in corso, 1 = non in corso
        self.__turno = 0  # 0= turno del bianco, 1 = turno del nero
        self.__lista_mosse = []

    def get_turno(self):
        return self.__turno
    
    def cambiaturno(self):  # passa il turno
        self.__turno = 1 - self.__turno
        if self.__turno == 1:
                text_turno = "TURNO DEL NERO: In attesa della mossa...\n"
                console.print(Text(text_turno, style="italic grey50"), justify="center")
        else:
             text_turno = "TURNO DEL BIANCO: In attesa della mossa...\n"
             console.print(Text(text_turno, style="italic grey50"), justify="center")

            


    def get_stato_partita(self):
        return self.__stato_partita
    
    def cambia_stato_partita(self):                             # cambia lo stato della partita
            self.__stato_partita =1-self.__stato_partita

    def aggiungi_mossa(self, mossa):  
        self.__lista_mosse.append(mossa)  # iniziamo un nuovo turno
    
    def stampa_mosse(self):
        if len(self.__lista_mosse) == 0:
            print("Nessuna mossa effettuata.")
        else:   
            for i in range(len(self.__lista_mosse)):
                if i % 2 == 0:
                    print(f"{(i // 2) + 1}. {self.__lista_mosse[i]} ", end="")
                else:
                    print(f"{self.__lista_mosse[i]} ", end="" "\n")