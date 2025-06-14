"""Suite di test per la classe Entity Donna, per garantirne la correttezza."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Pezzi.Donna import Donna

# --- Oggetti Mock per simulare le dipendenze ---

class MockScacchiera:
    """Un mock per simulare una scacchiera per i test."""

    def __init__(self, pezzi_posizionati=None):
        """Inizializza il mock della scacchiera con pezzi pre-posizionati."""
        self._pezzi = pezzi_posizionati if pezzi_posizionati is not None else {}
        self.simula = MagicMock(return_value=False)
        self.aggiorna_lista_istanze = MagicMock()
        self.discard_istanze = MagicMock()
        self.set_pezzo_scacchiera = MagicMock()
        self.filtra_istanze = MagicMock(return_value=[])

    def get_casa(self, riga, colonna):
        """Restituisce una Casa alla posizione data."""
        pezzo = self._pezzi.get((riga, colonna))
        return Casa(riga, colonna, pezzo)

    def get_pezzo_scacchiera(self, riga, colonna):
        """Restituisce il pezzo alla posizione data."""
        return self.get_casa(riga, colonna).get_pezzo()


# --- Fixtures di Pytest ---

@pytest.fixture
def donna_bianca():
    """Restituisce un'istanza di Donna bianca per i test."""
    return Donna(0)

@pytest.fixture
def mock_partita():
    """Restituisce un mock generico di una Partita."""
    partita = MagicMock()
    partita.get_turno.return_value = 0
    return partita

@pytest.fixture
def mock_scacchiera():
    """Restituisce un'istanza del MockScacchiera per i test."""
    return MockScacchiera()

# --- Test ---

def test_donna_init(donna_bianca):
    """Testa la corretta inizializzazione di un oggetto Donna."""
    assert donna_bianca.get_colore() == 0
    assert donna_bianca.get_tipo() == 'D'

@pytest.mark.parametrize(
    ("r_partenza", "c_partenza", "r_arrivo", "c_arrivo", "atteso"),
    [
        (3, 3, 0, 3, 1),  # Verticale
        (3, 3, 3, 7, 1),  # Orizzontale
        (3, 3, 0, 0, 1),  # Diagonale
        (3, 3, 5, 5, 1),  # Diagonale
        (3, 3, 4, 5, 0)   # Non valido (mossa da cavallo)
    ]
)
def test_movimento_donna(
    r_partenza, c_partenza, r_arrivo, c_arrivo, atteso, donna_bianca, mock_scacchiera
):
    """Testa la logica di movimento base della donna."""
    risultato = donna_bianca.movimento_Donna(
        r_partenza, r_arrivo, c_partenza, c_arrivo, mock_scacchiera
    )
    assert risultato == atteso

def test_movimento_donna_diagonale_bloccato(donna_bianca):
    """Testa che il movimento della donna sia bloccato da un pezzo intermedio."""
    scacchiera_bloccata = MockScacchiera({(2, 2): MagicMock()})
    risultato = donna_bianca.movimento_Donna(0, 4, 0, 4, scacchiera_bloccata)
    assert risultato == 0

@patch.object(Donna, 'Algebrica_a_Matrice', return_value=(3, 6))
@patch.object(Donna, 'riga_colonna_disambiguazione', return_value=(None, None))
@patch('scacchi.Entity.Pezzi.Donna.errori')
def test_fattibilita_successo_una_donna(
    mock_errori, _mock_disamb, _mock_alg, donna_bianca, mock_scacchiera, mock_partita
):
    """Testa la fattibilità di una mossa valida e non ambigua."""
    casa_partenza_valida = Casa(0, 3, donna_bianca)
    mock_scacchiera.filtra_istanze.return_value = [casa_partenza_valida]
    
    risultato = donna_bianca.fattibilità("Dg5", mock_scacchiera, mock_partita)

    assert isinstance(risultato, Casa)
    assert risultato.get_riga() == 0 and risultato.get_colonna() == 3
    mock_scacchiera.simula.assert_called_once()
    mock_errori.assert_not_called()

@patch.object(Donna, 'Algebrica_a_Matrice', return_value=(3, 4))
@patch('scacchi.Entity.Pezzi.Donna.errori')
def test_fattibilita_fallimento_mossa_illegale(
    mock_errori, _mock_alg, donna_bianca, mock_scacchiera, mock_partita
):
    """Testa che una mossa non valida fallisca il controllo di fattibilità."""
    risultato = donna_bianca.fattibilità("De4", mock_scacchiera, mock_partita)
    assert risultato == -1
    mock_errori.errore_donna_mossa_illegale.assert_called_once()

@patch.object(Donna, 'Algebrica_a_Matrice', return_value=(3, 4))
@patch.object(Donna, 'fattibilità')
def test_mossa_successo(
    mock_fattibilita, _mock_alg, donna_bianca, mock_scacchiera, mock_partita
):
    """Testa l'esecuzione corretta di una mossa."""
    mock_pezzo_in_movimento = MagicMock()
    mock_fattibilita.return_value = Casa(0, 3, mock_pezzo_in_movimento)
    donna_bianca.mossa("De4", mock_scacchiera, mock_partita)
    
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_scacchiera.set_pezzo_scacchiera.assert_any_call(3, 4, mock_pezzo_in_movimento)
    mock_scacchiera.set_pezzo_scacchiera.assert_any_call(0, 3, None)
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once()

@patch.object(Donna, 'Algebrica_a_Matrice', return_value=(3, 4))
@patch.object(Donna, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Donna.errori')
def test_mossa_fallimento_cattura_non_specificata(
    mock_errori,
    mock_fattibilita,
    _mock_alg,
    donna_bianca,
    mock_scacchiera,
    mock_partita
):
    """Testa che una mossa su casa occupata senza 'x' generi un errore."""
    mock_pezzo_in_movimento = MagicMock()
    mock_fattibilita.return_value = Casa(0, 3, mock_pezzo_in_movimento)
    mock_scacchiera._pezzi[(3, 4)] = MagicMock() # Casa di arrivo occupata
    
    donna_bianca.mossa("De4", mock_scacchiera, mock_partita)
    
    mock_errori.errore_donna_cattura_non_specificata.assert_called_once()
    mock_partita.cambiaturno.assert_not_called()

@patch.object(Donna, 'Algebrica_a_Matrice', return_value=(3, 4))
@patch.object(Donna, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Donna.errori')
def test_cattura_successo(
    mock_errori,
    mock_fattibilita,
    _mock_alg,
    donna_bianca,
    mock_scacchiera,
    mock_partita
):
    """Testa l'esecuzione corretta di una cattura."""
    mock_pezzo_in_movimento = MagicMock()
    mock_fattibilita.return_value = Casa(0, 3, mock_pezzo_in_movimento)
    mock_scacchiera._pezzi[(3, 4)] = MagicMock() # Pezzo nemico da catturare

    donna_bianca.cattura("Dxe4", mock_scacchiera, mock_partita)
    
    mock_scacchiera.discard_istanze.assert_called_once()
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_partita.cambiaturno.assert_called_once()
    mock_errori.assert_not_called()