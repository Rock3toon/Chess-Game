"""Suite di test per la classe Entity Partita, per garantirne la correttezza."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python per permettere l'import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Partita import Partita  # Importa la classe Partita

# --- Fixtures di Pytest ---

@pytest.fixture
def partita():
    """Restituisce un'istanza pulita di Partita per ogni test."""
    return Partita()

@pytest.fixture
def mock_scacchiera():
    """Restituisce un MagicMock che simula una Scacchiera."""
    return MagicMock()

# --- Test ---

def test_partita_init(partita):
    """Verifica la corretta inizializzazione di un oggetto Partita."""
    assert partita.get_stato_partita() == 1
    assert partita.get_turno() == 0
    assert partita._Partita__lista_mosse == []

def test_cambia_stato_partita(partita):
    """Testa il corretto cambiamento dello stato della partita."""
    assert partita.get_stato_partita() == 1
    partita.cambia_stato_partita()
    assert partita.get_stato_partita() == 0
    partita.cambia_stato_partita()
    assert partita.get_stato_partita() == 1

@patch('scacchi.Entity.Partita.console.print')
def test_cambiaturno(mock_print, partita):
    """Testa il corretto funzionamento del cambio di turno."""
    assert partita.get_turno() == 0
    partita.cambiaturno()
    assert partita.get_turno() == 1
    mock_print.assert_called_once()
    partita.cambiaturno()
    assert partita.get_turno() == 0
    assert mock_print.call_count == 2

def test_aggiungi_mossa_normale(partita, mock_scacchiera):
    """Verifica l'aggiunta di una mossa normale alla lista mosse."""
    mock_re = MagicMock()
    mock_re.sotto_scacco.return_value = False
    mock_scacchiera.filtra_istanze.return_value = [mock_re]
    partita.aggiungi_mossa("e4", mock_scacchiera)
    assert partita._Partita__lista_mosse == ["e4"]

def test_aggiungi_mossa_con_scacco(partita, mock_scacchiera):
    """Verifica che una mossa con scacco aggiunga il simbolo '+'."""
    mock_re = MagicMock()
    mock_re.sotto_scacco.return_value = True
    mock_scacchiera.filtra_istanze.return_value = [mock_re]
    partita.aggiungi_mossa("Nf7", mock_scacchiera)
    assert partita._Partita__lista_mosse == ["Nf7+"]

@patch('scacchi.Entity.Partita.print')
def test_stampa_mosse(mock_print, partita):
    """Testa la corretta stampa della lista delle mosse."""
    partita._Partita__lista_mosse = ["e4", "e5", "Nf3", "Nc6"]
    partita.stampa_mosse()
    assert mock_print.call_count > 2

@patch('scacchi.Entity.Partita.errori.errore_stampa_mosse')
def test_stampa_mosse_vuote(mock_errore, partita):
    """Verifica che venga generato un errore se la lista mosse è vuota."""
    partita.stampa_mosse()
    mock_errore.assert_called_once()

@patch('scacchi.Entity.Partita.cli.partita_in_scacco_matto')
def test_scacco_matto_true(mock_cli_scaccomatto, partita, mock_scacchiera):
    """Testa il corretto riconoscimento di una situazione di scacco matto."""
    partita._Partita__lista_mosse = ["Qf7+"]
    mock_re = MagicMock()
    mock_re.sotto_scacco.return_value = True
    mock_scacchiera.filtra_istanze.return_value = [mock_re]
    with patch.object(partita, 'scaccomatto_evitabile', return_value=False):
        result = partita.scacco_matto(mock_scacchiera)
    assert result is True
    assert partita._Partita__lista_mosse == ["Qf7#"]
    mock_cli_scaccomatto.assert_called_once_with(partita)

def test_scacco_matto_false_no_scacco(partita, mock_scacchiera):
    """Verifica che non venga rilevato scacco matto se non c'è scacco."""
    mock_re = MagicMock()
    mock_re.sotto_scacco.return_value = False
    mock_scacchiera.filtra_istanze.return_value = [mock_re]
    result = partita.scacco_matto(mock_scacchiera)
    assert result is False

@patch('scacchi.Entity.Partita.cli')
@patch('scacchi.Entity.Partita.ui.print_stallo_partita')
def test_stallo_due_re(
    mock_ui_print,
    mock_cli,  # Il mock per il modulo 'cli' viene passato come argomento
    partita, 
    mock_scacchiera):
    """Testa lo stallo per materiale insufficiente (solo i due re)."""
    # Arrange
    # La configurazione dei mock della scacchiera è corretta
    mock_scacchiera.get_istanze.return_value = [MagicMock(), MagicMock()]
    mock_scacchiera.filtra_istanze.return_value = [MagicMock()]

    # Act
    result = partita.stallo(mock_scacchiera)

    # Assert
    assert result is True
    
    # Verifichiamo che la funzione problematica sia stata chiamata
    # Ora che `cli` è un mock, possiamo verificare che `partita_in_stallo` sia chiamata
    mock_cli.partita_in_stallo.assert_called_once_with(partita)

    # In questo scenario, `print_stallo_partita` NON viene chiamato
    # Il codice esce prima, alla riga `cli.partita_in_stallo(self)`.
    # Quindi l'assert corretto è che NON sia stato chiamato.
    mock_ui_print.assert_not_called()

@patch('scacchi.Entity.Partita.ui.print_stallo_partita')
def test_stallo_no_mosse_legali(mock_ui_stallo, partita, mock_scacchiera):
    """Testa lo stallo per assenza di mosse legali senza essere sotto scacco."""
    mock_re = MagicMock()
    mock_re.sotto_scacco.return_value = False
    mock_scacchiera.filtra_istanze.return_value = [mock_re]
    mock_scacchiera.get_istanze.return_value = [1, 2, 3, 4, 5]
    
    with patch.object(partita, 'almeno_una_legale', return_value=False):
        result = partita.stallo(mock_scacchiera)
    
    assert result is True
    mock_ui_stallo.assert_called_once()