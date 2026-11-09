#!/usr/bin/env python3
"""Ajoute le terme anglais entre parenthèses à la première mention d’un terme.

Règle du lexique : quand un terme traduit est technique ou peu courant en
français, la leçon donne le terme anglais entre parenthèses à sa première
mention dans le texte courant, par exemple « flagornerie (sycophancy) ». Le
script parcourt les leçons données, cherche la première mention de chaque
terme de la table dans une ligne de texte courant (hors code, titres,
tableaux et propriétés des composants) et ajoute l’anglais s’il n’y est pas
déjà.

  docs/traduction/outils/termes_anglais.py site/src/content/docs/concepts/*.mdx
"""

import re
import sys
from pathlib import Path

# (terme français, terme anglais). L’ordre compte : un terme long passe avant
# un terme court qu’il contient.
TERMES = [
    ("date limite des connaissances", "knowledge cutoff"),
    ("dilution des instructions", "instruction dilution"),
    ("dégradation du contexte", "context rot"),
    ("mise en cache du prompt", "prompt caching"),
    ("coût croissant d’une session", "growing session cost"),
    ("vérification par sondage", "spot-check"),
    ("fenêtre de contexte", "context window"),
    ("échelle d’autonomie", "autonomy scale"),
    ("degré d’autonomie", "degree of autonomy"),
    ("modèle sans état", "stateless model"),
    ("requête au modèle", "model request"),
    ("gabarit de prompt", "prompt template"),
    ("sortie structurée", "structured output"),
    ("niveau d’effort", "effort level"),
    ("boucle d’agent", "agent loop"),
    ("appel d’outil", "tool call"),
    ("prompt système", "system prompt"),
    ("style maison", "house style"),
    ("échantillonnage", "sampling"),
    ("flagornerie", "sycophancy"),
    ("délimiteur", "delimiter"),
    ("sous-agent", "subagent"),
    ("harnais", "harness"),
    ("ancrage", "grounding"),
    ("jetons d’accès", "access tokens"),
    ("jeton", "token"),
    ("IA fantôme", "shadow AI"),
    ("masquage", "redaction"),
    ("table de correspondance", "redaction map"),
    ("responsable du traitement", "controller"),
    ("sous-traitant", "processor"),
    ("mention de l’usage de l’IA", "disclosure"),
    ("rayon d’impact", "blast radius"),
    ("moindre privilège", "least privilege"),
    ("humain dans la boucle", "human in the loop"),
    ("injection de prompt", "prompt injection"),
    ("dépendance excessive", "overreliance"),
    ("complaisance envers l’automatisation", "automation complacency"),
    ("garde-fous", "guardrails"),
    ("jeu de référence", "golden set"),
    ("grille d’évaluation", "rubric"),
]

PROSE = re.compile(r"^(\*\*|«|\(|\d+\. |- |[A-Za-zÀ-ÿ’])")


def prose_lines(lines: list[str]) -> list[int]:
    """Indexes of the running-text lines: outside fences, JSX tags, tables and headings."""
    out, fence, in_tag = [], False, False
    for i, line in enumerate(lines):
        s = line.rstrip("\n")
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if in_tag:
            if s.rstrip().endswith(">") and not s.rstrip().endswith("=>"):
                in_tag = False
            continue
        if s.startswith("<") and not s.startswith("</"):
            if not s.rstrip().endswith(">"):
                in_tag = True
            continue
        if s.startswith(("import ", "#", "|", "{", "}", "</")):
            continue
        if PROSE.match(s):
            out.append(i)
    return out


def annotate(text: str) -> tuple[str, list[str]]:
    lines = text.split("\n")
    prose = prose_lines(lines)
    added = []
    for fr, en in TERMES:
        after = r"(?! d’accès)" if fr == "jeton" else ""
        word = r"(?<![\w’-])(" + re.escape(fr) + r")(s|x)?(?![\w’-])"
        pat = re.compile(word + after, re.IGNORECASE)
        done = False
        for i in prose:
            for m in pat.finditer(lines[i]):
                before = lines[i][: m.start()]
                # Inside inline code or a link label: look further.
                if before.count("`") % 2 or before.count("[") > before.count("]"):
                    continue
                end = m.end()
                rest = lines[i][end:]
                if rest.startswith("**"):
                    end += 2
                    rest = rest[2:]
                if re.match(r"\s*»?\s*\(", rest):
                    done = True
                    break
                word = en + "s" if m.group(2) and not en.endswith("s") else en
                lines[i] = lines[i][:end] + f" ({word})" + lines[i][end:]
                added.append(f"{fr} ({word})")
                done = True
                break
            if done:
                break
    return "\n".join(lines), added


def main(paths: list[str]) -> None:
    for p in map(Path, paths):
        text = p.read_text(encoding="utf-8")
        new, added = annotate(text)
        if added:
            p.write_text(new, encoding="utf-8")
            print(f"{p.name}: {', '.join(added)}")


if __name__ == "__main__":
    main(sys.argv[1:])
