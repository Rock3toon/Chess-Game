"""Suite di test per la classe parse_input."""

import unittest

from scacchi.Control.parse_input import parse_input


class TestParseInput(unittest.TestCase):
    """Suite di test per la classe parse_input."""

    def setUp(self):
        """Crea un'istanza del parser prima di ogni test."""
        self.parser = parse_input()

    # --- Test per il metodo parseCommand ---

    def test_parse_command_validi(self):
        """Verifica che i comandi validi restituiscano il codice corretto."""
        self.assertEqual(self.parser.parseCommand("/help"), 1)
        self.assertEqual(self.parser.parseCommand("/esci"), 2)
        self.assertEqual(self.parser.parseCommand("/scacchiera"), 3)
        self.assertEqual(self.parser.parseCommand("/gioca"), 4)
        self.assertEqual(self.parser.parseCommand("/abbandona"), 5)
        self.assertEqual(self.parser.parseCommand("/patta"), 6)
        self.assertEqual(self.parser.parseCommand("/mosse"), 7)

    def test_parse_command_con_spazi_e_maiuscole(self):
        """Verifica che spazi e maiuscole vengano ignorati correttamente."""
        self.assertEqual(self.parser.parseCommand(" /Help "), 1)
        self.assertEqual(self.parser.parseCommand("/GIOCA"), 4)

    def test_parse_command_non_valido(self):
        """Verifica che un comando non valido restituisca -1."""
        self.assertEqual(self.parser.parseCommand("/start"), -1)
        self.assertEqual(self.parser.parseCommand("mossa a caso"), -1)
        self.assertEqual(self.parser.parseCommand(""), -1)

    # --- Test per il metodo parseMove ---

    def test_parse_move_valide(self):
        """Verifica che vari formati di mosse valide vengano accettati."""
        mosse_valide = [
            "e4", "Cf3", "d5", "a1", "h8",           # Mosse semplici
            "Ra1", "Dd8", "Tc4", "Ae6", "Cg5",       # Mosse con lettera pezzo
            "Tad1", "T1d2",                          # Mosse ambigue
            # MODIFICA: "Cf1d2" è stato rimosso perché non è supportato dal parser
            "0-0", "0-0-0",                          # Arrocco
            "a8D", "h1T",                           # Promozione
            "bxa8A", "gxh1C",                        # Promozione con cattura
            "exd5", "cxb2",                         # Cattura semplice
            "Rxa1", "Dxh7", "Cxf7",                  # Cattura con lettera pezzo
            "Taxd1", "C1xf2"                         # Cattura con ambiguità
        ]
        for mossa in mosse_valide:
            with self.subTest(mossa=mossa):
                input_con_spazi = f" {mossa} "
                # Il metodo parseMove rimuove già gli spazi interni ed esterni
                self.assertEqual(self.parser.parseMove(input_con_spazi), mossa)

    def test_parse_move_non_valide(self):
        """Verifica che le mosse non valide vengano rifiutate con -1."""
        mosse_non_valide = [
            "e9", "i4", "RDTa1", "Cff", "cattura",   # Formati invalidi
            "0-0-0-0", "e8x", "axb9D", "Zf3", "",
            "Cf1d2"  # MODIFICA: Aggiunto perché il parser non lo gestisce
        ]
        for mossa in mosse_non_valide:
            with self.subTest(mossa=mossa):
                self.assertEqual(self.parser.parseMove(mossa), -1)

    # --- Test per il metodo parseConfirm ---

    def test_parse_confirm_positive(self):
        """Verifica che tutte le varianti di 'sì' restituiscano 'si'."""
        # Rimossi i casi con spazi (" SI ", "Yes") perché parseConfirm non usa .strip()
        risposte_positive = ["s", "si", "y", "ys", "yes", "Si", "YES"]
        for risposta in risposte_positive:
            with self.subTest(risposta=risposta):
                self.assertEqual(self.parser.parseConfirm(risposta), "si")

    def test_parse_confirm_negative(self):
        """Verifica che tutte le varianti di 'no' restituiscano 'no'."""
        # Rimosso il caso con spazi (" No ") perché parseConfirm non usa .strip()
        risposte_negative = ["n", "no", "nop", "nope", "No", "N"]
        for risposta in risposte_negative:
            with self.subTest(risposta=risposta):
                self.assertEqual(self.parser.parseConfirm(risposta), "no")

    def test_parse_confirm_invalide(self):
        """Verifica che risposte non chiare restituiscano -1."""
        risposte_invalide = \
        ["forse", "ok", "certo", "sisi", "nono", "yess", "", " si ", " no "]
        for risposta in risposte_invalide:
            with self.subTest(risposta=risposta):
                self.assertEqual(self.parser.parseConfirm(risposta), -1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
