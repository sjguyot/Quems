"""Graphical interface for the Quems card counter."""

from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError:
    tk = None
    ttk = None

from quems_card_counter import count_cards


def parse_seen_cards_text(raw_text: str) -> list[str]:
    normalized = raw_text.replace(",", " ").replace("\n", " ").replace("\t", " ")
    return [token for token in normalized.split(" ") if token.strip()]


class QuemsCardCounterApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Quems Card Counter")
        self.root.geometry("920x640")
        self.root.configure(bg="#0f172a")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Main.TFrame", background="#0f172a")
        self.style.configure("Card.TFrame", background="#111827")
        self.style.configure("Title.TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 24, "bold"))
        self.style.configure("SubTitle.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 11))
        self.style.configure("Section.TLabel", background="#111827", foreground="#e2e8f0", font=("Segoe UI", 12, "bold"))
        self.style.configure("Metric.TLabel", background="#111827", foreground="#22d3ee", font=("Segoe UI", 16, "bold"))
        self.style.configure("Action.TButton", font=("Segoe UI", 11, "bold"))
        self.style.configure("Status.TLabel", background="#111827", foreground="#f8fafc", font=("Segoe UI", 11))

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, style="Main.TFrame", padding=24)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Quems Card Counter", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            container,
            text="Use cards like AS 10H QD or numeric format (x;y), ex: (3;12) for Queen of Hearts.",
            style="SubTitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 16))

        card = ttk.Frame(container, style="Card.TFrame", padding=18)
        card.pack(fill=tk.BOTH, expand=True)

        ttk.Label(card, text="Seen cards", style="Section.TLabel").pack(anchor=tk.W)
        self.input_text = tk.Text(
            card,
            height=4,
            bg="#0b1220",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief=tk.FLAT,
            font=("Consolas", 12),
            padx=10,
            pady=10,
        )
        self.input_text.pack(fill=tk.X, pady=(8, 12))
        self.input_text.insert("1.0", "AS 10H QD")

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill=tk.X, pady=(0, 12))

        ttk.Button(actions, text="Count cards", command=self.on_count, style="Action.TButton").pack(side=tk.LEFT)
        ttk.Button(actions, text="Clear", command=self.on_clear, style="Action.TButton").pack(side=tk.LEFT, padx=10)

        metrics = ttk.Frame(card, style="Card.TFrame")
        metrics.pack(fill=tk.X, pady=(0, 12))

        self.seen_label = ttk.Label(metrics, text="Seen cards: 0", style="Metric.TLabel")
        self.seen_label.pack(side=tk.LEFT, padx=(0, 24))
        self.remaining_label = ttk.Label(metrics, text="Remaining cards: 52", style="Metric.TLabel")
        self.remaining_label.pack(side=tk.LEFT)

        ttk.Label(card, text="Remaining deck", style="Section.TLabel").pack(anchor=tk.W)
        self.remaining_output = tk.Text(
            card,
            height=12,
            bg="#0b1220",
            fg="#e2e8f0",
            relief=tk.FLAT,
            font=("Consolas", 11),
            padx=10,
            pady=10,
            state=tk.DISABLED,
        )
        self.remaining_output.pack(fill=tk.BOTH, expand=True, pady=(8, 10))

        self.status_label = ttk.Label(card, text="Ready.", style="Status.TLabel")
        self.status_label.pack(anchor=tk.W)

    def on_count(self) -> None:
        raw_text = self.input_text.get("1.0", tk.END)
        cards = parse_seen_cards_text(raw_text)
        try:
            result = count_cards(cards)
        except ValueError as error:
            self.status_label.configure(text=f"Error: {error}")
            return

        self.seen_label.configure(text=f"Seen cards: {result['seen_count']}")
        self.remaining_label.configure(text=f"Remaining cards: {result['remaining_count']}")
        self._set_remaining_cards(result["remaining_cards"])
        self.status_label.configure(text="Count updated successfully.")

    def on_clear(self) -> None:
        self.input_text.delete("1.0", tk.END)
        self.seen_label.configure(text="Seen cards: 0")
        self.remaining_label.configure(text="Remaining cards: 52")
        self._set_remaining_cards([])
        self.status_label.configure(text="Cleared.")

    def _set_remaining_cards(self, remaining_cards: list[str]) -> None:
        chunks = [" ".join(remaining_cards[index : index + 13]) for index in range(0, len(remaining_cards), 13)]
        text = "\n".join(chunks)
        self.remaining_output.configure(state=tk.NORMAL)
        self.remaining_output.delete("1.0", tk.END)
        self.remaining_output.insert("1.0", text)
        self.remaining_output.configure(state=tk.DISABLED)


def main() -> int:
    if tk is None or ttk is None:
        raise RuntimeError("Tkinter is not available in this Python environment.")

    root = tk.Tk()
    app = QuemsCardCounterApp(root)
    app.on_count()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
