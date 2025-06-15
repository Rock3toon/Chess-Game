"""Tests for the Torre entity."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Pezzi.Torre import Torre

# --- Oggetti Mock per simulare le dipendenze ---

class MockScacchiera:
    """Un mock per simulare una scacchiera con pezzi posizionati a piacimento."""

    def __init__(self, pezzi_posizionati=None):
        """Inizializza il mock della scacchiera."""
        self.board = pezzi_posizionati if pezzi_posizionati is not None else {}
        self.simula = MagicMock(return_value=False)
        self.aggiorna_lista_istanze = MagicMock()
        self.discard_istanze = MagicMock()
        self.set_pezzo_scacchiera = MagicMock()
        self.filtra_istanze = MagicMock(return_value=[])

    def get_casa(self, riga, colonna):
        """Restituisce una Casa alla posizione data."""
        pezzo = self.board.get((riga, colonna))
        return Casa(riga, colonna, pezzo)


# --- Fixtures di Pytest ---

@pytest.fixture
def torre_bianca():
    """Restituisce un'istanza pulita di Torre bianca."""
    return Torre(0)

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

def test_torre_init_e_stato_iniziale(torre_bianca):
    """Testa la corretta inizializzazione e lo stato prima_mossa della Torre."""
    assert torre_bianca.get_colore() == 0
    assert torre_bianca.get_tipo() == 'T'
    assert torre_bianca.get_prima_mossa() is True


def test_set_prima_mossa(torre_bianca):
    """Verifica il corretto funzionamento del metodo set_prima_mossa."""
    torre_bianca.set_prima_mossa()
    assert torre_bianca.get_prima_mossa() is False


def test_movimento_torre_verticale_valido(torre_bianca, mock_scacchiera):
    """Testa che un movimento verticale valido restituisca 1."""
    risultato = torre_bianca.movimento_Torre(0, 4, 0, 0, mock_scacchiera)
    assert risultato == 1


def test_movimento_torre_verticale_bloccato(torre_bianca):
    """Testa che un pezzo intermedio blocchi il movimento verticale."""
    scacchiera_bloccata = MockScacchiera({(2, 0): MagicMock()})
    risultato = torre_bianca.movimento_Torre(0, 4, 0, 0, scacchiera_bloccata)
    assert risultato == 0


def test_movimento_torre_diagonale_invalido(torre_bianca, mock_scacchiera):
    """Testa che un movimento diagonale venga correttamente invalidato."""
    risultato = torre_bianca.movimento_Torre(0, 2, 0, 2, mock_scacchiera)
    assert risultato == 0


@patch.object(Torre, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch.object(Torre, 'riga_colonna_disambiguazione', return_value=(None, None))
@patch('scacchi.Entity.Pezzi.Torre.errori')
def test_fattibilita_successo_una_torre(
    mock_errori, _mock_disamb, _mock_alg, torre_bianca, mock_partita
):
    """Testa che una mossa valida e non ambigua superi la fattibilità."""
    scacchiera = MockScacchiera()
    casa_partenza_valida = Casa(0, 3, torre_bianca)
    scacchiera.filtra_istanze.return_value = [casa_partenza_valida]
    
    risultato = torre_bianca.fattibilità("Td4", scacchiera, mock_partita)
    
    assert risultato == casa_partenza_valida
    scacchiera.simula.assert_called_once()
    mock_errori.assert_not_called()


@patch.object(Torre, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch('scacchi.Entity.Pezzi.Torre.errori')
def test_fattibilita_fallimento_mossa_illegale(
    mock_errori, _mock_alg, torre_bianca, mock_partita
):
    """Testa che una mossa non valida fallisca il controllo di fattibilità."""
    scacchiera = MockScacchiera()
    scacchiera.filtra_istanze.return_value = []
    
    risultato = torre_bianca.fattibilità("Td4", scacchiera, mock_partita)
    
    assert risultato == -1
    mock_errori.errore_torre_mossa_illegale.assert_called_once()


@patch.object(Torre, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch.object(Torre, 'fattibilità')
def test_mossa_successo(
    mock_fattibilita, _mock_alg, torre_bianca, mock_scacchiera, mock_partita
):
    """Testa l'esecuzione di una mossa valida su una casa vuota."""
    mock_fattibilita.return_value = Casa(0, 3, MagicMock())
    mock_scacchiera.get_casa(3, 3).set_pezzo(None)
    
    torre_bianca.mossa("Td4", mock_scacchiera, mock_partita)
    
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    assert mock_scacchiera.set_pezzo_scacchiera.call_count == 2
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once()


@patch.object(Torre, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch.object(Torre, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Torre.errori')
def test_mossa_fallimento_bersaglio_amico(
    mock_errori,mock_fattibilita, _mock_alg, torre_bianca, mock_scacchiera, mock_partita
):
    """Testa che una mossa su un pezzo amico generi un errore."""
    mock_pezzo_in_movimento = MagicMock()
    mock_pezzo_in_movimento.get_colore.return_value = 0
    mock_fattibilita.return_value = Casa(0, 3, mock_pezzo_in_movimento)
    
    pezzo_amico_sul_bersaglio = MagicMock()
    pezzo_amico_sul_bersaglio.get_colore.return_value = 0
    mock_scacchiera.board[(3, 3)] = pezzo_amico_sul_bersaglio
    
    torre_bianca.mossa("Td4", mock_scacchiera, mock_partita)
    
    mock_errori.errore_torre_mossa_illegale.assert_called_once()
    mock_partita.cambiaturno.assert_not_called()


@patch.object(Torre, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch.object(Torre, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Torre.errori')
def test_cattura_successo(
    mock_errori,
    mock_fattibilita,
    _mock_alg,
    torre_bianca,
    mock_scacchiera,
    mock_partita
):
    """Testa l'esecuzione di una cattura valida."""
    mock_pezzo_in_movimento = MagicMock()
    mock_pezzo_in_movimento.get_colore.return_value = 0
    mock_fattibilita.return_value = Casa(0, 3, mock_pezzo_in_movimento)
    
    pezzo_nemico = MagicMock()
    pezzo_nemico.get_colore.return_value = 1
    mock_scacchiera.board[(3, 3)] = pezzo_nemico

    torre_bianca.cattura("Txd4", mock_scacchiera, mock_partita)
    
    mock_scacchiera.discard_istanze.assert_called_once()
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_partita.cambiaturno.assert_called_once()
    mock_errori.assert_not_called()


@patch.object(Torre, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch.object(Torre, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Torre.errori')
def test_cattura_fallimento_bersaglio_vuoto(
    mock_errori,
    mock_fattibilita,
    _mock_alg,
    torre_bianca,
    mock_scacchiera,
    mock_partita
):
    """Testa che una cattura su una casa vuota generi un errore."""
    mock_fattibilita.return_value = Casa(0, 3, torre_bianca)
    mock_scacchiera.get_casa(3, 3).set_pezzo(None)
    
    torre_bianca.cattura("Txd4", mock_scacchiera, mock_partita)
    
    mock_errori.errore_torre_cattura_vuota.assert_called_once()
    mock_partita.cambiaturno.assert_not_called()