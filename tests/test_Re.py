"""Tests for the Re entity."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Pezzi.Re import Re

# --- Oggetti Mock per simulare le dipendenze ---

class MockPezzo:
    """Un semplice mock per simulare un pezzo con stato."""

    def __init__(self, tipo, colore, prima_mossa=True):
        """Inizializza il mock con tipo, colore e stato prima mossa."""
        self._tipo = tipo
        self._colore = colore
        self._prima_mossa = prima_mossa

    def get_tipo(self):
        """Restituisce il tipo del pezzo."""
        return self._tipo

    def get_colore(self):
        """Restituisce il colore del pezzo."""
        return self._colore

    def get_prima_mossa(self):
        """Restituisce se il pezzo è alla sua prima mossa."""
        return self._prima_mossa

    def set_prima_mossa(self):
        """Imposta lo stato del pezzo a non essere più alla prima mossa."""
        self._prima_mossa = False


class MockScacchiera:
    """Un mock per simulare una scacchiera con pezzi e case configurabili."""

    def __init__(self):
        """Inizializza il mock della scacchiera."""
        self.case = {}
        self.simula = MagicMock(return_value=False)
        self.aggiorna_lista_istanze = MagicMock()
        self.discard_istanze = MagicMock()
        self.filtra_istanze = MagicMock(return_value=[])

    def get_casa(self, riga, colonna):
        """Restituisce o crea una Casa alla posizione data."""
        if (riga, colonna) not in self.case:
            self.case[(riga, colonna)] = Casa(riga, colonna)
        return self.case[(riga, colonna)]
    
    def set_pezzo_scacchiera(self, riga, colonna, pezzo):
        """Simula l'impostazione di un pezzo, aggiornando lo stato interno."""
        self.get_casa(riga, colonna).set_pezzo(pezzo)
    
    def get_pezzo_scacchiera(self, riga, colonna):
        """Restituisce il pezzo presente su una casa."""
        return self.get_casa(riga, colonna).get_pezzo()


# --- Fixtures di Pytest ---

@pytest.fixture
def re_bianco():
    """Restituisce un'istanza pulita di Re bianco."""
    return Re(0)

@pytest.fixture
def mock_partita():
    """Restituisce un MagicMock che simula una Partita."""
    partita = MagicMock()
    partita.get_turno.return_value = 0
    return partita

@pytest.fixture
def mock_scacchiera():
    """Restituisce un'istanza del MockScacchiera per i test."""
    return MockScacchiera()

# --- Test ---

def test_re_init_e_prima_mossa(re_bianco):
    """Testa l'inizializzazione e lo stato prima_mossa del Re."""
    assert re_bianco.get_colore() == 0
    assert re_bianco.get_tipo() == 'R'
    assert re_bianco.get_prima_mossa() is True
    re_bianco.set_prima_mossa()
    assert re_bianco.get_prima_mossa() is False

def test_fattibilita_mossa_valida(re_bianco, mock_scacchiera, mock_partita):
    """Testa che una mossa valida superi il controllo di fattibilità."""
    casa_re = Casa(4, 4, re_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_re]
    with patch.object(Re, 'Algebrica_a_Matrice', return_value=(3, 4)):
        risultato = re_bianco.fattibilità("Re5", mock_scacchiera, mock_partita)
    assert risultato == casa_re

def test_fattibilita_mossa_invalida(re_bianco, mock_scacchiera, mock_partita):
    """Testa che una mossa non valida fallisca il controllo di fattibilità."""
    casa_re = Casa(4, 4, re_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_re]
    with patch.object(Re, 'Algebrica_a_Matrice', return_value=(2, 4)):
        risultato = re_bianco.fattibilità("Re6", mock_scacchiera, mock_partita)
    assert risultato == -1

@patch.object(Re, 'Algebrica_a_Matrice', return_value=(3, 4))
@patch.object(Re, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Re.errori')
def test_mossa_successo(
    mock_errori, mock_fattibilita, _mock_alg, re_bianco, mock_scacchiera, mock_partita
):
    """Testa l'esecuzione corretta di una mossa valida."""
    casa_partenza = Casa(4, 4, re_bianco)
    mock_fattibilita.return_value = casa_partenza
    casa_arrivo = mock_scacchiera.get_casa(3, 4)
    casa_arrivo.sotto_scacco = MagicMock(return_value=False)
    
    re_bianco.mossa("Re5", mock_scacchiera, mock_partita)
    
    assert re_bianco.get_prima_mossa() is False
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_partita.cambiaturno.assert_called_once()
    mock_errori.assert_not_called()

@patch.object(Re, 'Algebrica_a_Matrice', return_value=(3, 4))
@patch.object(Re, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Re.errori')
def test_mossa_fallimento_sotto_scacco(
    mock_errori, mock_fattibilita, _mock_alg, re_bianco, mock_scacchiera, mock_partita
):
    """Testa che una mossa in una casa sotto scacco generi un errore."""
    mock_fattibilita.return_value = Casa(4, 4, re_bianco)
    casa_arrivo = mock_scacchiera.get_casa(3, 4)
    casa_arrivo.sotto_scacco = MagicMock(return_value=True)
    
    re_bianco.mossa("Re5", mock_scacchiera, mock_partita)
    
    mock_errori.errore_re_mossa_sotto_scacco.assert_called_once()
    mock_partita.cambiaturno.assert_not_called()

@patch('scacchi.Entity.Pezzi.Re.errori')
def test_arrocco_corto_successo(mock_errori, mock_scacchiera, mock_partita):
    """Testa l'esecuzione corretta di un arrocco corto valido."""
    re_bianco_reale = Re(0)
    torre_bianca_reale = MockPezzo('T', 0, prima_mossa=True)
    mock_scacchiera.set_pezzo_scacchiera(7, 4, re_bianco_reale)
    mock_scacchiera.set_pezzo_scacchiera(7, 7, torre_bianca_reale)

    casa_re = mock_scacchiera.get_casa(7, 4)
    casa_re.sotto_scacco = MagicMock(return_value=False)
    mock_scacchiera.get_casa(7, 5).sotto_scacco = MagicMock(return_value=False)
    mock_scacchiera.get_casa(7, 6).sotto_scacco = MagicMock(return_value=False)
    mock_scacchiera.filtra_istanze.return_value = [casa_re]

    re_bianco_reale.arrocco("0-0", mock_scacchiera, mock_partita)
    
    assert mock_scacchiera.get_pezzo_scacchiera(7, 6) == re_bianco_reale
    assert mock_scacchiera.get_pezzo_scacchiera(7, 5) == torre_bianca_reale
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once_with("0-0", mock_scacchiera)
    mock_errori.assert_not_called()

@patch('scacchi.Entity.Pezzi.Re.errori')
def test_arrocco_percorso_bloccato(mock_errori, mock_scacchiera, mock_partita):
    """Testa che l'arrocco fallisca se il percorso non è libero."""
    re_bianco_reale = Re(0)
    torre_bianca_reale = MockPezzo('T', 0, prima_mossa=True)
    mock_scacchiera.set_pezzo_scacchiera(7, 4, re_bianco_reale)
    mock_scacchiera.set_pezzo_scacchiera(7, 7, torre_bianca_reale)
    mock_scacchiera.set_pezzo_scacchiera(7, 5, MagicMock())
    
    casa_re = mock_scacchiera.get_casa(7, 4)
    casa_re.sotto_scacco = MagicMock(return_value=False)
    mock_scacchiera.filtra_istanze.return_value = [casa_re]

    re_bianco_reale.arrocco("0-0", mock_scacchiera, mock_partita)

    mock_errori.errore_arrocco_illegale.assert_called_once()
    mock_partita.cambiaturno.assert_not_called()