class Partita:
    """Classe di tipo <<  Entity >>, per la gestione della partita."""
    
    def __init__(self):
        self.__stato_partita = 1  # 0 = in corso, 1 = non in corso
        self.__turno = 0  # 0= turno del bianco, 1 = turno del nero
        self.__lista_mosse = []

    def get_turno(self):
        return self.__turno
    
    def cambiaturno(self):  # passa il turno
        self.__turno = 1 - self.__turno
        if self.__turno == 1:
            print("""
╔════════════════════════════╗
║    ♛  TURNO DEL NERO ♚     ║
╠════════════════════════════╣
║  In attesa della mossa...  ║
╚════════════════════════════╝""")
        else:
            print("""
╔════════════════════════════╗
║    ♕  TURNO DEL BIANCO ♔   ║
╠════════════════════════════╣
║  In attesa della mossa...  ║
╚════════════════════════════╝""")

            


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