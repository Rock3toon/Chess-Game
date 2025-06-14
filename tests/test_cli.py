"""Tests per il modulo CLI di Scacchi."""

import unittest
from unittest.mock import Mock, patch

import scacchi.Boundary.cli as cli


class TestCliScacchi(unittest.TestCase):
    """Suite di test per le funzioni dell'interfaccia a riga di comando (CLI)."""

    def setUp(self):
        """Prepara i mock per Scacchiera e Partita prima di ogni test."""
        # Creiamo oggetti 'Mock' che simulano il comportamento di Scacchiera e Partita.
        self.mock_scacchiera = Mock()
        self.mock_partita = Mock()

    #Sostituiamo 'errori', 'ui' e l'oggetto 'console' per controllarne le chiamate.
    @patch('scacchi.Boundary.cli.errori')
    @patch('scacchi.Boundary.cli.ui')
    @patch('scacchi.Boundary.cli.console')
    def test_gioca_starts_new_game(self, mock_console, mock_ui, mock_errori):
        """Verifica l'avvio corretto di una nuova partita tramite la funzione gioca."""
        # Simuliamo che la partita non sia in corso (stato = 1)
        self.mock_partita.get_stato_partita.return_value = 1
        
         # Chiamiamo la funzione che vogliamo testare.
        cli.gioca(self.mock_scacchiera, self.mock_partita)

         # Verifa che i metodi per inizializzare nuova partita siano chiamati 1 volta.
        self.mock_partita.azzera_mosse.assert_called_once()
        self.mock_partita.set_turno.assert_called_once()
        self.mock_scacchiera.azzera_istanze.assert_called_once()
        # Verifichiamo che la scacchiera sia stata popolata (64 caselle).
        self.assertEqual(self.mock_scacchiera.set_pezzo_scacchiera.call_count, 64)
        self.mock_partita.cambia_stato_partita.assert_called_once()
        self.mock_scacchiera.inizializza_istanze.assert_called_once()
        # Verifichiamo che la scacchiera sia stata stampata a schermo.
        self.mock_scacchiera.stampa_scacchiera.assert_called_once()
        mock_console.print.assert_called()
        # Ci assicuriamo che non sia stata sollevata nessuna condizione di errore.
        mock_errori.errore_gioca.assert_not_called()

    @patch('scacchi.Boundary.cli.errori')
    def test_gioca_when_game_in_progress(self, mock_errori):
        """Verifica che gioca() segnali un errore se una partita è già in corso."""
        self.mock_partita.get_stato_partita.return_value = 0
        
        cli.gioca(self.mock_scacchiera, self.mock_partita)
        
        mock_errori.errore_gioca.assert_called_once()
        self.mock_partita.azzera_mosse.assert_not_called()

    @patch('scacchi.Boundary.cli.ui')
    @patch('builtins.input', return_value='si')
    def test_abbandona_with_confirmation(self, mock_input, mock_ui):
        """Testa l'abbandono della partita con conferma da parte dell'utente."""
        self.mock_partita.get_stato_partita.return_value = 0
        self.mock_partita.get_turno.return_value = 0
        
        cli.abbandona(self.mock_partita, self.mock_scacchiera)
        
        self.mock_partita.cambia_stato_partita.assert_called_once()
        mock_ui.print_abbandono_partita.assert_called_once_with("NERO")

    @patch('builtins.print')
    @patch('builtins.input', return_value='no')
    def test_abbandona_with_cancellation(self, mock_input, mock_print):
        """Testa l'annullamento del comando di abbandono."""
        self.mock_partita.get_stato_partita.return_value = 0
        
        cli.abbandona(self.mock_partita, self.mock_scacchiera)
        
        self.mock_partita.cambia_stato_partita.assert_not_called()
        mock_print.assert_any_call("Operazione annullata!")

    @patch('sys.exit')
    @patch('builtins.input', return_value='si')
    def test_esci_with_confirmation(self, mock_input, mock_exit):
        """Verifica l'uscita dal programma con conferma dell'utente."""
        cli.esci()
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    @patch('builtins.input', return_value='no')
    def test_esci_with_cancellation(self, mock_input, mock_exit):
        """Verifica l'annullamento dell'uscita dal programma."""
        cli.esci()
        mock_exit.assert_not_called()

    @patch('scacchi.Boundary.cli.ui')
    @patch('builtins.input', side_effect=['si', 'si'])
    def test_patta_accepted(self, mock_input, mock_ui):
        """Verifica la corretta gestione di una proposta di patta accettata."""
        self.mock_partita.get_stato_partita.return_value = 0
        
        cli.patta(self.mock_partita, self.mock_scacchiera)
        
        mock_ui.print_patta_accettata.assert_called_once()
        self.mock_partita.cambia_stato_partita.assert_called_once()
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['si', 'no'])
    def test_patta_rejected(self, mock_input, mock_print):
        """Verifica la corretta gestione di una proposta di patta rifiutata."""
        self.mock_partita.get_stato_partita.return_value = 0
        
        cli.patta(self.mock_partita, self.mock_scacchiera)
        
        self.mock_partita.cambia_stato_partita.assert_not_called()
        self.assertTrue(any("rifiutata" in str(c) for c in mock_print.call_args_list))

    @patch('scacchi.Boundary.cli.ui')
    def test_partita_in_scacco_matto(self, mock_ui):
        """Verifica che lo scacco matto dichiari il vincitore corretto."""
        self.mock_partita.get_turno.return_value = 0
        cli.partita_in_scacco_matto(self.mock_partita)
        mock_ui.print_scacco_matto.assert_called_with("NERO")
        
        self.mock_partita.get_turno.return_value = 1
        cli.partita_in_scacco_matto(self.mock_partita)
        mock_ui.print_scacco_matto.assert_called_with("BIANCO")

    def test_configurazione_parser_crea_argomenti_help(self):
        """Verifica la corretta configurazione degli argomenti di aiuto nel parser."""
        parser = cli.ConfigurazioneParser()
        actions = [action.option_strings for action in parser._actions]
        
        self.assertIn(['-h'], actions)
        self.assertIn(['--help'], actions)


if __name__ == '__main__':
    unittest.main(verbosity=2)