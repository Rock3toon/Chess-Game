"""Suite di test per la classe Entity Afliere, per garantirne la correttezza."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Pezzi.Alfiere import Alfiere

# --- Oggetti Mock per simulare le dipendenze ---

class MockScacchiera:
    """Un mock per simulare una scacchiera, crea oggetti Casa al volo."""

    def __init__(self, pezzi_posizionati=None):
        """Inizializza la scacchiera fittizia con pezzi specifici."""        
        self._pezzi = pezzi_posizionati if pezzi_posizionati else {}
        self.simula = MagicMock(return_value=False)
        self.aggiorna_lista_istanze = MagicMock()
        self.discard_istanze = MagicMock()
        self.set_pezzo_scacchiera = MagicMock()
        self.filtra_istanze = MagicMock(return_value=[])

    def get_casa(self, riga, colonna):
        """Restituisce un oggetto Casa per le coordinate date, con o senza pezzo."""
        pezzo = self._pezzi.get((riga, colonna))
        return Casa(riga, colonna, pezzo)

    def get_pezzo_scacchiera(self, riga, colonna):
        """Restituisce il pezzo presente in una data casa della scacchiera."""
        return self.get_casa(riga, colonna).get_pezzo()


# --- Fixtures di Pytest ---

@pytest.fixture
def alfiere_bianco():
    """Fixture per fornire un'istanza di Alfiere bianco (colore 0) per i test."""
    return Alfiere(0)

@pytest.fixture
def mock_partita():
    """Fixture per fornire un mock di una Partita con turno impostato al giocatore 0."""
    partita = MagicMock()
    partita.get_turno.return_value = 0
    return partita

@pytest.fixture
def mock_scacchiera():
    """Fixture per fornire un mock pulito di una Scacchiera per ogni test."""
    return MockScacchiera()

# --- Test ---

def test_alfiere_init(alfiere_bianco):
    """Verifica che un Alfiere sia inizializzato correttamente colore e tipo."""
    assert alfiere_bianco.get_colore() == 0
    assert alfiere_bianco.get_tipo() == 'A'

@pytest.mark.parametrize("r_arrivo, c_arrivo, atteso", [
    (5, 5, 1), (1, 1, 1), (1, 5, 1), (5, 1, 1), # Movimenti diagonali validi
    (3, 4, False), (4, 3, False), (5, 4, False) # Movimenti non diagonali
])
def test_movimento_alfiere(
    r_arrivo: int,
    c_arrivo: int,
    atteso: bool,
    alfiere_bianco: 'Alfiere',
    mock_scacchiera: 'MockScacchiera',
):
    """Testa la logica di movimento dell'alfiere."""
    r_partenza, c_partenza = 3, 3

    # Chiama il metodo da testare
    risultato = alfiere_bianco.movimento_alfiere(
        r_partenza, r_arrivo, c_partenza, c_arrivo, mock_scacchiera
    )

    # Verifica che il risultato sia quello atteso
    assert risultato == atteso

def test_movimento_alfiere_bloccato(alfiere_bianco):
    """Verifica che il movimento alfiere fallisca se un pezzo ostruisce il percorso."""
    scacchiera_bloccata = MockScacchiera({(2, 2): MagicMock()}) # Un pezzo in (2,2)
    risultato = alfiere_bianco.movimento_alfiere(0, 4, 0, 4, scacchiera_bloccata)
    assert risultato is False

@patch.object(Alfiere, 'Algebrica_a_Matrice', return_value=(4, 5)) # Arrivo a f4
@patch.object(Alfiere, 'riga_colonna_disambiguazione', return_value=(None, None))
@patch('scacchi.Entity.Pezzi.Alfiere.errori')
def test_fattibilita_successo_un_alfiere(
    mock_errori,
    mock_disamb,
    mock_alg,
    alfiere_bianco,
    mock_scacchiera,
    mock_partita
):
    """Testa il caso di successo di fattibilità() con un solo alfiere."""
    # Arrange: Alfiere in c1 (7, 2) si muove a f4 (4, 5). Mossa valida.
    casa_partenza_valida = Casa(7, 2, alfiere_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_partenza_valida]
    
    risultato = alfiere_bianco.fattibilità("Af4", mock_scacchiera, mock_partita)

    assert isinstance(risultato, Casa)
    assert risultato.get_riga() == 7 and risultato.get_colonna() == 2
    mock_scacchiera.simula.assert_called_once()
    mock_errori.assert_not_called()

@patch.object(Alfiere, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch('scacchi.Entity.Pezzi.Alfiere.errori')
def test_fattibilita_fallimento_mossa_illegale(
    mock_errori,
    mock_alg,
    alfiere_bianco,
    mock_scacchiera,
    mock_partita):
    """Verifica che fattibilità() fallisca e chiami un errore se mossa non fattibile."""
    risultato = alfiere_bianco.fattibilità("Ad4", mock_scacchiera, mock_partita)
    assert risultato == -1
    mock_errori.errore_alfiere_mossa_illegale.assert_called_once()


@patch.object(Alfiere, 'Algebrica_a_Matrice', return_value=(2, 2))
@patch.object(Alfiere, 'fattibilità')
def test_mossa_successo(
    mock_fattibilita,
    mock_alg, alfiere_bianco,
    mock_scacchiera,
    mock_partita
):
    """Testa il metodo mossa(), verificando aggiornamento scacchiera e partita."""
    mock_pezzo_in_movimento = MagicMock()
    mock_fattibilita.return_value = Casa(0, 0, mock_pezzo_in_movimento)
    alfiere_bianco.mossa("Ac3", mock_scacchiera, mock_partita)
    
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_scacchiera.set_pezzo_scacchiera.assert_any_call(2, 2, mock_pezzo_in_movimento)
    mock_scacchiera.set_pezzo_scacchiera.assert_any_call(0, 0, None)
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once()

@patch.object(Alfiere, 'Algebrica_a_Matrice', return_value=(2, 2))
@patch.object(Alfiere, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Alfiere.errori')
def test_cattura_successo(
    mock_errori,
    mock_fattibilita,
    mock_alg,
    alfiere_bianco,
    mock_scacchiera,
    mock_partita):
    """Testa l'esecuzione di una cattura valida verificando pezzi e stato di gioco."""
    mock_pezzo_in_movimento = MagicMock()
    mock_pezzo_in_movimento.get_colore.return_value = 0
    casa_partenza = Casa(0, 0, mock_pezzo_in_movimento)
    mock_fattibilita.return_value = casa_partenza

    pezzo_nemico = MagicMock()
    pezzo_nemico.get_colore.return_value = 1
    mock_scacchiera._pezzi[(2, 2)] = pezzo_nemico
    
    alfiere_bianco.cattura("Axc3", mock_scacchiera, mock_partita)
    
    mock_scacchiera.discard_istanze.assert_called_once()
    call_args = mock_scacchiera.discard_istanze.call_args[0]
    casa_catturata = call_args[0]
    assert isinstance(casa_catturata, Casa)
    assert casa_catturata.get_riga() == 2
    assert casa_catturata.get_colonna() == 2
    
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_partita.cambiaturno.assert_called_once()
    mock_errori.assert_not_called()