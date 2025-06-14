"""Tests for the Casa entity."""

import os
import sys
from unittest.mock import MagicMock, patch  # <-- MODIFICA: Aggiunto 'patch' all'import

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa

# --- Oggetti Mock per simulare le dipendenze ---

class MockPezzo:
    """Un semplice mock per simulare un pezzo."""

    def __init__(self, tipo, colore):
        self._tipo = tipo
        self._colore = colore

    def get_tipo(self):
        return self._tipo

    def get_colore(self):
        return self._colore

class MockScacchiera:
    """Un mock per simulare una scacchiera con pezzi posizionati a piacimento."""

    def __init__(self, pezzi_posizionati=None):
        # pezzi_posizionati è un dizionario {(riga, colonna): MockPezzo}
        self.board = pezzi_posizionati if pezzi_posizionati else {}

    def get_pezzo_scacchiera(self, riga, colonna):
        return self.board.get((riga, colonna))

    def get_casa(self, riga, colonna):
        # Per controlla_L, che chiama get_casa
        casa = Casa(riga, colonna, self.get_pezzo_scacchiera(riga, colonna))
        return casa

# --- Test ---

def test_casa_init_e_getters():
    """Testa l'inizializzazione e i metodi getter di base."""
    pezzo_bianco = MockPezzo('P', 0)
    casa = Casa(3, 4, pezzo_bianco)

    assert casa.get_riga() == 3
    assert casa.get_colonna() == 4
    assert casa.get_pezzo() == pezzo_bianco

def test_casa_setters():
    """Testa i metodi setter di base."""
    casa = Casa(0, 0)
    pezzo_nero = MockPezzo('T', 1)

    casa.set_riga(5)
    casa.set_colonna(6)
    casa.set_pezzo(pezzo_nero)

    assert casa.get_riga() == 5
    assert casa.get_colonna() == 6
    assert casa.get_pezzo().get_tipo() == 'T'

# --- Test sulla logica di controllo minacce ---

@pytest.fixture
def mock_partita():
    """Fixture che simula una partita."""
    partita = MagicMock()
    # Per controlla_L, che usa out_of_bounds
    partita.out_of_bounds.side_effect = lambda r, c: not (0 <= r < 8 and 0 <= c < 8)
    return partita

def test_controlla_L_minacciata(mock_partita):
    """Testa che la casa sia correttamente rilevata come minacciata da un cavallo."""
    # Arrange: Cavallo nero in (2, 2) minaccia la casa (4, 3)
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({(2, 2): MockPezzo('C', 1)}) # Colore nemico: 1 (nero)

    # Act
    minacciata = casa_da_controllare.controlla_L(scacchiera, 1, mock_partita)

    # Assert
    assert minacciata is True

def test_controlla_L_non_minacciata(mock_partita):
    """Testa che la casa non sia minacciata se non ci sono cavalli nelle vicinanze."""
    # Arrange: Nessun pezzo minaccioso
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({(2, 2): MockPezzo('P', 1)}) 
        # Un pedone non minaccia a L

    # Act
    minacciata = casa_da_controllare.controlla_L(scacchiera, 1, mock_partita)

    # Assert
    assert minacciata is False

def test_controlla_T_minacciata_da_torre(mock_partita):
    """Testa una minaccia verticale da una Torre."""
    # Arrange: Torre nera in (0, 3) minaccia la casa (4, 3)
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({(0, 3): MockPezzo('T', 1)}) # Colore nemico: 1 (nero)
    
    # Act
    minacciata = casa_da_controllare.controlla_T(scacchiera, 1, mock_partita)

    # Assert
    assert minacciata is True

def test_controlla_T_bloccata(mock_partita):
    """Testa che la minaccia sia bloccata da un altro pezzo."""
    # Arrange: Torre nera in (0, 3), pezzo amico in (2, 3), casa (4, 3)
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({
        (0, 3): MockPezzo('T', 1),
        (2, 3): MockPezzo('P', 0) # Pezzo amico che blocca
    })
    
    # Act
    minacciata = casa_da_controllare.controlla_T(scacchiera, 1, mock_partita)

    # Assert
    assert minacciata is False

def test_controlla_X_minacciata_da_alfiere(mock_partita):
    """Testa una minaccia diagonale da un Alfiere."""
    # Arrange: Alfiere nero in (2, 1) minaccia la casa (4, 3)
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({(2, 1): MockPezzo('A', 1)})
    
    # Act
    minacciata = casa_da_controllare.controlla_X(scacchiera, 1, mock_partita)

    # Assert
    assert minacciata is True

def test_controlla_X_minacciata_da_pedone(mock_partita):
    """Testa una minaccia diagonale da un Pedone."""
    # Arrange: Pedone nero in (3, 2) minaccia la casa (4, 3)
    # Assumiamo che il pedone nero si muova verso il basso
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({(3, 2): MockPezzo('P', 1)})
    
    # Act
    minacciata = casa_da_controllare.controlla_X(scacchiera, 1, mock_partita)
    
    # Assert
    assert minacciata is True

def test_controlla_X_non_minacciata_da_pedone_distante(mock_partita):
    """Verifica che un pedone non minacci diagonalmente a distanza > 1."""
    # Arrange: Pedone nero in (2, 1) NON minaccia la casa (4, 3)
    casa_da_controllare = Casa(4, 3)
    scacchiera = MockScacchiera({(2, 1): MockPezzo('P', 1)})
    
    # Act
    minacciata = casa_da_controllare.controlla_X(scacchiera, 1, mock_partita)

    # Assert
    assert minacciata is False

@patch('scacchi.Entity.Casa.Casa.controlla_X', return_value=False)
@patch('scacchi.Entity.Casa.Casa.controlla_T', return_value=True) # <-- Minaccia qui
@patch('scacchi.Entity.Casa.Casa.controlla_L', return_value=False)
def test_sotto_scacco_usa_or_logico(mock_L, mock_T, mock_X, mock_partita):
    """Testa che sotto_scacco combini correttamente i risultati e si fermi presto."""
    casa = Casa(3, 3)
    scacchiera = MockScacchiera()
    
    # Il turno del bianco (0), quindi colore nemico è 1
    mock_partita.get_turno.return_value = 0
    
    # Act
    risultato = casa.sotto_scacco(scacchiera, mock_partita)

    # Assert
    assert risultato is True
    # Verifica che i controlli vengano chiamati nell'ordine corretto
    mock_X.assert_called_once()
    mock_T.assert_called_once()
    # Verifica che controlla_L non venga chiamato
    mock_L.assert_not_called()