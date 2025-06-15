from rich.console import Console
from rich.text import Text

import scacchi.Boundary.cli as cli
import scacchi.Boundary.scacchi_ui as ui
import scacchi.Error.errori as errori

console = Console()

class Partita:
    """Classe di tipo << Entity >> per la gestione di una partita di scacchi.

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

    def set_turno(self):
         self.__turno = 0
            
    def get_stato_partita(self):
        return self.__stato_partita
    
    def cambia_stato_partita(self):                             
            # cambia lo stato della partita
            self.__stato_partita =1-self.__stato_partita

    def aggiungi_mossa(self, mossa, scacchiera):
        #colore = 1 if self.get_turno() == 0 else 0 e
        listare = scacchiera.filtra_istanze("R", self.get_turno())
        
        if listare[0].sotto_scacco(scacchiera, self):
            self.__lista_mosse.append(mossa + "+")
        else:
            self.__lista_mosse.append(mossa)
         
        

    
    def stampa_mosse(self):
        if len(self.__lista_mosse) == 0:
            errori.errore_stampa_mosse()
        else:   
            for i in range(len(self.__lista_mosse)):
                if i % 2 == 0:
                    print(f"{(i // 2) + 1}. {self.__lista_mosse[i]} ", end="")
                else:
                    print(f"{self.__lista_mosse[i]} ", end="\n")
            print("\n")  # Aggiunge una riga vuota dopo la stampa delle mosse
    
    def azzera_mosse(self):
        """Azzera la lista delle mosse."""
        self.__lista_mosse = []

    def out_of_bounds(self, riga, colonna):
        return riga < 0 or riga >= 8 or colonna < 0 or colonna >= 8

    def scacco_matto(self, scacchiera):
        lista_re = scacchiera.filtra_istanze("R", self.get_turno())
        for re in lista_re:
            if re.sotto_scacco(scacchiera, self) and \
            not self.scaccomatto_evitabile(scacchiera):
                self.__lista_mosse[-1] = self.__lista_mosse[-1].replace("+", "#")
                cli.partita_in_scacco_matto(self)
                return True
        return False
    
    def stallo(self, scacchiera):
        istanze = scacchiera.get_istanze()
        lista_re = scacchiera.filtra_istanze("R", self.get_turno())
        re = lista_re[0]
        if len(istanze) == 2:
            #sono rimasti due RE
            cli.partita_in_stallo(self)
            return True
        elif len(istanze) == 3:
            for pezzo in istanze:
                if pezzo.get_pezzo().get_tipo() in ("C", "A"):
                    #sono rimasti due Re ed un Cavallo o Alfiere
                    cli.partita_in_stallo(self)
                    return True
        elif len(istanze) == 4:
            lista_A = scacchiera.filtra_istanze_tipo("A")
            if lista_A[0].get_pezzo().get_colore() !=\
                lista_A[1].get_pezzo().get_colore() and\
                (lista_A[0].get_riga() % 2 != lista_A[1].get_riga() % 2):
                #sono rimasti due Re e due Alfiere di colore diverso
                cli.partita_in_stallo(self)
                return True
        elif not re.sotto_scacco(scacchiera, self) and \
            not self.almeno_una_legale(scacchiera): 
                ui.print_stallo_partita()
                return True      
        else:
            return False
    

    def scaccomatto_evitabile(self, scacchiera):
        pedoni = scacchiera.filtra_istanze("P", self.get_turno())
        direzione = -1 if self.get_turno() == 0 else 1 
        colore_nemico = 1 if self.get_turno() == 0 else 0
        for pedone in pedoni:
            # Controllo mossa in avanti di 1
            partenza = pedone
            arrivo = scacchiera.get_casa(pedone.get_riga() + direzione,\
                                        pedone.get_colonna())
            if scacchiera.get_pezzo_scacchiera(arrivo.get_riga(), arrivo.get_colonna())\
                is None and not scacchiera.simula(partenza, arrivo, self):
                return True
            # Controllo mossa in avanti di 2
            if not pedone.get_pezzo().get_prima_mossa() and \
                scacchiera.get_pezzo_scacchiera(pedone.get_riga() + direzione,\
                pedone.get_colonna()) is None:
                    arrivo = scacchiera.get_casa(pedone.get_riga() + direzione * 2, \
                        pedone.get_colonna())
                    if scacchiera.get_pezzo_scacchiera(arrivo.get_riga(), \
                        arrivo.get_colonna()) is None \
                        and not scacchiera.simula(partenza, arrivo, self):
                        return True
            # Controllo cattura
            for dxsx in (-1, 1):
                riga_en_passant = 3 if pedone.get_pezzo().get_colore() == 0 else 4
                if not self.out_of_bounds(pedone.get_riga() + direzione,\
                                        pedone.get_colonna() + dxsx):
                    arrivo = scacchiera.get_casa(pedone.get_riga() + direzione,\
                                                pedone.get_colonna() + dxsx)
                    if arrivo.get_pezzo() is not None:
                        if arrivo.get_pezzo().get_colore() != self.get_turno() and\
                             not scacchiera.simula(partenza, arrivo, self):
                            return True
                    # Controllo en-passant
                    elif pedone.get_riga() == riga_en_passant:
                        pedone_catturato = scacchiera.get_casa(pedone.get_riga(),\
                                        pedone.get_colonna() + dxsx)
                        if pedone_catturato.get_pezzo() is not None:  # noqa: SIM102
                            if pedone_catturato.get_pezzo().get_tipo()\
                            == "P" and pedone_catturato.get_pezzo().get_colore() !=\
                            self.get_turno() and not scacchiera.simula_en_passant\
                            (partenza, arrivo, pedone_catturato, self):
                                return True      
        #Simulazioni cavallo
        cavalli = scacchiera.filtra_istanze("C", self.get_turno()) 
        mosse_cavallo = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2),\
                        (2, -1), (2, 1)]
        for partenza_cavallo in cavalli:
            riga = partenza_cavallo.get_riga()
            colonna = partenza_cavallo.get_colonna()
            for dr, dc in mosse_cavallo:
                riga_arrivo = riga + dr
                colonna_arrivo = colonna + dc
                if not self.out_of_bounds(riga_arrivo, colonna_arrivo):
                    arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
                    if arrivo.get_pezzo() is None:
                        if not scacchiera.simula(partenza_cavallo, arrivo, self):
                            return True
                    elif arrivo.get_pezzo() is not None:  # noqa: SIM102
                        if arrivo.get_pezzo().get_colore() != self.get_turno() and \
                        not scacchiera.simula(partenza_cavallo, arrivo, self):
                            return True
        #Simulazioni Torre - Donna
        torre = scacchiera.filtra_istanze("T", self.get_turno())
        donna = scacchiera.filtra_istanze("D", self.get_turno())
        torre_donna = torre + donna
        mosse_torre = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for partenza_torre in torre_donna:
            riga = partenza_torre.get_riga()
            colonna = partenza_torre.get_colonna()
            for dr, dc in mosse_torre:
                riga_arrivo = riga + dr
                colonna_arrivo = colonna + dc
                ramo_bloccato = False
                while not self.out_of_bounds(riga_arrivo, colonna_arrivo) and\
                not ramo_bloccato:
                    arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
                    if arrivo.get_pezzo() is not None:
                        ramo_bloccato = True
                        if arrivo.get_pezzo().get_colore() == colore_nemico and\
                        not scacchiera.simula(partenza_torre, arrivo, self):
                            return True
                    elif arrivo.get_pezzo() is None and \
                    not scacchiera.simula(partenza_torre, arrivo, self):
                        return True

                    riga_arrivo = riga_arrivo + dr
                    colonna_arrivo = colonna_arrivo + dc
                    
        #Simulazioni Alfiere - Donna
        alfiere = scacchiera.filtra_istanze("A", self.get_turno())
        alfiere_donna = alfiere + donna
        mosse_alfiere = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        for partenza_alfiere in alfiere_donna:
            riga = partenza_alfiere.get_riga()
            colonna = partenza_alfiere.get_colonna()
            for dr, dc in mosse_alfiere:
                riga_arrivo = riga + dr
                colonna_arrivo = colonna + dc
                ramo_bloccato = False
                while not self.out_of_bounds(riga_arrivo, colonna_arrivo) and\
                not ramo_bloccato:
                    arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
                    if arrivo.get_pezzo() is not None:
                        ramo_bloccato = True
                        if arrivo.get_pezzo().get_colore() == colore_nemico and\
                        not scacchiera.simula(partenza_alfiere, arrivo, self):
                            return True
                    elif arrivo.get_pezzo() is None and \
                    not scacchiera.simula(partenza_alfiere, arrivo, self):
                        return True
                    riga_arrivo = riga_arrivo + dr
                    colonna_arrivo = colonna_arrivo + dc
        #Simulazioni Re
        mosse_re = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1),\
                    (0, -1), (-1, -1)]
        for partenza_re in scacchiera.filtra_istanze("R", self.get_turno()):
            riga = partenza_re.get_riga()
            colonna = partenza_re.get_colonna()
            for (dr, dc) in mosse_re:
                riga_arrivo = riga + dr
                colonna_arrivo = colonna + dc
                if not self.out_of_bounds(riga_arrivo, colonna_arrivo):
                    arrivo = scacchiera.get_casa(riga_arrivo, colonna_arrivo)
                    if arrivo.get_pezzo() is not None and\
                    arrivo.get_pezzo().get_colore() != self.get_turno() and \
                        not scacchiera.simula(partenza_re, arrivo, self):  # noqa: SIM114
                        return True
                    elif arrivo.get_pezzo() is None and\
                    not scacchiera.simula(partenza_re, arrivo, self):
                        return True
        #Simulazioni Arrocco
        re_lista = scacchiera.filtra_istanze("R", self.get_turno())
        re = re_lista[0]
        if not re.sotto_scacco(scacchiera, self) and \
        re.get_pezzo().get_prima_mossa():
            
            #Simulazione arrocco corto
            torre_corto = scacchiera.get_casa(re.get_riga(), 7)
            if (torre_corto.get_pezzo() is not None and 
            torre_corto.get_pezzo().get_tipo() == "T" and
            torre_corto.get_pezzo().get_colore() == self.get_turno() and
            not torre_corto.get_pezzo().get_prima_mossa() and \
            scacchiera.get_casa(re.get_riga(), 5).get_pezzo() is not None and\
            scacchiera.get_casa(re.get_riga(), 6).get_pezzo() is not None) and\
            scacchiera.simula_arrocco(re, torre_corto, self):
                return True
            
            #Simulazione arrocco lungo
            torre_lungo = scacchiera.get_casa(re.get_riga(), 0)
            if (torre_lungo.get_pezzo() is not None and 
            torre_lungo.get_pezzo().get_tipo() == "T" and
            torre_lungo.get_pezzo().get_colore() == self.get_turno() and
            not torre_lungo.get_pezzo().get_prima_mossa() and \
            scacchiera.get_casa(re.get_riga(), 1).get_pezzo() is not None and\
            scacchiera.get_casa(re.get_riga(), 2).get_pezzo() is not None and\
            scacchiera.get_casa(re.get_riga(), 3).get_pezzo() is not None) and\
            scacchiera.simula_arrocco(re, torre_lungo, self):
                return True
    
        #se tutti i controlli non arrivano mai a ritornare True    
        return False

    def almeno_una_legale(self, scacchiera):
        return self.scaccomatto_evitabile(scacchiera)