"""Read an agent's permission list and print what each row reaches.

The fixture behind the lesson "Sizing an agent's blast radius". The task is
to tidy one shared folder. The permission list is what the agent was given
for it. For each row the fixture prints what the row reaches, how many
people can be affected, and whether its actions can be undone. It then
does the same for the list with the rows the task does not need crossed out
and the rest narrowed to the one folder.

Nothing here talks to a model, a drive or a mail server. The rows and the
audience sizes are invented, and the undo rule is written out below.
"""

from typing import NamedTuple, Optional


class Row(NamedTuple):
    number: int
    kind: str  # read, write or send (printed in French by KIND)
    where: str
    actions: str


# Who a row reaches in each place: a label for the report and a head count.
# A count of None means there is no fixed limit.
AUDIENCE = {
    "Lecteur d’équipe, tous les dossiers": ("14 personnes", 14),
    "Lecteur d’équipe/Projets/2025": ("5 personnes", 5),
    "votre messagerie": ("vous, et tous ceux qui vous ont écrit", 1),
    "e-mails depuis votre adresse": ("toute personne qui a une adresse", None),
    "canal de discussion de tout le personnel": ("120 personnes", 120),
}

# How each kind of row prints.
KIND = {"read": "lecture", "write": "écriture", "send": "envoi"}

GRANTED = [
    Row(1, "read", "Lecteur d’équipe, tous les dossiers", "ouvrir, lister"),
    Row(2, "write", "Lecteur d’équipe, tous les dossiers", "créer, déplacer, renommer"),
    Row(3, "write", "Lecteur d’équipe, tous les dossiers", "supprimer (sans corbeille)"),
    Row(4, "read", "votre messagerie", "ouvrir, chercher"),
    Row(5, "send", "e-mails depuis votre adresse", "vers n’importe quelle adresse"),
    Row(6, "send", "canal de discussion de tout le personnel", "publier"),
]

# The same list after the tidy-up task is applied to it: rows 4, 5 and 6
# crossed out, and rows 1 to 3 narrowed to the one folder.
FOLDER = "Lecteur d’équipe/Projets/2025"
NEEDED = [
    Row(1, "read", FOLDER, "ouvrir, lister"),
    Row(2, "write", FOLDER, "créer, déplacer, renommer"),
    Row(3, "write", FOLDER, "supprimer (sans corbeille)"),
]


def undo(row: Row) -> str:
    """Return whether the row's actions can be undone.

    Reading changes nothing. On this drive a move never replaces a file:
    two files with the same name stay side by side, so a move or a rename
    can be moved or renamed back. A delete with no trash cannot be restored, and a message that
    someone has read cannot be taken back.
    """
    if row.kind == "read":
        return "rien à annuler"
    if row.kind == "send" or "supprimer" in row.actions:
        return "non"
    return "oui"


def most(rows: list[Row]) -> Optional[str]:
    """Return the widest audience among the rows that change something."""
    changing = [AUDIENCE[row.where] for row in rows if row.kind != "read"]
    unlimited = [label for label, count in changing if count is None]
    if unlimited:
        return unlimited[0]
    if not changing:
        return None
    return max(changing, key=lambda audience: audience[1] or 0)[0]


def report(title: str, rows: list[Row]) -> str:
    """Return one block of the report: a line per row, then a summary."""
    lines = [title]
    for row in rows:
        kind = KIND[row.kind]
        lines.append(f"  ligne {row.number}  {kind:<8}  {row.where} : {row.actions}")
        lines.append(f"           atteint : {AUDIENCE[row.where][0]}   annulable : {undo(row)}")
    final = [str(row.number) for row in rows if undo(row) == "non"]
    lines.append(f"  lignes irréversibles : {', '.join(final) or 'aucune'}")
    lines.append(f"  le plus de personnes qu’une erreur peut toucher : {most(rows) or 'personne'}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report("accès accordé", GRANTED))
    print()
    print(report("accès nécessaire à la tâche", NEEDED))
