class Partita:
    """Classe di tipo <<  Entity >>, per la gestione della partita."""
    
    def __init__(self):
        self.__stato_partita = 1  # 0 = in corso, 1 = non in corso
        self.__turno = 0  # 0= turno del bianco, 1 = turno del nero

    def get_turno(self):
        return self.__turno
    
    def cambiaturno(self):                  # passa il turno
        self.__turno = 1 - self.__turno 

    def get_stato_partita(self):
        return self.__stato_partita
    

    def cambia_stato_partita(self):                             # cambia lo stato della partita
            self.__stato_partita =1-self.__stato_partita
