"""How many pages of a given token count fit in a context window.

Run it with the token count of your page:   python3 pages_per_window.py 150
Run it with no argument and it uses the estimate count_tokens.py prints for
the meeting notes in sample/notes.txt.

The window sizes are round numbers that stand for the sizes on the market
in 2026: small open models at the low end, the large vendor models at the
high end. Check the vendor's documentation for the size of the model you use.
"""

import sys

SAMPLE_TOKENS = 141
WINDOWS = [8_000, 32_000, 200_000, 1_000_000]


def pages_per_window(tokens_per_page: int) -> "list[tuple[int, int]]":
    """Return (window size, whole pages that fit) for every window size."""
    return [(window, window // tokens_per_page) for window in WINDOWS]


def thousands(n: int) -> str:
    """`n` with a space between each group of three digits, as French writes it."""
    return f"{n:,}".replace(",", " ")


def pages_word(n: int) -> str:
    """`page` for 0 and 1, `pages` from 2 on."""
    return "pages" if n > 1 else "page"


def report(tokens_per_page: int) -> str:
    """Return one line per window size."""
    lines = [f"une page : {tokens_per_page} jetons"]
    for window, pages in pages_per_window(tokens_per_page):
        fit = f"{thousands(pages)} {pages_word(pages)}"
        lines.append(f"fenêtre de {thousands(window)} jetons : {fit}")
    return "\n".join(lines)


def main(argv: "list[str]") -> None:
    tokens_per_page = int(argv[1]) if len(argv) > 1 else SAMPLE_TOKENS
    print(report(tokens_per_page))


if __name__ == "__main__":
    main(sys.argv)
