"""Suite di test per il modulo GestioneInput."""

import unittest
from unittest.mock import Mock, patch

from scacchi.Control.GestoreMosse import GestioneInput

PATH_TO_MODULE = 'scacchi.Control.GestoreMosse'

class TestGestioneInput(unittest.TestCase):
    """Suite di test per la classe GestioneInput."""

    def setUp(self):
        """Prepara i mock per Scacchiera e Partita prima di ogni test."""
        self.mock_scacchiera = Mock()
        self.mock_partita = Mock()
        self.mock_partita.get_stato_partita.return_value = 0
        self.mock_partita.get_turno.return_value = 0

    @patch(f'{PATH_TO_MODULE}.Re')
    def test_mossa_re(self, mock_Re):
        """Testa la corretta gestione di una mossa del Re."""
        move = "Rg1"
        GestioneInput(move, self.mock_scacchiera, self.mock_partita)
        mock_Re.assert_called_once_with(0)
        mock_Re.return_value.mossa.assert_called_once_with(
            move, self.mock_scacchiera, self.mock_partita
        )

    @patch(f'{PATH_TO_MODULE}.Re')
    def test_cattura_re(self, mock_Re):
        """Testa la corretta gestione di una cattura da parte del Re."""
        move = "Rxf7"
        GestioneInput(move, self.mock_scacchiera, self.mock_partita)
        mock_Re.assert_called_once_with(0)
        mock_Re.return_value.cattura.assert_called_once_with(
            move, self.mock_scacchiera, self.mock_partita
        )
        
    @patch(f'{PATH_TO_MODULE}.Donna')
    def test_mossa_donna(self, mock_Donna):
        """Testa la corretta gestione di una mossa della Donna."""
        move = "Dd4"
        GestioneInput(move, self.mock_scacchiera, self.mock_partita)
        mock_Donna.assert_called_once_with(0)
        mock_Donna.return_value.mossa.assert_called_once_with(
            move, self.mock_scacchiera, self.mock_partita
        )

    @patch(f'{PATH_TO_MODULE}.Pedone')
    def test_mossa_pedone(self, mock_Pedone):
        """Testa la corretta gestione di una mossa del Pedone."""
        move = "e4"
        GestioneInput(move, self.mock_scacchiera, self.mock_partita)
        mock_Pedone.assert_called_once_with(0)
        mock_Pedone.return_value.mossa.assert_called_once_with(
            move, self.mock_scacchiera, self.mock_partita
        )

    @patch(f'{PATH_TO_MODULE}.Pedone')
    def test_promozione_pedone(self, mock_Pedone):
        """Testa la corretta gestione di una promozione del Pedone."""
        move = "a8D"
        GestioneInput(move, self.mock_scacchiera, self.mock_partita)
        mock_Pedone.assert_called_once_with(0)
        mock_Pedone.return_value.promozione_pedone.assert_called_once_with(
            move, self.mock_scacchiera, self.mock_partita
        )

    def test_stampa_scacchiera_a_fine_turno(self):
        """Verifica che la scacchiera venga stampata alla fine di un turno valido."""
        self.mock_partita.get_turno.side_effect = [0, 1]
        
        with patch(f'{PATH_TO_MODULE}.Pedone'):
            GestioneInput("e4", self.mock_scacchiera, self.mock_partita)
        
        self.mock_scacchiera.stampa_scacchiera.assert_called_once_with(
            self.mock_scacchiera
        )

    def test_reset_partita_su_scacco_matto(self):
        """Verifica che la partita venga resettata dopo uno scacco matto."""
        self.mock_partita.get_turno.side_effect = [0, 1]
        self.mock_partita.scacco_matto.return_value = True
        self.mock_partita.stallo.return_value = False

        with patch(f'{PATH_TO_MODULE}.Pedone'):
            GestioneInput("e4", self.mock_scacchiera, self.mock_partita)

        self.mock_partita.azzera_mosse.assert_called_once()
        self.mock_scacchiera.azzera_istanze.assert_called_once()
        self.mock_partita.set_turno.assert_called_once()
        self.mock_partita.cambia_stato_partita.assert_called_once()
        
    @patch(f'{PATH_TO_MODULE}.errori')
    def test_errore_se_nessuna_partita_in_corso(self, mock_errori):
        """Verifica che venga generato un errore se non ci sono partite in corso."""
        self.mock_partita.get_stato_partita.return_value = 1
        
        GestioneInput("qualsiasi mossa", self.mock_scacchiera, self.mock_partita)
        
        mock_errori.errore_nessuna_partita.assert_called_once()

if __name__ == '__main__':
    unittest.main()