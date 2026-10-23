"""Simple card counter for a standard Quems deck (52 cards)."""

from __future__ import annotations

import argparse
from collections import Counter

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["C", "D", "H", "S"]
DECK = {f"{rank}{suit}" for suit in SUITS for rank in RANKS}


def normalize_card(value: str) -> str:
    card = value.strip().upper()
    if len(card) < 2:
        raise ValueError(f"Invalid card: {value!r}")

    suit = card[-1]
    rank = card[:-1]

    if rank not in RANKS or suit not in SUITS:
        raise ValueError(f"Invalid card: {value!r}")

    return f"{rank}{suit}"


def count_cards(cards: list[str]) -> dict[str, object]:
    normalized_cards = [normalize_card(card) for card in cards]

    duplicates = [card for card, count in Counter(normalized_cards).items() if count > 1]
    if duplicates:
        dupes = ", ".join(sorted(duplicates))
        raise ValueError(f"Duplicate card(s) found: {dupes}")

    unknown_cards = sorted(set(normalized_cards) - DECK)
    if unknown_cards:
        unknown = ", ".join(unknown_cards)
        raise ValueError(f"Unknown card(s): {unknown}")

    remaining = sorted(DECK - set(normalized_cards), key=lambda c: (SUITS.index(c[-1]), RANKS.index(c[:-1])))

    return {
        "seen_count": len(normalized_cards),
        "remaining_count": len(remaining),
        "remaining_cards": remaining,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Count seen and remaining cards in Quems.")
    parser.add_argument(
        "cards",
        nargs="*",
        help="Seen cards in format <rank><suit>, example: AS 10H QD",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = count_cards(args.cards)
    except ValueError as error:
        parser.error(str(error))

    print(f"Seen cards: {result['seen_count']}")
    print(f"Remaining cards: {result['remaining_count']}")

    if result["remaining_cards"]:
        print("Remaining deck:")
        print(" ".join(result["remaining_cards"]))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
