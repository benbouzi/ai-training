"""The toy agent behind the lesson "Watch a tiny agent work".

A scripted stand-in for a model, two tools (list a directory, read a file)
and a loop that runs each tool the model asks for and hands the result
back, until the model says it is done, the step limit is reached, or the
script runs out. The lesson page shows the transcripts this prints.

Run one of the scripted tasks with:  python3 tiny_agent.py <run>
where run is one of the names in RUNS below.
"""

import sys
from pathlib import Path
from typing import Callable, NamedTuple, Optional

HERE = Path(__file__).resolve().parent

# Each tool is a function plus the description the model reads.
TOOL_DESCRIPTIONS = {
    "list_dir": "List the files in a directory. Parameter: path, the directory to list.",
    "read_file": "Return the text of one file. Parameter: path, the file to read.",
}


def list_dir(path: str) -> str:
    target = HERE / path
    if not target.is_dir():
        return f"erreur : {path} n’est pas un dossier"
    return ", ".join(sorted(p.name for p in target.iterdir() if p.is_file()))


def read_file(path: str) -> str:
    target = HERE / path
    if not target.is_file():
        return f"erreur : {path} n’est pas un fichier"
    return target.read_text(encoding="utf-8").strip()


TOOLS: dict[str, Callable[[str], str]] = {"list_dir": list_dir, "read_file": read_file}

# A scripted model: a fixed list of replies, one per step. A reply is either a
# tool request (tool name, path) or a final answer (None, text).
Reply = tuple[Optional[str], str]


class Run(NamedTuple):
    task: str
    max_steps: int
    script: list[Reply]


RUNS: dict[str, Run] = {
    "find": Run(
        task="Quelle note de réunion mentionne la livraison de juin ?",
        max_steps=6,
        script=[
            ("list_dir", "notes"),
            ("read_file", "notes/2026-03-14-lantern.txt"),
            (None, "La note du 14 mars : la livraison des cartes capteurs passe d’avril à juin."),
        ],
    ),
    "count": Run(
        task="Combien de notes de réunion portent sur le projet Lantern ?",
        max_steps=6,
        script=[
            ("list_dir", "notes"),
            ("read_file", "notes/2026-03-14-lantern.txt"),
            ("read_file", "notes/2026-03-21-budget.txt"),
            ("read_file", "notes/2026-03-28-lantern.txt"),
            (None, "Deux des trois notes portent sur le projet Lantern : le 14 et le 28 mars."),
        ],
    ),
    "limit": Run(
        task="Qui confirme la date de livraison ?",
        max_steps=3,
        script=[
            ("list_dir", "notes"),
            ("list_dir", "notes"),
            ("read_file", "notes/2026-03-21-budget.txt"),
            ("read_file", "notes/2026-03-14-lantern.txt"),
            (None, "Ana confirme la date de livraison d’ici vendredi."),
        ],
    ),
}


def run(task: str, script: list[Reply], max_steps: int) -> list[str]:
    """Run the loop for one task and return the transcript, one line per entry."""
    lines = [f"tâche : {task}"]
    for step, (tool_name, text) in enumerate(script, start=1):
        if step > max_steps:
            limit = f"la limite de {max_steps} étapes est atteinte"
            lines.append(f"boucle : arrêt, {limit}, pas de réponse")
            return lines
        if tool_name is None:
            lines.append(f"{step}. modèle : terminé. {text}")
            lines.append(f"boucle : arrêt, le modèle a dit avoir terminé après {step} étapes")
            return lines
        lines.append(f'{step}. modèle : appelle {tool_name} avec le chemin "{text}"')
        tool = TOOLS[tool_name]
        result = tool(text)
        lines.append(f"   boucle : a exécuté {tool_name}, résultat : {result}")
    lines.append("boucle : arrêt, le script est épuisé")
    return lines


def transcript(name: str) -> str:
    spec = RUNS[name]
    return "\n".join(run(spec.task, spec.script, spec.max_steps))


def main(argv: list[str]) -> None:
    name = argv[1] if len(argv) > 1 else "find"
    if name not in RUNS:
        sys.exit(f"unknown run {name!r}, expected one of: {', '.join(RUNS)}")
    print(transcript(name))


if __name__ == "__main__":
    main(sys.argv)
