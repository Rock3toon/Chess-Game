"""Tests for the main module."""

import os
import sys
from unittest.mock import patch

import pytest

# Aggiungi la root del progetto al path di Python per permettere l'import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importa il modulo main da testare. Usiamo un alias per chiarezza.
from scacchi import main as scacchi_main  # noqa: E402


def test_main_loop_calls_gioca(monkeypatch):
    """Verifica che il comando /gioca chiami la funzione gioca."""
    user_inputs = ["/gioca", "/esci"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    with (
        patch("scacchi.main.gioca") as mock_gioca,
        patch("scacchi.main.esci", side_effect=SystemExit),
        patch("scacchi.main.parse_input") as mock_parse_class,
    ):
        mock_parser_instance = mock_parse_class.return_value
        mock_parser_instance.parseCommand.side_effect = [4, 2]

        with pytest.raises(SystemExit):
            scacchi_main.main()

        mock_gioca.assert_called_once()


def test_main_loop_handles_invalid_command(monkeypatch):
    """Verifica la corretta gestione di un comando non valido."""
    user_inputs = ["/comando_inesistente", "/esci"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    with (
        patch("scacchi.main.errori.errore_comando_non_riconosciuto") as mock_errore_cmd,
        patch("scacchi.main.esci", side_effect=SystemExit),
        patch("scacchi.main.parse_input") as mock_parse_class,
    ):
        mock_parser_instance = mock_parse_class.return_value
        mock_parser_instance.parseCommand.side_effect = [-1, 2]

        with pytest.raises(SystemExit):
            scacchi_main.main()

        mock_errore_cmd.assert_called_once()


def test_main_loop_handles_valid_move(monkeypatch):
    """Verifica che una mossa valida venga passata a GestioneInput."""
    user_inputs = ["e2e4", "/esci"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    with (
        patch("scacchi.main.parse_input") as mock_parse_class,
        patch("scacchi.main.GestioneInput") as mock_gestione_input,
        patch("scacchi.main.esci", side_effect=SystemExit),
    ):
        mock_parser_instance = mock_parse_class.return_value
        mock_parser_instance.parseMove.return_value = ("e2", "e4")
        # Simula che l'input non sia un comando ma una mossa
        mock_parser_instance.parseCommand.return_value = 2

        with pytest.raises(SystemExit):
            scacchi_main.main()

        mock_parser_instance.parseMove.assert_called_once_with("e2e4")
        mock_gestione_input.assert_called_once()


def test_main_loop_handles_invalid_move(monkeypatch):
    """Verifica la corretta gestione di una mossa non valida."""
    user_inputs = ["mossa-errata", "/esci"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs.pop(0))

    with (
        patch("scacchi.main.parse_input") as mock_parse_class,
        patch("scacchi.main.errori.errore_mossa_non_valida") as mock_errore_mossa,
        patch("scacchi.main.esci", side_effect=SystemExit),
    ):
        mock_parser_instance = mock_parse_class.return_value
        mock_parser_instance.parseMove.return_value = -1
        # Simula che l'input non sia un comando ma una mossa (invalida)
        mock_parser_instance.parseCommand.return_value = 2

        with pytest.raises(SystemExit):
            scacchi_main.main()

        mock_parser_instance.parseMove.assert_called_once_with("mossa-errata")
        mock_errore_mossa.assert_called_once()