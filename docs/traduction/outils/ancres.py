#!/usr/bin/env python3
"""Met à jour les ancres de section après la traduction des titres.

Une page traduite garde les mêmes titres de section, dans le même ordre, que
la page anglaise de `upstream/main`. Le slug de chaque titre change avec la
traduction, et ce slug sert d’ancre (`/concepts/how-models-work/#...`) et de
valeur aux champs `section:` des YAML de leçon (spec S11).

Le script calcule, pour chaque page traduite, la correspondance entre les
anciens et les nouveaux slugs, puis réécrit :

- les liens `/<page>/#<ancien>` dans toutes les pages et tous les YAML ;
- les liens internes `(#<ancien>)` dans la page elle-même ;
- les champs `section: <ancien>` qui suivent `lesson: <page>` dans les YAML.

Le slug reproduit `github-slugger`, que le site utilise : minuscules, on garde
les lettres, chiffres, marques, `-` et `_`, et les espaces deviennent `-`.
Un titre répété reçoit `-1`, `-2`, etc.

Usage : docs/traduction/outils/ancres.py [--verifier] <page.mdx>...
Avec --verifier, le script signale seulement les ancres cassées.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
DOCS = RACINE / "site/src/content/docs"
DATA = RACINE / "site/src/data"
REF = "upstream/main"

TITRE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
CLOTURE = re.compile(r"^\s*(```|~~~)")


def texte_du_titre(brut: str) -> str:
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", brut)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = t.replace("`", "")
    t = re.sub(r"(\*\*|__|\*|_)(.+?)\1", r"\2", t)
    t = re.sub(r"(?<!-)--(?!-)", "—", t)
    return t


def slugifier(texte: str) -> str:
    sortie = []
    for ch in texte.lower():
        if ch in "-_ " or unicodedata.category(ch)[0] in "LMN":
            sortie.append(ch)
    return "".join(sortie).replace(" ", "-")


def titres(source: str) -> list[tuple[int, str]]:
    """(niveau, slug) de chaque titre, dans l’ordre, hors blocs de code."""
    vus: dict[str, int] = {}
    sortie = []
    dans_code = False
    for ligne in source.splitlines():
        if CLOTURE.match(ligne):
            dans_code = not dans_code
            continue
        if dans_code:
            continue
        m = TITRE.match(ligne)
        if not m:
            continue
        base = slugifier(texte_du_titre(m.group(2)))
        slug = base
        if base in vus:
            vus[base] += 1
            slug = f"{base}-{vus[base]}"
        else:
            vus[base] = 0
        sortie.append((len(m.group(1)), slug))
    return sortie


def id_de_page(chemin: Path) -> str:
    rel = chemin.resolve().relative_to(DOCS)
    return str(rel.with_suffix("")).removesuffix("/index").removesuffix("index")


def source_anglaise(chemin: Path) -> str:
    rel = chemin.resolve().relative_to(RACINE)
    return subprocess.run(
        ["git", "show", f"{REF}:{rel}"], cwd=RACINE, capture_output=True, text=True, check=True
    ).stdout


def correspondance(chemin: Path) -> dict[str, str]:
    avant = titres(source_anglaise(chemin))
    apres = titres(chemin.read_text(encoding="utf-8"))
    if [n for n, _ in avant] != [n for n, _ in apres]:
        raise SystemExit(
            f"{chemin}: les titres ne correspondent pas à l’anglais "
            f"({len(avant)} titres avant, {len(apres)} après, ou niveaux différents)."
        )
    return {a: b for (_, a), (_, b) in zip(avant, apres, strict=True) if a != b}


def fichiers_cibles() -> list[Path]:
    return [*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx"), *DATA.rglob("*.yaml")]


def reecrire(pages: list[Path]) -> None:
    cartes = {id_de_page(p): (p.resolve(), correspondance(p)) for p in pages}
    for fichier in fichiers_cibles():
        texte = fichier.read_text(encoding="utf-8")
        nouveau = texte
        for page, (chemin, carte) in cartes.items():
            for ancien, neuf in carte.items():
                nouveau = re.sub(
                    rf"(/{re.escape(page)}/#){re.escape(ancien)}(?=[)\s\"'`]|$)",
                    rf"\g<1>{neuf}",
                    nouveau,
                )
                if fichier.resolve() == chemin:
                    nouveau = re.sub(rf"\(#{re.escape(ancien)}\)", f"(#{neuf})", nouveau)
                if fichier.suffix == ".yaml":
                    nouveau = re.sub(
                        rf"(lesson:\s*{re.escape(page)}\s*\n\s*section:\s*){re.escape(ancien)}\b",
                        rf"\g<1>{neuf}",
                        nouveau,
                    )
        if nouveau != texte:
            fichier.write_text(nouveau, encoding="utf-8")
            print(f"mis à jour : {fichier.relative_to(RACINE)}")


def verifier() -> int:
    """Signale les liens /page/#ancre et les section: qui ne visent aucun titre."""
    slugs: dict[str, set[str]] = {}
    for p in [*DOCS.rglob("*.md"), *DOCS.rglob("*.mdx")]:
        source = p.read_text(encoding="utf-8")
        # Les questions de contrôle et les habitudes ont aussi une ancre : leur `id`.
        ids = set(re.findall(r'\bid="([^"]+)"', source))
        slugs[id_de_page(p)] = {s for _, s in titres(source)} | ids
    erreurs = 0
    lien = re.compile(r"\]\(/([a-z0-9/-]+?)/#([^)\s]+)\)")
    section = re.compile(r"lesson:\s*([a-z0-9/-]+)\s*\n\s*section:\s*(\S+)")
    for fichier in fichiers_cibles():
        texte = fichier.read_text(encoding="utf-8")
        trouves = [*lien.findall(texte)]
        if fichier.suffix == ".yaml":
            trouves += section.findall(texte)
        for page, ancre in trouves:
            if page == "glossary" or page not in slugs:
                continue
            if ancre not in slugs[page]:
                erreurs += 1
                print(f"{fichier.relative_to(RACINE)} : /{page}/#{ancre} ne vise aucun titre")
    print(f"{erreurs} ancre(s) cassée(s)")
    return 1 if erreurs else 0


def main(args: list[str]) -> int:
    if args and args[0] == "--verifier":
        return verifier()
    if not args:
        print(__doc__)
        return 2
    reecrire([Path(a) for a in args])
    return verifier()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
