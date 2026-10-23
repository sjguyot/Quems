import unittest

from quems_gui import parse_seen_cards_text


class ParseSeenCardsTextTests(unittest.TestCase):
    def test_splits_spaces_commas_and_newlines(self):
        cards = parse_seen_cards_text("AS, 10H\nQD\t(3;12)")
        self.assertEqual(cards, ["AS", "10H", "QD", "(3;12)"])

    def test_ignores_empty_tokens(self):
        cards = parse_seen_cards_text("   AS   ,   ")
        self.assertEqual(cards, ["AS"])


if __name__ == "__main__":
    unittest.main()
