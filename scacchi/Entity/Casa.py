class Casa:
    """Classe di tipo <<Entity>> per gestire una singola casella della scacchiera.

    Responsabilità:
        - Memorizzare la posizione (riga, colonna) della casella.
        - Contenere (o meno) il pezzo attualmente presente.
        - Fornire metodi di accesso e modifica del pezzo in essa posizionato.
    """

    def __init__(self, riga, colonna, pezzo=None):
        self._riga = riga
        self._colonna = colonna
        self._pezzo = pezzo  

    def get_pezzo(self):
        return self._pezzo

    def set_pezzo(self, pezzo):
        self._pezzo = pezzo

    def get_riga(self):
        return self._riga
    
    def set_riga(self, riga):
        self._riga = riga

    def get_colonna(self):
        return self._colonna
    
    def set_colonna(self, colonna):
        self._colonna = colonna

    def sotto_scacco(self, scacchiera, partita):
        
        colore_nemico = 0 if partita.get_turno() == 1 else 1
        
        return (
            self.controlla_X(scacchiera, colore_nemico)
            or self.controlla_T(scacchiera, colore_nemico)
            or self.controlla_L(scacchiera, colore_nemico)
        )
          
    def controlla_X(self, scacchiera, colore_nemico):
        # True = minacciata, False = non minacciata
        
        riga = self.get_riga()
        colonna = self.get_colonna()
        
        lista_P = []  
        lista_P = scacchiera.filtra_istanze("P", colore_nemico)

        for pedone in lista_P:
            if colore_nemico == 0:
                if pedone.get_riga() == riga + 1 and (
                    pedone.get_colonna() == colonna - 1
                    or pedone.get_colonna() == colonna + 1
                ):
                    return True
            else:
                if pedone.get_riga() == riga - 1 and (
                    pedone.get_colonna() == colonna - 1
                    or pedone.get_colonna() == colonna + 1
                ):
                    return True

        # Controlla la diagonale in alto a dx
        ramo_bloccato = False 
        flag_re=False               
        while (riga > 0 and colonna < 7) and not ramo_bloccato:
            riga = riga - 1
            colonna = colonna + 1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("A", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore() == colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True     
            flag_re=True
            # Flag utile a fermersi a controllare il re nemico solo alla case adiacenti
        
        # Controlla la diagonale in basso a dx
        riga = self.get_riga()
        colonna = self.get_colonna()
        flag_re=False
        ramo_bloccato = False                
        while (riga < 7 and colonna < 7) and not ramo_bloccato:
            riga = riga + 1
            colonna = colonna + 1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("A", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True
            flag_re=True

        # Controlla la diagonale in basso a sx
        riga = self.get_riga()
        colonna = self.get_colonna()
        ramo_bloccato = False 
        flag_re=False               
        while (riga < 7 and colonna > 0) and not ramo_bloccato:
            riga = riga + 1
            colonna = colonna - 1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("A", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True
            flag_re=True    

        # Controlla la diagonale in alto a sx
        ramo_bloccato = False
        riga = self.get_riga()
        colonna = self.get_colonna()
        flag_re=False
        while (riga > 0 and colonna > 0) and not ramo_bloccato:
            riga = riga - 1
            colonna = colonna - 1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("A", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True
            flag_re=True
        return False

    def controlla_T(self, scacchiera, colore_nemico):
        # True = minacciata, False = non minacciata

    #controllo colonna verso l' alto
        ramo_bloccato=False
        flag_re=False
        riga= self.get_riga()
        colonna = self.get_colonna()
        while riga > 0 and not ramo_bloccato:
            riga = riga - 1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("T", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True
            flag_re=True

    #controllo riga a destra
        ramo_bloccato=False
        riga= self.get_riga()
        colonna = self.get_colonna()
        flag_re=False
        while colonna < 7 and not ramo_bloccato:
            colonna= colonna + 1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("T", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True
            flag_re=True

    #controllo colonna verso il basso
        ramo_bloccato=False
        riga= self.get_riga()
        colonna = self.get_colonna()
        flag_re=False
        while riga < 7 and not ramo_bloccato:
            riga = riga +1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("T", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":      
                    return True
            flag_re=True

    #controllo riga a sinistra        
        ramo_bloccato=False
        riga= self.get_riga()
        colonna = self.get_colonna()
        flag_re=False
        while colonna > 0 and not ramo_bloccato:
            colonna= colonna -1
            if scacchiera.get_pezzo_scacchiera(riga, colonna) is not None:
                ramo_bloccato = True
                if scacchiera.get_pezzo_scacchiera(riga, colonna).get_colore()\
                    == colore_nemico and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() in ("T", "D"):
                        return True
                if not flag_re and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_colore()== colore_nemico\
                    and scacchiera.get_pezzo_scacchiera(riga, colonna)\
                    .get_tipo() == "R":
                    return True
            flag_re=True    
        return False
        

    def controlla_L(self, scacchiera, colore_nemico):
        # True = minacciata, False = non minacciata
        # Posizioni relative del cavallo
        mosse_cavallo = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]

        riga = self.get_riga()
        colonna = self.get_colonna()

        for dr, dc in mosse_cavallo:
            riga_arrivo = riga + dr
            colonna_arrivo = colonna + dc

            # Controlla se è dentro la scacchiera
            if 0 <= riga_arrivo < 8 and 0 <= colonna_arrivo < 8:
                casa_arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
                pezzo_arrivo = casa_arrivo.get_pezzo()
                if pezzo_arrivo is not None and pezzo_arrivo.get_tipo() == 'C' and \
                pezzo_arrivo.get_colore() == colore_nemico:
                    return True

        return False