"""Tests for the Pedone entity."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Pezzi.Donna import Donna
from scacchi.Entity.Pezzi.Pedone import Pedone

# --- Oggetti Mock per simulare le dipendenze ---

class MockScacchiera:
    """Un mock per simulare una scacchiera con pezzi e case configurabili."""

    def __init__(self):
        """Inizializza il mock della scacchiera."""
        self.board = {}
        self.simula = MagicMock(return_value=False)
        self.simula_en_passant = MagicMock(return_value=False)
        self.aggiorna_lista_istanze = MagicMock()
        self.discard_istanze = MagicMock()
        self.filtra_istanze = MagicMock(return_value=[])

    def get_casa(self, riga, colonna):
        """Restituisce o crea una Casa alla posizione data."""
        if (riga, colonna) not in self.board:
            self.board[(riga, colonna)] = Casa(riga, colonna)
        return self.board.get((riga, colonna))
    
    def get_pezzo_scacchiera(self, riga, colonna):
        """Restituisce il pezzo presente su una casa."""
        return self.get_casa(riga, colonna).get_pezzo()
    
    def set_pezzo_scacchiera(self, riga, colonna, pezzo):
        """Imposta un pezzo su una determinata casa."""
        self.get_casa(riga, colonna).set_pezzo(pezzo)


# --- Fixtures di Pytest ---

@pytest.fixture
def pedone_bianco():
    """Restituisce un'istanza di Pedone bianco per i test."""
    return Pedone(0)

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

def test_pedone_init_e_stato_iniziale(pedone_bianco):
    """Testa che l'inizializzazione imposti i valori corretti."""
    assert pedone_bianco.get_colore() == 0
    assert pedone_bianco.get_tipo() == 'P'
    assert pedone_bianco.get_prima_mossa() is True
    assert pedone_bianco.get_en_passant() is False

def test_set_prima_mossa_e_en_passant(pedone_bianco):
    """Testa che i flag di stato vengano impostati correttamente."""
    pedone_bianco.set_prima_mossa()
    pedone_bianco.set_en_passant()
    assert pedone_bianco.get_prima_mossa() is False
    assert pedone_bianco.get_en_passant() is True

@patch.object(Pedone, 'Algebrica_a_Matrice', return_value=(5, 4))
def test_fattibilita_mossa_singola_valida(
    _mock_alg, pedone_bianco, mock_scacchiera, mock_partita
):
    """Testa la fattibilità di una mossa singola valida in avanti."""
    casa_pedone = Casa(6, 4, pedone_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_pedone]
    mock_scacchiera.board[(6, 4)] = casa_pedone
    
    risultato = pedone_bianco.fattibilità("e4", mock_scacchiera, mock_partita)
    
    assert risultato is not None
    assert risultato.get_riga() == 6 and risultato.get_colonna() == 4
    mock_scacchiera.simula.assert_called_once()

@patch.object(Pedone, 'Algebrica_a_Matrice', return_value=(4, 4))
def test_fattibilita_mossa_doppia_valida(
    _mock_alg, pedone_bianco, mock_scacchiera, mock_partita
):
    """Testa la fattibilità di una mossa doppia valida dalla posizione iniziale."""
    casa_pedone = Casa(6, 4, pedone_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_pedone]
    mock_scacchiera.board[(6, 4)] = casa_pedone

    risultato = pedone_bianco.fattibilità("e5", mock_scacchiera, mock_partita)
    
    assert risultato is not None
    assert risultato.get_riga() == 6 and risultato.get_colonna() == 4

@patch.object(Pedone, 'Algebrica_a_Matrice', return_value=(5, 3))
@patch.object(Pedone, 'riga_colonna_disambiguazione', return_value=(None, 4))
def test_fattibilita_cattura_valida(
    _mock_disamb, _mock_alg, pedone_bianco, mock_scacchiera, mock_partita
):
    """Testa la fattibilità di una cattura diagonale valida."""
    casa_pedone = Casa(6, 4, pedone_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_pedone]
    mock_scacchiera.board[(6, 4)] = casa_pedone

    risultato = pedone_bianco.fattibilità("exd4", mock_scacchiera, mock_partita)

    assert risultato is not None
    assert risultato.get_riga() == 6 and risultato.get_colonna() == 4

@patch.object(Pedone, 'Algebrica_a_Matrice', return_value=(4, 4))
@patch.object(Pedone, 'fattibilità')
def test_mossa_doppia_imposta_en_passant(
    mock_fattibilita, _mock_alg, pedone_bianco, mock_scacchiera, mock_partita
):
    """Verifica che una mossa doppia imposti correttamente il flag en_passant."""
    pedone_reale_da_muovere = Pedone(0)
    mock_fattibilita.return_value = Casa(6, 4, pedone_reale_da_muovere)

    pedone_bianco.mossa("e5", mock_scacchiera, mock_partita)
    
    assert pedone_reale_da_muovere.get_en_passant() is True
    mock_partita.cambiaturno.assert_called_once()

@patch('scacchi.Entity.Pezzi.Pedone.errori')
@patch.object(Pedone, 'Algebrica_a_Matrice_promozione', return_value=(0, 4))
@patch.object(Pedone, 'fattibilità')
def test_promozione_pedone_successo(
    mock_fattibilita,
    _mock_alg,
    _mock_errori,
    pedone_bianco,
    mock_scacchiera,
    mock_partita
):
    """Testa una promozione valida a Donna."""
    casa_partenza = Casa(1, 4, pedone_bianco)
    mock_fattibilita.return_value = casa_partenza
    mock_scacchiera.get_casa(0, 4).set_pezzo(None)
    
    pedone_bianco.promozione_pedone("e8D", mock_scacchiera, mock_partita)

    pezzo_promosso = mock_scacchiera.get_casa(0, 4).get_pezzo()
    assert isinstance(pezzo_promosso, Donna)
    assert pezzo_promosso.get_colore() == 0
    assert casa_partenza.get_pezzo() is None
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once_with("e8D", mock_scacchiera)

@patch('scacchi.Entity.Pezzi.Pedone.errori')
@patch.object(Pedone, 'fattibilità')
def test_cattura_en_passant_successo(
    mock_fattibilita, _mock_errori, pedone_bianco, mock_scacchiera, mock_partita
):
    """Testa una cattura en passant valida."""
    casa_partenza_bianco = Casa(3, 4, pedone_bianco)
    mock_fattibilita.return_value = casa_partenza_bianco
    
    pedone_nero_da_catturare = Pedone(1)
    pedone_nero_da_catturare.set_en_passant()
    mock_scacchiera.set_pezzo_scacchiera(3, 3, pedone_nero_da_catturare)

    with patch.object(Pedone, 'Algebrica_a_Matrice', return_value=(2, 3)):
        pedone_bianco.cattura("exd6", mock_scacchiera, mock_partita)

    assert mock_scacchiera.get_pezzo_scacchiera(3, 3) is None
    assert mock_scacchiera.get_casa(2, 3).get_pezzo() == pedone_bianco
    assert mock_scacchiera.get_pezzo_scacchiera(3, 4) is None
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once_with("exd6 e.p.", mock_scacchiera)