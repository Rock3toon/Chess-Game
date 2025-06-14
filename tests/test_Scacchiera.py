"""Tests for the Scacchiera entity."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python per permettere l'import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Scacchiera import Scacchiera

# --- Oggetti Mock per simulare le dipendenze ---

class MockPezzo:
    """Un semplice mock per simulare un pezzo."""

    def __init__(self, tipo, colore):
        """Inizializza il mock con tipo e colore."""
        self._tipo = tipo
        self._colore = colore

    def get_tipo(self):
        """Restituisce il tipo del pezzo."""
        return self._tipo

    def get_colore(self):
        """Restituisce il colore del pezzo."""
        return self._colore


class MockPartita:
    """Un semplice mock per simulare una partita."""

    def get_turno(self):
        """Restituisce il turno di gioco (sempre del bianco per i test)."""
        return 0


# --- Fixtures di Pytest ---

@pytest.fixture
def scacchiera():
    """Restituisce un'istanza pulita di Scacchiera per ogni test."""
    return Scacchiera()


@pytest.fixture
def mock_partita():
    """Restituisce un'istanza del mock di Partita."""
    return MockPartita()


# --- Test ---

def test_scacchiera_init(scacchiera):
    """Testa l'inizializzazione corretta della matrice 8x8 di Casa."""
    matrice = scacchiera.get_matrice()
    assert len(matrice) == 8
    assert all(len(riga) == 8 for riga in matrice)
    assert isinstance(matrice[0][0], Casa)
    assert matrice[3][4].get_riga() == 3
    assert matrice[3][4].get_colonna() == 4
    assert matrice[7][7].get_pezzo() is None


def test_get_set_pezzo(scacchiera):
    """Testa l'impostazione e il recupero di un pezzo da una casa."""
    mock_pezzo = MockPezzo('P', 0)
    assert scacchiera.get_pezzo_scacchiera(4, 4) is None
    scacchiera.set_pezzo_scacchiera(4, 4, mock_pezzo)
    pezzo_recuperato = scacchiera.get_pezzo_scacchiera(4, 4)
    assert pezzo_recuperato == mock_pezzo


def test_gestione_istanze(scacchiera):
    """Testa l'aggiunta, la rimozione e l'azzeramento delle istanze."""
    casa1 = scacchiera.get_casa(0, 0)
    casa2 = scacchiera.get_casa(1, 1)
    assert scacchiera.get_istanze() == []
    
    scacchiera.set_istanze(casa1)
    scacchiera.set_istanze(casa2)
    assert scacchiera.get_istanze() == [casa1, casa2]

    scacchiera.discard_istanze(casa1)
    assert scacchiera.get_istanze() == [casa2]

    scacchiera.azzera_istanze()
    assert scacchiera.get_istanze() == []


def test_filtra_istanze(scacchiera):
    """Testa la logica di filtraggio dei pezzi per tipo e colore."""
    pedone_bianco = MockPezzo('P', 0)
    torre_nera = MockPezzo('T', 1)
    re_bianco = MockPezzo('R', 0)
    
    scacchiera.set_pezzo_scacchiera(1, 0, pedone_bianco)
    scacchiera.set_pezzo_scacchiera(3, 3, torre_nera)
    scacchiera.set_pezzo_scacchiera(7, 4, re_bianco)

    scacchiera.set_istanze(scacchiera.get_casa(1, 0))
    scacchiera.set_istanze(scacchiera.get_casa(3, 3))
    scacchiera.set_istanze(scacchiera.get_casa(7, 4))
    
    lista_re_bianchi = scacchiera.filtra_istanze('R', 0)
    assert len(lista_re_bianchi) == 1
    assert lista_re_bianchi[0].get_pezzo() == re_bianco

    lista_tutti_i_pezzi_p = scacchiera.filtra_istanze_tipo('P')
    assert len(lista_tutti_i_pezzi_p) == 1
    assert lista_tutti_i_pezzi_p[0].get_pezzo() == pedone_bianco


def test_converti_pezzo_unicode(scacchiera):
    """Testa la conversione di un pezzo nel suo simbolo Unicode."""
    re_bianco = MockPezzo('R', 0)
    regina_nera = MockPezzo('D', 1)
    assert scacchiera.converti_pezzo_unicode(re_bianco) == "♔"
    assert scacchiera.converti_pezzo_unicode(regina_nera) == "♛"


@patch('scacchi.Entity.Scacchiera.console.print')
def test_stampa_scacchiera(mock_print, scacchiera):
    """Verifica che stampa_scacchiera chiami print il numero corretto di volte."""
    scacchiera.stampa_scacchiera(scacchiera)
    assert mock_print.call_count == 10


def test_simula_restores_state_after_move(scacchiera, mock_partita):
    """Verifica che simula() ripristini lo stato originale della scacchiera."""
    pedone = MockPezzo('P', 0)
    casa_partenza = scacchiera.get_casa(6, 4)
    casa_arrivo = scacchiera.get_casa(4, 4)
    scacchiera.set_pezzo_scacchiera(6, 4, pedone)
    scacchiera.set_istanze(casa_partenza)

    re_mock = MagicMock()
    re_mock.sotto_scacco.return_value = False
    
    with patch.object(scacchiera, 'filtra_istanze', return_value=[re_mock]):
        scacchiera.simula(casa_partenza, casa_arrivo, mock_partita)

    assert scacchiera.get_pezzo_scacchiera(6, 4) == pedone
    assert scacchiera.get_pezzo_scacchiera(4, 4) is None
    assert casa_partenza in scacchiera.get_istanze()
    assert casa_arrivo not in scacchiera.get_istanze()