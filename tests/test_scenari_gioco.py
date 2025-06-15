"""Suite di test per scenari di gioco."""

import os
import sys

import pytest

# Aggiungi la root del progetto al path di Python per permettere l'import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importiamo i componenti REALI che vogliamo testare insieme
from scacchi.Boundary import cli
from scacchi.Control.GestoreMosse import GestioneInput
from scacchi.Entity.Partita import Partita
from scacchi.Entity.Scacchiera import Scacchiera


@pytest.fixture
def setup_partita_reale():
    """Inizializza una partita pronta per essere giocata."""
    scacchiera = Scacchiera()
    partita = Partita()
    # Usiamo la funzione `gioca` per popolare la scacchiera e avviare la partita,
    # simulando il comando /gioca dell'utente. Questa funzione NON solleva SystemExit.
    cli.gioca(scacchiera, partita)
    return scacchiera, partita


# --- TEST DI INTEGRAZIONE ---

def test_integrazione_mossa_e_cambio_turno(setup_partita_reale):
    """Funzione di test per verificare mossa, turno e scacchiera."""
    # OBIETTIVO: Verificare che GestioneInput (Control) interagisca correttamente
    #            con Scacchiera e Partita (Entity) per eseguire una mossa e cambiare 
    #            turno.
    scacchiera, partita = setup_partita_reale

    # Arrange: Lo stato iniziale è Turno BIANCO (0)
    assert partita.get_turno() == 0
    assert scacchiera.get_pezzo_scacchiera(6, 4) is not None # Pedone bianco in e2
    assert scacchiera.get_pezzo_scacchiera(4, 4) is None     # Casa e4 vuota

    # Act: Eseguiamo una mossa valida tramite il nostro gestore
    GestioneInput("e4", scacchiera, partita)

    # Assert: Verifichiamo lo stato del sistema DOPO l'interazione
    assert partita.get_turno() == 1
    assert "e4" in partita._Partita__lista_mosse
    assert scacchiera.get_pezzo_scacchiera(6, 4) is None
    pezzo_mosso = scacchiera.get_pezzo_scacchiera(4, 4)
    assert pezzo_mosso is not None
    assert pezzo_mosso.get_tipo() == 'P'


# --- TEST DI SISTEMA / ACCETTAZIONE ---

def test_accettazione_scaccomatto_del_barbiere(setup_partita_reale):
    """Funzione di test per verificare lo scacco matto del barbiere."""
    # OBIETTIVO: Verificare che il sistema gestisca correttamente uno scenario di 
    #            scacco matto, terminando e resettando la partita come da design.
    scacchiera, partita = setup_partita_reale

    # Arrange: Definiamo la sequenza di mosse per lo "scacco matto del barbiere"
    mosse_preparatorie = [
        "e4",    # Bianco
        "e5",    # Nero
        "Ac4",   # Bianco
        "Ac5",   # Nero
        "Dh5",   # Bianco
        "Cf6",   # Nero
    ]
    mossa_di_matto = "Dxf7"   # Bianco -> Scacco Matto

    # Act 1: Eseguiamo le mosse che preparano lo scenario
    for mossa in mosse_preparatorie:
        GestioneInput(mossa, scacchiera, partita)

    # Assert 1: Verifichiamo lo stato del sistema PRIMA della mossa finale
    assert partita.get_stato_partita() == 0  # La partita è ancora in corso
    assert len(partita._Partita__lista_mosse) == 6

    # Act 2: Eseguiamo la mossa finale che causa lo scacco matto
    GestioneInput(mossa_di_matto, scacchiera, partita)

    # Assert 2: Verifichiamo lo stato finale del sistema DOPO lo scacco matto
    # Il sistema, come da sua logica, ha rilevato il matto e resettato la partita.
    # Quindi la lista delle mosse deve essere vuota e lo stato partita "terminato".
    assert len(partita._Partita__lista_mosse) == 0
    assert partita.get_stato_partita() == 1 # La partita è finita


def test_sistema_arrocco_illegale_re_sotto_scacco(setup_partita_reale):
    """Funzione test per verificare l'arrocco illegale quando il re è sotto scacco."""
    # OBIETTIVO: Verificare che il sistema impedisca una mossa complessa (arrocco)
    #            quando le condizioni di gioco non lo permettono (Re sotto scacco),
    #            testando l'interazione tra Re, Scacchiera e le regole di minaccia.
    scacchiera, partita = setup_partita_reale

    # Arrange: Creiamo uno scenario in cui il Bianco vuole arroccare, ma è sotto scacco.
    mosse_preparatorie = [
        "e4", "e5",
        "Cf3", "Cc6",
        "d4", "exd4",
        "Ae2", "Ab4" # L'alfiere nero in b4 mette il re bianco sotto scacco
    ]
    for mossa in mosse_preparatorie:
        GestioneInput(mossa, scacchiera, partita)

    # Verifichiamo che il re sia effettivamente sotto scacco prima del tentativo
    re_bianco_casa = scacchiera.filtra_istanze('R', 0)[0]
    assert re_bianco_casa.sotto_scacco(scacchiera, partita) is True
    
    turno_prima_mossa_illegale = partita.get_turno()

    # Act: Tentiamo di eseguire l'arrocco (mossa illegale in questa situazione)
    GestioneInput("0-0", scacchiera, partita)

    # Assert:
    assert partita.get_turno() == turno_prima_mossa_illegale
    assert "0-0" not in partita._Partita__lista_mosse
    assert scacchiera.get_pezzo_scacchiera(7, 4).get_tipo() == 'R'
    assert scacchiera.get_pezzo_scacchiera(7, 7).get_tipo() == 'T'
    assert scacchiera.get_pezzo_scacchiera(7, 6) is None
    assert scacchiera.get_pezzo_scacchiera(7, 5) is None