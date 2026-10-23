import unittest

from quems_card_counter import count_cards


class CountCardsTests(unittest.TestCase):
    def test_counts_seen_and_remaining_cards(self):
        result = count_cards(["AS", "10H", "qd"])
        self.assertEqual(result["seen_count"], 3)
        self.assertEqual(result["remaining_count"], 49)
        self.assertNotIn("AS", result["remaining_cards"])
        self.assertNotIn("10H", result["remaining_cards"])
        self.assertNotIn("QD", result["remaining_cards"])

    def test_duplicate_cards_raise_error(self):
        with self.assertRaisesRegex(ValueError, "Duplicate card"):
            count_cards(["AS", "as"])

    def test_invalid_card_raises_error(self):
        with self.assertRaisesRegex(ValueError, "Invalid card"):
            count_cards(["1X"])


if __name__ == "__main__":
    unittest.main()
