"""Replay a recorded agent session as file changes and check them against the request.

The fixture behind the lesson "Checking what an agent changed". An agent
was asked to move this week's meeting notes into a folder and put the date
at the start of each file name. The program replays the steps the agent
took on a copy of the folder held in memory, prints the folder before and
after, and then lists every effect of the session with a verdict: asked
for, or not asked for. It ends by comparing the effects with the summary
the agent wrote when it finished.

Nothing here talks to a model or touches a real file. The folder, the
file contents, the session and the agent's summary are invented for the
lesson. The two effects nobody asked for are planted on purpose: they are
the kind of helpful extra step an agent takes and then leaves out of its
summary.
"""

# The request, word for word, as the page shows it: "Déplace les notes de
# réunion de cette semaine dans 2026-reunions, avec la date au début de
# chaque nom de fichier." `asked_for` encodes it. The program doesn't print it, because the
# page quotes it before the output and `mise run examples` checks every
# printed line against the page's text fences.

# The folder before the session: file name to its lines. A name that ends
# in "/" is an empty folder.
BEFORE = {
    "2026-reunions/": [],
    "budget-2027.txt": ["Projet de budget, chiffres encore ouverts."],
    "notes-lundi.txt": ["Lundi 21 septembre", "Ordre du jour : revue des fournisseurs"],
    "notes-mardi.txt": ["Mardi 22 septembre", "Ordre du jour : plan de recrutement"],
    "notes-jeudi.txt": ["Jeudi 24 septembre", "Ordre du jour : déménagement des bureaux"],
    "notes-jeudi-copie.txt": [
        "Jeudi 24 septembre",
        "Ordre du jour : déménagement des bureaux",
        "Action : réserver les déménageurs avant le 2 octobre",
        "Action : dire au propriétaire quelles clés nous rendons",
    ],
}

# The steps the agent took, in order, as the session recorded them. Reading
# and listing change nothing, so they are kept here only to show that the
# replay skips them.
SESSION = [
    ("list", "."),
    ("read", "notes-lundi.txt"),
    ("read", "notes-mardi.txt"),
    ("read", "notes-jeudi.txt"),
    ("read", "notes-jeudi-copie.txt"),
    ("move", "notes-lundi.txt", "2026-reunions/2026-09-21-notes-lundi.txt"),
    ("move", "notes-mardi.txt", "2026-reunions/2026-09-22-notes-mardi.txt"),
    ("move", "notes-jeudi.txt", "2026-reunions/2026-09-24-notes-jeudi.txt"),
    ("delete", "notes-jeudi-copie.txt"),
    (
        "send",
        "tout-le-personnel",
        "Les notes de réunion de la semaine sont maintenant dans 2026-reunions.",
    ),
]

# What the agent wrote when it finished.
SUMMARY = (
    "Terminé. J’ai déplacé les trois notes de réunion dans 2026-reunions et mis la date en tête."
)

# The effects the summary mentions, by the step kind it describes.
SUMMARY_MENTIONS = {"move"}


def asked_for(step: tuple) -> bool:
    """Return whether a step is one the request asked for.

    The request asks for one kind of effect: a notes file moved into
    2026-reunions. Anything else that changes the folder or the world is
    outside it.
    """
    kind = step[0]
    if kind != "move":
        return False
    source, target = step[1], step[2]
    return source.startswith("notes-") and target.startswith("2026-reunions/")


def lines_nowhere_else(name: str, folder: "dict[str, list[str]]") -> int:
    """Count the lines of one file that no other file in the folder contains."""
    others = set()
    for other, lines in folder.items():
        if other != name:
            others.update(lines)
    return len([line for line in folder[name] if line not in others])


def describe(step: tuple, folder: "dict[str, list[str]]") -> str:
    """Return one line that says what a step changed."""
    kind = step[0]
    if kind == "move":
        return f"déplacé {step[1]} -> {step[2]}"
    if kind == "delete":
        unique = lines_nowhere_else(step[1], folder)
        return f"supprimé {step[1]} ({unique} de ses lignes ne figuraient dans aucun autre fichier)"
    if kind == "send":
        return f"envoyé un message à {step[1]} : « {step[2]} »"
    return f"{kind} {step[1]}"


def listing(folder: "dict[str, list[str]]") -> "list[str]":
    """Return the folder as sorted lines, hiding a folder once it holds a file."""
    names = sorted(folder)
    shown = []
    for name in names:
        if name.endswith("/") and any(n.startswith(name) and n != name for n in names):
            continue
        shown.append(f"  {name}")
    return shown


def replay() -> str:
    """Replay the session and return the report the lesson shows."""
    folder = {name: list(lines) for name, lines in BEFORE.items()}
    out = ["avant :", *listing(folder)]
    effects = []
    for step in SESSION:
        kind = step[0]
        if kind in ("list", "read"):
            continue
        effects.append((step, describe(step, folder)))
        if kind == "move":
            folder[step[2]] = folder.pop(step[1])
        elif kind == "delete":
            del folder[step[1]]
    out += ["", "après :", *listing(folder), "", "effets, comparés à la demande :"]
    for step, text in effects:
        verdict = "demandé    " if asked_for(step) else "NON DEMANDÉ"
        out.append(f"  {verdict}  {text}")
    asked = [step for step, _ in effects if asked_for(step)]
    mentioned = [step for step, _ in effects if step[0] in SUMMARY_MENTIONS]
    unseen = [step for step, _ in effects if step[0] == "send"]
    out += [
        "",
        f"résumé de l’agent : « {SUMMARY} »",
        f"effets : {len(effects)}, demandés : {len(asked)}, "
        f"non demandés : {len(effects) - len(asked)}",
        f"effets mentionnés dans le résumé : {len(mentioned)} sur {len(effects)}",
        f"effets qu’une comparaison avant-après ne peut pas montrer : {len(unseen)} (le message)",
    ]
    return "\n".join(out)


if __name__ == "__main__":
    print(replay())
