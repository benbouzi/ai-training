"""Check the specific claims in a summary against a folder of source files.

A model's summary of a document is fluent whether or not the document says
what the summary says. This script pulls the specifics out of a summary and
looks each one up in the sources: every quoted passage, every reference of
the form `article 7(3)` or `section 12`, and every figure. It prints one
entry per claim, `trouvé` with the source file, line and sentence, or
`SANS SOURCE`, then a summary line.

The sources are the `.txt` files in the `sources/` directory next to this
script, written one sentence per line so that an entry can point at a line.

- A quote is found when its text appears in a source, ignoring case and
  the amount of whitespace.
- A reference is found when the same article or section number appears.
- A figure is found when the same number appears, with or without a
  thousands comma or space, as a whole number and never as part of a longer one.

The script checks presence, and nothing more. A number that is found may
still be used for a different thing in the source, so the entry shows the
sentence for a person to read. Names and dates written in words are not
extracted, so those are left to the reader too.

Usage: python3 check_claims.py SUMMARY [--missing]

`--missing` prints only the claims with no source, one per line.

Exit status 0 when every claim has a source, 1 otherwise.

Standard library only, Python 3.9 or later.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(HERE, "sources")

# French translation: a quote is in « » or in straight double quotes, a
# figure may group its thousands with a space (7 200), and the word after a
# figure may have accents or be a percent sign (38 %).
QUOTE = re.compile(r'"([^"]+)"|«\s*([^»]+?)\s*»')
REFERENCE = re.compile(r"\b(?:article|section)\s+\d+(?:\(\d+\))?", re.IGNORECASE)
NUMBER = re.compile(r"\d{1,3}(?: \d{3})+(?![\d,])|\d[\d,]*(?:\.\d+)?")
NEXT_WORD = re.compile(r"\s+([A-Za-zÀ-ÿ]+|%)")

# A figure is shown with the word after it ("38 percent"), unless that word
# says nothing about what the number counts.
STOP_WORDS = {"a", "an", "and", "in", "of", "on", "or", "the", "to"}
STOP_WORDS |= {"à", "au", "aux", "d", "de", "des", "du", "en", "et"}
STOP_WORDS |= {"l", "la", "le", "les", "ou", "un", "une"}


def squash(text):
    """Lower-case `text` and collapse every run of whitespace to one space."""
    return " ".join(text.lower().split())


def find_claims(text):
    """Every quote, reference and figure in `text`, in order of appearance.

    Each claim is a tuple of (kind, label, needle): the label is what the
    report shows, and the needle is what is looked up in the sources.
    """
    found = []
    taken = []
    for match in QUOTE.finditer(text):
        quoted = match.group(1) or match.group(2)
        found.append((match.start(), "quote", f"« {quoted} »", quoted))
        taken.append((match.start(), match.end()))
    for match in REFERENCE.finditer(text):
        found.append((match.start(), "reference", match.group(0), match.group(0)))
        taken.append((match.start(), match.end()))
    for match in NUMBER.finditer(text):
        if any(start <= match.start() < end for start, end in taken):
            continue
        label = match.group(0)
        after = NEXT_WORD.match(text, match.end())
        if after and after.group(1).lower() not in STOP_WORDS:
            label += " " + after.group(1)
        found.append((match.start(), "figure", label, match.group(0)))
    found.sort()
    return [(kind, label, needle) for _, kind, label, needle in found]


def matcher(kind, needle):
    """Return a function that says whether one source line supports the claim."""
    if kind == "quote":
        wanted = squash(needle)
        return lambda line: wanted in squash(line)
    if kind == "reference":
        pattern = re.compile(r"\s+".join(re.escape(part) for part in needle.split()), re.IGNORECASE)
        return lambda line: pattern.search(line) is not None
    digits = needle.replace(",", "").replace(" ", "")
    body = "[, ]?".join(re.escape(d) for d in digits)
    pattern = re.compile(r"(?<![\d,.])(?<!\d )" + body + r"(?![\d,.]\d)(?! \d{3})")
    return lambda line: pattern.search(line) is not None


def read_sources(directory):
    """Every source as (file name, list of lines), in file name order."""
    sources = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".txt"):
            continue
        with open(os.path.join(directory, name), encoding="utf-8") as f:
            sources.append((name, f.read().splitlines()))
    return sources


def look_up(kind, needle, sources):
    """The first (file name, line number, line) that supports the claim, or None."""
    supports = matcher(kind, needle)
    for name, lines in sources:
        for number, line in enumerate(lines, start=1):
            if supports(line):
                return name, number, line
    return None


def report(claims, sources, missing_only):
    """Print the entries and the summary line. Returns the number of claims with no source."""
    missing = 0
    for kind, label, needle in claims:
        hit = look_up(kind, needle, sources)
        if hit is None:
            missing += 1
            print(label if missing_only else f"SANS SOURCE  {label}")
        elif not missing_only:
            name, number, line = hit
            print(f"trouvé       {label}")
            print(f"             {name}:{number}  {line}")
    if not missing_only:
        claims_word = "affirmations" if missing > 1 else "affirmation"
        verb = "n’ont" if missing > 1 else "n’a"
        print(f"{missing} {claims_word} sur {len(claims)} {verb} pas de source")
    return missing


def main(argv):
    args = [a for a in argv[1:] if a != "--missing"]
    missing_only = "--missing" in argv[1:]
    if len(args) != 1:
        print("usage : python3 check_claims.py RÉSUMÉ [--missing]")
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    except OSError as exc:
        print(f"ÉCHEC : impossible de lire {args[0]} : {exc.strerror}")
        return 1
    claims = find_claims(text)
    if not claims:
        print("aucune citation, référence ou chiffre trouvé dans le résumé")
        return 0
    missing = report(claims, read_sources(SOURCES), missing_only)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
