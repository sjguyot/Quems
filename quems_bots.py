"""Bot simulation for Quems to exercise card-counter behavior."""

from __future__ import annotations

import argparse
import random

from quems_card_counter import DECK, RANKS, SUITS, count_cards


def card_strength(card: str) -> int:
    """Return strength index for comparing cards by rank then suit."""
    rank = card[:-1]
    suit = card[-1]
    return RANKS.index(rank) * len(SUITS) + SUITS.index(suit)


def simulate_quems_game(bot_count: int, seed: int | None = None) -> dict[str, object]:
    if bot_count < 2:
        raise ValueError("bot_count must be at least 2")

    rng = random.Random(seed)
    deck = list(DECK)
    rng.shuffle(deck)

    hands = {f"Bot {index + 1}": [] for index in range(bot_count)}
    for turn, card in enumerate(deck):
        bot_name = f"Bot {(turn % bot_count) + 1}"
        hands[bot_name].append(card)

    scores = {bot_name: 0 for bot_name in hands}
    seen_cards: list[str] = []
    rounds: list[dict[str, object]] = []
    max_rounds = max(len(hand) for hand in hands.values())

    for round_number in range(max_rounds):
        played_cards: dict[str, str] = {}
        for bot_name, hand in hands.items():
            if round_number < len(hand):
                played_cards[bot_name] = hand[round_number]

        if not played_cards:
            continue

        winner = max(played_cards, key=lambda name: card_strength(played_cards[name]))
        scores[winner] += 1

        seen_cards.extend(played_cards.values())
        counter_result = count_cards(seen_cards)
        rounds.append(
            {
                "round": round_number + 1,
                "plays": played_cards,
                "winner": winner,
                "seen_count": counter_result["seen_count"],
                "remaining_count": counter_result["remaining_count"],
            }
        )

    champions = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_score = champions[0][1]
    winners = [name for name, score in champions if score == best_score]

    return {
        "bot_count": bot_count,
        "seed": seed,
        "scores": scores,
        "winners": winners,
        "rounds": rounds,
    }


def estimate_bot_win_probability(
    bot_count: int,
    target_bot: int,
    trials: int = 1000,
    seed: int | None = None,
) -> dict[str, object]:
    if bot_count < 2:
        raise ValueError("bot_count must be at least 2")
    if target_bot < 1 or target_bot > bot_count:
        raise ValueError("target_bot must be between 1 and bot_count")
    if trials < 1:
        raise ValueError("trials must be at least 1")

    rng = random.Random(seed)
    target_name = f"Bot {target_bot}"
    weighted_wins = 0.0

    for _ in range(trials):
        game_seed = rng.randrange(0, 2**32)
        game_result = simulate_quems_game(bot_count=bot_count, seed=game_seed)
        winners = game_result["winners"]
        if target_name in winners:
            weighted_wins += 1.0 / len(winners)

    probability = weighted_wins / trials
    return {
        "bot_count": bot_count,
        "target_bot": target_bot,
        "target_name": target_name,
        "trials": trials,
        "seed": seed,
        "estimated_win_probability": probability,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Quems bot simulations for testing.")
    parser.add_argument("--bots", type=int, default=4, help="Number of bots (minimum 2).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for deterministic results.")
    parser.add_argument("--show-rounds", action="store_true", help="Display each simulated round.")
    parser.add_argument("--estimate", action="store_true", help="Estimate win probability instead of one game.")
    parser.add_argument("--target-bot", type=int, default=1, help="Bot index to evaluate in estimate mode.")
    parser.add_argument("--trials", type=int, default=1000, help="Number of Monte Carlo trials in estimate mode.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.estimate:
            result = estimate_bot_win_probability(
                bot_count=args.bots,
                target_bot=args.target_bot,
                trials=args.trials,
                seed=args.seed,
            )
        else:
            result = simulate_quems_game(args.bots, args.seed)
    except ValueError as error:
        parser.error(str(error))

    if args.estimate:
        print(f"Bots: {result['bot_count']}")
        print(f"Seed: {result['seed']}")
        print(f"Target bot: {result['target_name']}")
        print(f"Trials: {result['trials']}")
        print(f"Estimated win probability: {result['estimated_win_probability']:.4f}")
    else:
        print(f"Bots: {result['bot_count']}")
        print(f"Seed: {result['seed']}")
        print("Scores:")
        for bot_name in sorted(result["scores"]):
            print(f"  {bot_name}: {result['scores'][bot_name]}")

        print(f"Winners: {', '.join(result['winners'])}")
        if args.show_rounds:
            print("Rounds:")
            for round_info in result["rounds"]:
                plays = ", ".join(f"{name}={card}" for name, card in sorted(round_info["plays"].items()))
                print(
                    f"  R{round_info['round']:02d}: {plays} -> {round_info['winner']} "
                    f"(seen={round_info['seen_count']}, remaining={round_info['remaining_count']})"
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
