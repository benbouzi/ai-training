"""Price a short prompt and a long one, for the lesson "What every token costs".

Run it with no argument and it prices the two built-in prompts below at the
example prices in PRICES. Run it on your own prompt to see its estimated
token count and its price:   python3 price_prompts.py prompt.txt

Every number here is an estimate or an example. The token rule is the
common rule of thumb for English, about four characters per token, the same
rule the lesson "What the model can see" uses: a word of up to six
characters is one token, a longer word is one token per four characters
(rounded up), and every punctuation mark is a token of its own. Vendors
publish the exact tokenizer and the current prices; PRICES holds round
example numbers for "a small model" and "a large model", not a quote.
"""

import math
import re
import sys

CHARS_PER_TOKEN = 4
ONE_TOKEN_WORD = 6

# A piece is a run of letters and digits, or a single mark of punctuation.
PIECE = re.compile(r"\w+|[^\w\s]")

# Example prices in dollars per million tokens: (input, output). Vendors
# charge more for a token the model writes than for one it reads.
PRICES = {
    "small model": (0.6, 3.0),
    "large model": (6.0, 30.0),
}

# The model's answer is priced at the output rate. The lesson assumes the
# same five-bullet summary, about 120 tokens, for every call.
ANSWER_TOKENS = 120

# The lesson's team wants a summary of every meeting, about a thousand a month.
CALLS_PER_MONTH = 1_000

SHORT_PROMPT = """\
Résume ce compte rendu de réunion en cinq puces pour l’équipe financière.
Chaque puce doit faire moins de 20 mots.

Compte rendu, projet Lantern, 14 mars.
Présents : Ana, Bram, Chidi. Le fournisseur a déplacé la livraison des
cartes capteurs d’avril à juin. Ana confirmera la date de juin par écrit
d’ici vendredi. Le guide d’installation doit être raccourci, avec une photo
par étape. Le pilote de l’entrepôt d’Utrecht passe en juillet. Prochaine
réunion le 28 mars.
"""

LONG_PROMPT = """\
Bonjour ! J’espère que vous allez bien aujourd’hui. J’ai une tâche à vous
confier et j’apprécierais vraiment votre aide. Je travaille dans une
entreprise qui mène un projet appelé Lantern, qui consiste à installer des
cartes capteurs dans des entrepôts, et nous avons régulièrement des réunions
à ce sujet. J’ai ci-dessous le compte rendu de notre dernière réunion et j’en
ai besoin d’un résumé. Le résumé est destiné à l’équipe financière, merci de
le garder en tête. Je pense que cinq puces seraient une bonne longueur, et ce
serait formidable que chaque puce ne soit pas trop longue, peut-être moins de
20 mots environ, parce que l’équipe financière n’a pas beaucoup de temps pour
lire de longs documents. Merci de bien inclure les points les plus
importants. Merci beaucoup d’avance pour votre aide, je l’apprécie vraiment !

Voici le compte rendu :

Compte rendu, projet Lantern, 14 mars.
Présents : Ana, Bram, Chidi. Ana a ouvert la réunion et indiqué que le
fournisseur a déplacé la livraison des cartes capteurs d’avril à juin. Bram a
demandé si la date de juin était ferme. Ana confirmera la date de juin par
écrit d’ici vendredi. Chidi a présenté le premier jet du guide d’installation,
et l’équipe a demandé une version plus courte avec une photo par étape. Après
discussion, l’équipe a décidé que le pilote de l’entrepôt d’Utrecht passe en
juillet. La prochaine réunion aura lieu le 28 mars, dans la même salle que la
dernière fois.

N’hésitez pas à me dire si vous avez besoin d’autres informations. Merci
encore !
"""


def estimate_tokens(text: str) -> int:
    """Return the estimated number of tokens in `text`."""
    total = 0
    for piece in PIECE.findall(text):
        if not piece[0].isalnum() or len(piece) <= ONE_TOKEN_WORD:
            total += 1
        else:
            total += math.ceil(len(piece) / CHARS_PER_TOKEN)
    return total


def price(prompt_tokens: int, answer_tokens: int, model: str, calls: int = 1) -> float:
    """Return the price in dollars of `calls` calls at the example prices of `model`."""
    input_price, output_price = PRICES[model]
    per_call = (prompt_tokens * input_price + answer_tokens * output_price) / 1_000_000
    return per_call * calls


def report(prompts: "dict[str, str]") -> str:
    """Return the report the lesson shows: token counts, then a price per prompt and model."""
    counts = {name: estimate_tokens(text) for name, text in prompts.items()}
    lines = [f"{name}: {tokens} tokens (estimate)" for name, tokens in counts.items()]
    if len(counts) == 2:
        low, high = sorted(counts.values())
        lines.append(f"difference: {high - low} tokens")
    lines.append(f"answer: {ANSWER_TOKENS} tokens (assumed)")
    lines.append("")
    lines.append(f"{'':26}{'one call':>10}{f'{CALLS_PER_MONTH:,} calls':>16}")
    for model in PRICES:
        for name, tokens in counts.items():
            one = price(tokens, ANSWER_TOKENS, model)
            month = price(tokens, ANSWER_TOKENS, model, CALLS_PER_MONTH)
            lines.append(f"{model + ', ' + name:26}{f'${one:.4f}':>10}{f'${month:,.2f}':>16}")
    return "\n".join(lines)


def main(argv: "list[str]") -> None:
    if len(argv) > 1:
        with open(argv[1], encoding="utf-8") as handle:
            prompts = {"your prompt": handle.read()}
    else:
        prompts = {"short prompt": SHORT_PROMPT, "long prompt": LONG_PROMPT}
    print(report(prompts))


if __name__ == "__main__":
    main(sys.argv)
