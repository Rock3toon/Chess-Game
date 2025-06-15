"""Suite di test per la classe Entity Cavallo, per garantirne la correttezza."""


import os
import sys
from unittest.mock import MagicMock, call, patch

import pytest

# Aggiungi la root del progetto al path di Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.Entity.Casa import Casa
from scacchi.Entity.Pezzi.Cavallo import Cavallo

# --- Oggetti Mock per simulare le dipendenze ---

class MockScacchiera:
    """Un mock per simulare una scacchiera, crea oggetti Casa al volo."""
    
    def __init__(self, pezzi_posizionati=None):
        self._pezzi = pezzi_posizionati if pezzi_posizionati else {}
        self.simula = MagicMock(return_value=False)
        self.aggiorna_lista_istanze = MagicMock()
        self.discard_istanze = MagicMock()
        self.set_pezzo_scacchiera = MagicMock()
        self.filtra_istanze = MagicMock(return_value=[])

    def get_casa(self, riga, colonna):
        pezzo = self._pezzi.get((riga, colonna))
        return Casa(riga, colonna, pezzo)

    def get_pezzo_scacchiera(self, riga, colonna):
        return self.get_casa(riga, colonna).get_pezzo()


# --- Fixtures di Pytest ---

@pytest.fixture
def cavallo_bianco():
    """Restituisce un'istanza di Cavallo bianco per i test."""
    return Cavallo(0)

@pytest.fixture
def mock_partita():
    """Restituisce un mock di una Partita."""
    partita = MagicMock()
    partita.get_turno.return_value = 0
    return partita

@pytest.fixture
def mock_scacchiera():
    """Restituisce un'istanza del nostro MockScacchiera."""
    return MockScacchiera()

# --- Test ---

def test_cavallo_init(cavallo_bianco):
    """Testa la corretta inizializzazione di un oggetto Cavallo."""
    assert cavallo_bianco.get_colore() == 0
    assert cavallo_bianco.get_tipo() == 'C'

@pytest.mark.parametrize("dr, dc, atteso", [
    (1, 2, 1), (-1, 2, 1), (1, -2, 1), (-1, -2, 1),
    (2, 1, 1), (-2, 1, 1), (2, -1, 1), (-2, -1, 1),
    (1, 1, False), (2, 2, False), (0, 1, False)
])
def test_movimento_cavallo(dr, dc, atteso, cavallo_bianco):
    """Testa la logica di movimento base del cavallo (a 'L')."""
    r_partenza, c_partenza = 3, 3
    r_arrivo, c_arrivo = r_partenza + dr, c_partenza + dc
    risultato = cavallo_bianco.movimento_cavallo(
        r_partenza, r_arrivo, c_partenza, c_arrivo
    )
    assert risultato == atteso

@patch.object(Cavallo, 'Algebrica_a_Matrice', return_value=(2, 5))
@patch.object(Cavallo, 'riga_colonna_disambiguazione', return_value=(None, None))
@patch('scacchi.Entity.Pezzi.Cavallo.errori')
def test_fattibilita_successo_un_cavallo(
    mock_errori,
    _mock_disamb,
    _mock_alg,
    cavallo_bianco,
    mock_scacchiera,
    mock_partita
):
    """Testa che una mossa valida e non ambigua superi il controllo di fattibilità."""
    casa_partenza_valida = Casa(0, 6, cavallo_bianco)
    mock_scacchiera.filtra_istanze.return_value = [casa_partenza_valida]
    risultato = cavallo_bianco.fattibilità("Cf3", mock_scacchiera, mock_partita)
    assert isinstance(risultato, Casa)
    assert risultato.get_riga() == 0 and risultato.get_colonna() == 6
    mock_scacchiera.simula.assert_called_once()
    mock_errori.assert_not_called()

@patch.object(Cavallo, 'Algebrica_a_Matrice', return_value=(3, 3))
@patch('scacchi.Entity.Pezzi.Cavallo.errori')
def test_fattibilita_fallimento_mossa_ambigua(
    mock_errori,
    _mock_alg,
    cavallo_bianco,
    mock_scacchiera,
    mock_partita
):
    """Testa che una mossa ambigua generi un errore."""
    cavallo1 = Casa(0, 6, cavallo_bianco)
    cavallo2 = Casa(2, 6, cavallo_bianco)
    mock_scacchiera.filtra_istanze.return_value = [cavallo1, cavallo2]
    with patch.object(Cavallo, 'movimento_cavallo', return_value=1):
        risultato = cavallo_bianco.fattibilità("Ce5", mock_scacchiera, mock_partita)
    assert risultato == -1
    mock_errori.errore_cavallo_mossa_ambigua.assert_called_once()

@patch.object(Cavallo, 'Algebrica_a_Matrice', return_value=(2, 5))
@patch.object(Cavallo, 'fattibilità')
def test_mossa_successo(
    mock_fattibilita,
    _mock_alg,
    cavallo_bianco,
    mock_scacchiera,
    mock_partita
):
    """Testa l'esecuzione corretta di una mossa e verifica aggiornamento stato."""
    mock_pezzo_in_movimento = MagicMock()
    mock_fattibilita.return_value = Casa(0, 6, mock_pezzo_in_movimento)
    cavallo_bianco.mossa("Cf3", mock_scacchiera, mock_partita)
    mock_scacchiera.aggiorna_lista_istanze.assert_called_once()
    mock_scacchiera.set_pezzo_scacchiera.assert_any_call(2, 5, mock_pezzo_in_movimento)
    mock_scacchiera.set_pezzo_scacchiera.assert_any_call(0, 6, None)
    mock_partita.cambiaturno.assert_called_once()
    mock_partita.aggiungi_mossa.assert_called_once()

@patch.object(Cavallo, 'Algebrica_a_Matrice', return_value=(2, 5))
@patch.object(Cavallo, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Cavallo.errori')
def test_cattura_successo(
    mock_errori,
    mock_fattibilita,
    mock_alg,
    mock_scacchiera,  # Questa è la tua istanza di MockScacchiera
    mock_partita):
    """Testa l'esecuzione di una cattura valida."""
    # Arrange
    cavallo_bianco = Cavallo(0)

    mock_pezzo_in_movimento = MagicMock()
    mock_pezzo_in_movimento.get_colore.return_value = 0
    casa_partenza = Casa(0, 6, mock_pezzo_in_movimento)
    
    pezzo_nemico = MagicMock()
    pezzo_nemico.get_colore.return_value = 1
    casa_arrivo = Casa(2, 5, pezzo_nemico)

    mock_fattibilita.return_value = casa_partenza
    
    # Usiamo patch.object per sostituire temporaneamente il metodo get_casa 
    # dell'ISTANZA mock_scacchiera con un MagicMock che possiamo configurare.
    with patch.object(mock_scacchiera, 'get_casa') as mock_get_casa:
        
        # Ora mock_get_casa è un vero MagicMock e possiamo assegnargli un side_effect
        def get_casa_side_effect(riga, colonna):
            if riga == 2 and colonna == 5:
                return casa_arrivo
            if riga == 0 and colonna == 6:
                return casa_partenza
            return MagicMock() 
        mock_get_casa.side_effect = get_casa_side_effect

        # Act
        # L'azione e gli assert devono avvenire DENTRO il blocco 'with'
        # in modo che la patch sia attiva.
        cavallo_bianco.cattura("Cxf3", mock_scacchiera, mock_partita)

        # Assert
        mock_scacchiera.discard_istanze.assert_called_once_with(casa_partenza)

        expected_calls = [
            call(2, 5, casa_partenza.get_pezzo()),
            call(0, 6, None)
        ]
        mock_scacchiera.set_pezzo_scacchiera.assert_has_calls(
            expected_calls,
            any_order=True
        )

        mock_scacchiera.aggiorna_lista_istanze.assert_not_called()
        
        mock_partita.cambiaturno.assert_called_once()
        mock_errori.errore_cavallo_cattura_vuota.assert_not_called()
        mock_errori.errore_cavallo_mossa_illegale.assert_not_called()
    

@patch.object(Cavallo, 'Algebrica_a_Matrice', return_value=(2, 5))
@patch.object(Cavallo, 'fattibilità')
@patch('scacchi.Entity.Pezzi.Cavallo.errori')
def test_cattura_fallimento_casa_vuota(
    mock_errori,
    mock_fattibilita,
    mock_alg, cavallo_bianco,
    mock_scacchiera, mock_partita):
    """Testa che una cattura su una casa vuota generi un errore."""
    mock_pezzo_in_movimento = MagicMock()
    mock_pezzo_in_movimento.get_colore.return_value = 0
    mock_fattibilita.return_value = Casa(0, 6, mock_pezzo_in_movimento)
    cavallo_bianco.cattura("Cxf3", mock_scacchiera, mock_partita)
    mock_errori.errore_cavallo_cattura_vuota.assert_called_once()
    mock_partita.cambiaturno.assert_not_called()