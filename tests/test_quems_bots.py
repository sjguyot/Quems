import unittest

from quems_bots import simulate_quems_game


class QuemsBotsTests(unittest.TestCase):
    def test_simulation_is_deterministic_with_seed(self):
        first = simulate_quems_game(bot_count=4, seed=42)
        second = simulate_quems_game(bot_count=4, seed=42)
        self.assertEqual(first, second)

    def test_simulation_plays_full_deck_and_counter_reaches_zero(self):
        result = simulate_quems_game(bot_count=4, seed=7)
        self.assertEqual(sum(result["scores"].values()), len(result["rounds"]))
        self.assertEqual(sum(result["scores"].values()), 13)
        self.assertEqual(result["rounds"][-1]["seen_count"], 52)
        self.assertEqual(result["rounds"][-1]["remaining_count"], 0)

    def test_invalid_bot_count_raises_error(self):
        with self.assertRaisesRegex(ValueError, "at least 2"):
            simulate_quems_game(bot_count=1, seed=1)


if __name__ == "__main__":
    unittest.main()
