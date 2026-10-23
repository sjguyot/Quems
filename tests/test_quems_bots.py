import unittest

from quems_bots import estimate_bot_win_probability, simulate_quems_game


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

    def test_estimate_is_deterministic_with_seed(self):
        first = estimate_bot_win_probability(bot_count=4, target_bot=1, trials=200, seed=99)
        second = estimate_bot_win_probability(bot_count=4, target_bot=1, trials=200, seed=99)
        self.assertEqual(first, second)

    def test_estimate_probability_is_bounded(self):
        result = estimate_bot_win_probability(bot_count=4, target_bot=2, trials=200, seed=11)
        self.assertGreaterEqual(result["estimated_win_probability"], 0.0)
        self.assertLessEqual(result["estimated_win_probability"], 1.0)

    def test_estimate_invalid_target_bot_raises_error(self):
        with self.assertRaisesRegex(ValueError, "target_bot"):
            estimate_bot_win_probability(bot_count=4, target_bot=5, trials=10, seed=1)


if __name__ == "__main__":
    unittest.main()
