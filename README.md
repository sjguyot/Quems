# Quems

A simple Python card counter for the Quems game (standard 52-card deck).

## Usage

### Gorgeous GUI

```bash
python quems_gui.py
```

Then enter cards and click **Count cards**.

### CLI

```bash
python quems_card_counter.py AS 10H QD
```

You can also use numeric cards with `(x;y)`:
- `x` is the suit: `1=clover (C)`, `2=diamond (D)`, `3=heart (H)`, `4=spade (S)`
- `y` is the rank: `1=Ace`, `2-10=number cards`, `11=Jack`, `12=Queen`, `13=King`

```bash
python quems_card_counter.py "(3;12)" "(1;1)"
```

Example output:

```text
Seen cards: 3
Remaining cards: 49
Remaining deck:
AC 2C 3C 4C 5C 6C 7C 8C 9C 10C JC QC KC AD 2D 3D 4D 5D 6D 7D 8D 9D 10D JD KD AH 2H 3H 4H 5H 6H 7H 8H 9H JH QH KH 2S 3S 4S 5S 6S 7S 8S 9S 10S JS QS KS
```
