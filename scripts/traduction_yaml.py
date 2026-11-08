#!/usr/bin/env python3
"""Extrait et réinjecte les champs à traduire des YAML de données.

Les YAML sous `site/src/data/` mêlent des identifiants (à garder) et des
textes affichés (à traduire). Ce script ne touche qu’aux textes affichés.

  scripts/traduction_yaml.py extraire <fichier.yaml>... > a-traduire.json
  scripts/traduction_yaml.py injecter traductions.json

Le JSON a la forme {"chemin/du/fichier.yaml": [[["concepts", 0, "name"], "texte"], ...]}.
À l’injection, chaque texte remplace la valeur au chemin donné. La mise en
forme du fichier est gardée (ruamel.yaml en aller-retour), et un texte qui
était en bloc replié `>-` le reste, coupé vers 100 colonnes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import FoldedScalarString

RACINE = Path(__file__).resolve().parent.parent

# Clés dont la valeur est un texte affiché, quel que soit leur niveau.
TEXTES = {
    "name",
    "title",
    "description",
    "definition",
    "statement",
    "claim",
    "why",
    "example",
    "brief",
    "label",
    "audience",
}
# Clés dont la valeur est une liste de textes affichés.
LISTES = {"shorts"}


def yaml_rt() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.width = 100
    y.indent(mapping=2, sequence=4, offset=2)
    return y


def parcourir(noeud, chemin, sortie):
    if isinstance(noeud, dict):
        for cle, val in noeud.items():
            if cle in TEXTES and isinstance(val, str):
                sortie.append([[*chemin, cle], str(val)])
            elif cle in LISTES and isinstance(val, list):
                for i, v in enumerate(val):
                    if isinstance(v, str):
                        sortie.append([[*chemin, cle, i], str(v)])
            else:
                parcourir(val, [*chemin, cle], sortie)
    elif isinstance(noeud, list):
        for i, val in enumerate(noeud):
            parcourir(val, [*chemin, i], sortie)


def extraire(fichiers: list[str]) -> None:
    y = yaml_rt()
    resultat = {}
    for f in fichiers:
        chemin = Path(f).resolve()
        champs: list = []
        parcourir(y.load(chemin.read_text(encoding="utf-8")), [], champs)
        resultat[str(chemin.relative_to(RACINE))] = champs
    json.dump(resultat, sys.stdout, ensure_ascii=False, indent=1)
    print()


def replie(texte: str, largeur: int = 96) -> FoldedScalarString:
    s = FoldedScalarString(texte)
    positions = []
    debut = 0
    dernier = None
    for i, ch in enumerate(texte):
        if ch == " ":
            if i - debut > largeur and dernier is not None:
                positions.append(dernier)
                debut = dernier + 1
            dernier = i
    if len(texte) - debut > largeur and dernier is not None and dernier > debut:
        positions.append(dernier)
    s.fold_pos = positions
    return s


def injecter(source: str) -> None:
    y = yaml_rt()
    donnees = json.loads(Path(source).read_text(encoding="utf-8"))
    for rel, champs in donnees.items():
        chemin = RACINE / rel
        doc = y.load(chemin.read_text(encoding="utf-8"))
        for acces, texte in champs:
            parent = doc
            for cle in acces[:-1]:
                parent = parent[cle]
            ancien = parent[acces[-1]]
            if isinstance(ancien, FoldedScalarString) or len(texte) > 90:
                parent[acces[-1]] = replie(texte)
            else:
                parent[acces[-1]] = texte
        with chemin.open("w", encoding="utf-8") as sortie:
            y.dump(doc, sortie)
        print(f"injecté : {rel} ({len(champs)} champs)")


def main(args: list[str]) -> int:
    if len(args) >= 2 and args[0] == "extraire":
        extraire(args[1:])
        return 0
    if len(args) == 2 and args[0] == "injecter":
        injecter(args[1])
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
