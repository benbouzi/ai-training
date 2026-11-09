"""Score three proposed AI use cases against a risk threshold.

The fixture behind the lesson "Assessing the risk of a use case before it
starts". Each use case names the domains it touches and the people it
affects, and carries an impact rating and a likelihood rating on four-point
scales. The level is impact times likelihood, and a level at or above the
threshold needs extra controls or a written acceptance.

Nothing here talks to a model or to the network. The ratings are the
lesson's own worked example, and the output is what the page shows.
"""

IMPACT = {1: "mineur", 2: "modéré", 3: "majeur", 4: "grave"}
LIKELIHOOD = {1: "rare", 2: "possible", 3: "probable", 4: "presque certain"}
THRESHOLD = 8


def band(level):
    """Name the band a level falls in."""
    if level >= 12:
        return "très élevé"
    if level >= THRESHOLD:
        return "élevé"
    if level >= 4:
        return "moyen"
    return "faible"


# name, domains, affected, impact, likelihood
USE_CASES = [
    (
        "résumé de réunions",
        "données personnelles, réputation",
        "tous les participants aux réunions, et toute personne évoquée en entretien individuel",
        3,
        3,
    ),
    (
        "rédaction de la lettre interne",
        "réputation",
        "le personnel qui lit la lettre interne",
        2,
        2,
    ),
    (
        "agent de messagerie clients",
        "données personnelles, argent, réputation",
        "chaque client qui écrit, et l’équipe d’assistance",
        4,
        3,
    ),
]


def report(name, domains, affected, impact, likelihood):
    """Print one scored use case."""
    level = impact * likelihood
    print("cas d’usage : " + name)
    print("  domaines : " + domains)
    print("  personnes touchées : " + affected)
    print(f"  impact : {impact} ({IMPACT[impact]})")
    print(f"  probabilité : {likelihood} ({LIKELIHOOD[likelihood]})")
    print(f"  niveau : {level} ({band(level)})")
    print("  au seuil ou au-dessus : " + ("oui" if level >= THRESHOLD else "non"))


def main():
    print(f"seuil : {THRESHOLD} ({band(THRESHOLD)})")
    for name, domains, affected, impact, likelihood in USE_CASES:
        print()
        report(name, domains, affected, impact, likelihood)


if __name__ == "__main__":
    main()
