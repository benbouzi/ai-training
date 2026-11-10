#!/usr/bin/env python3
# ruff: noqa: E501  (la table cite des libellés entiers, qu’on ne peut pas couper)
"""Traduit les libellés de l’interface des leçons, puis les tests qui les citent.

Chaque entrée est (fichier source, ancien texte, nouveau texte). Le script
remplace l’ancien texte dans le fichier source, puis le même texte dans les
tests unitaires (`site/tests/`) et les tests navigateur (`site/e2e/`) qui le
citent mot pour mot. Une entrée dont l’ancien texte est absent du fichier
source arrête le script, pour qu’une mise à jour du dépôt d’origine qui
change un libellé se voie.

Usage : docs/traduction/outils/interface.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[3]
SITE = RACINE / "site"
TESTS = [*(SITE / "tests").rglob("*.ts"), *(SITE / "e2e").rglob("*.ts")]

C = "src/components/lesson/"
OV = "src/components/overrides/"
S = "src/scripts/"

# (fichier, ancien, nouveau, aussi dans les tests)
TABLE: list[tuple[str, str, str, bool]] = [
    # Cadre commun des questions de contrôle
    (C + "CheckpointShell.astro", "checkLabel = 'Check',", "checkLabel = 'Vérifier',", False),
    (
        C + "CheckpointShell.astro",
        'aria-expanded="false">Hint</button>',
        'aria-expanded="false">Indice</button>',
        True,
    ),
    (
        C + "CheckpointShell.astro",
        'class="cp-skip">Skip</button>',
        'class="cp-skip">Passer</button>',
        True,
    ),
    (
        C + "CheckpointShell.astro",
        'class="cp-giveup" hidden>Give up</button>',
        'class="cp-giveup" hidden>Voir la réponse</button>',
        True,
    ),
    (C + "CheckpointShell.astro", ">Open in the lesson</a>", ">Ouvrir dans la leçon</a>", True),
    (
        C + "Predict.astro",
        "checkLabel={honor ? 'Record' : 'Check'}",
        "checkLabel={honor ? 'Enregistrer' : 'Vérifier'}",
        False,
    ),
    (C + "Repair.astro", 'checkLabel="Record grade"', 'checkLabel="Enregistrer la note"', False),
    (C + "Scenario.astro", 'checkLabel="Decide"', 'checkLabel="Décider"', False),
    # Blocs de leçon
    (C + "Recap.astro", "<h2>Recap</h2>", "<h2>À retenir</h2>", True),
    (
        C + "Recap.astro",
        "<strong>You can now</strong>",
        "<strong>Vous savez maintenant</strong>",
        True,
    ),
    (
        C + "Recap.astro",
        "data-finish>Mark lesson finished</button>",
        "data-finish>Marquer la leçon comme terminée</button>",
        True,
    ),
    (
        C + "Recap.astro",
        "data-skip-lesson>I know this, skip it</button>",
        "data-skip-lesson>Je connais déjà, passer</button>",
        True,
    ),
    (C + "Exercise.astro", "<h2>Exercise</h2>", "<h2>Exercice</h2>", True),
    (
        C + "Exercise.astro",
        "<strong>Stretch:</strong>",
        "<strong>Pour aller plus loin :</strong>",
        True,
    ),
    (
        C + "Pitfall.astro",
        "aria-label={`Pitfall: ${title}`}",
        "aria-label={`Piège : ${title}`}",
        False,
    ),
    (
        C + "Pitfall.astro",
        '<p class="pitfall-title">Pitfall: {title}</p>',
        '<p class="pitfall-title">Piège : {title}</p>',
        False,
    ),
    (
        C + "Prompt.astro",
        "'Prompt (illustrative, not a recorded transcript)'",
        "'Prompt (illustration écrite pour la leçon)'",
        True,
    ),
    (
        C + "Prompt.astro",
        "`Prompt · ${model}, recorded ${recorded}`",
        "`Prompt · ${model}, enregistré en ${recorded}`",
        False,
    ),
    (
        C + "Response.astro",
        "<figcaption>Response</figcaption>",
        "<figcaption>Réponse</figcaption>",
        True,
    ),
    (
        C + "Habit.astro",
        '<p class="habit-title">Habit</p>',
        '<p class="habit-title">Habitude</p>',
        True,
    ),
    (C + "Habit.astro", "data-habit-done>Done</button>", "data-habit-done>Fait</button>", True),
    (C + "Habit.astro", "data-habit-skip>Skip</button>", "data-habit-skip>Passer</button>", True),
    (
        C + "MorePractice.astro",
        "<h2>More practice</h2>",
        "<h2>Pour s’entraîner davantage</h2>",
        True,
    ),
    (
        C + "MorePractice.astro",
        "Extra checkpoints on the same ideas, if you want them. You can finish the lesson without them.",
        "Des questions de contrôle en plus sur les mêmes idées, si vous le souhaitez. Vous pouvez terminer la leçon sans elles.",
        True,
    ),
    (C + "Match.astro", "Choose…", "Choisir…", True),
    (
        C + "Sort.astro",
        "Unplaced (drag an item to a bucket, or select it and then click the bucket)",
        "Non classés (faites glisser un élément vers une case, ou sélectionnez-le puis cliquez sur la case)",
        True,
    ),
    (C + "Order.astro", 'aria-label="Steps to order"', 'aria-label="Étapes à ordonner"', True),
    (C + "Order.astro", 'aria-label={`Move "${s}" up`}', "aria-label={`Monter « ${s} »`}", False),
    (
        C + "Order.astro",
        'aria-label={`Move "${s}" down`}',
        "aria-label={`Descendre « ${s} »`}",
        False,
    ),
    (C + "RouteAhead.astro", "You are ahead. Next:", "Vous êtes en avance. Ensuite :", True),
    (C + "RouteAhead.astro", "(external link)", "(lien externe)", True),
    (C + "RouteAhead.astro", "(not written yet)", "(pas encore écrite)", True),
    (C + "TutorBlock.astro", ">Study with the tutor</a>", ">Étudier avec le tuteur</a>", True),
    (
        C + "TutorBlock.astro",
        'aria-label="Copy the /ai-tutor line">Copy</button>',
        'aria-label="Copier la ligne /ai-tutor">Copier</button>',
        True,
    ),
    (
        OV + "MarkdownContent.astro",
        "data-skills-title>Skip ahead?</p>",
        "data-skills-title>Passer directement ?</p>",
        True,
    ),
    (
        OV + "MarkdownContent.astro",
        "data-skills-dismiss>Not now</button>",
        "data-skills-dismiss>Pas maintenant</button>",
        True,
    ),
    (
        OV + "MarkdownContent.astro",
        '<p class="route-title">Worth revisiting first</p>',
        '<p class="route-title">À revoir d’abord</p>',
        True,
    ),
    (
        OV + "MarkdownContent.astro",
        '<span class="route-where">in {b.lessonTitle}</span>',
        '<span class="route-where">dans « {b.lessonTitle} »</span>',
        False,
    ),
    # Widget de l’échantillonneur
    ("src/components/widgets/Sampler.astro", "The cat sat on the …", "Le chat dort sur le …", True),
    (
        "src/components/widgets/Sampler.astro",
        "		Temperature <input",
        "		Température <input",
        True,
    ),
    (
        "src/components/widgets/Sampler.astro",
        ">Sample next token</button>",
        ">Tirer le jeton suivant</button>",
        True,
    ),
    (
        S + "sampler-logic.ts",
        "return `The cat sat on the${token}.`;",
        "return `Le chat dort sur le${token}.`;",
        False,
    ),
    (
        S + "sampler-logic.ts",
        "	' mat': 2.0,\n	' sofa': 1.2,\n	' roof': 0.6,\n	' moon': -0.5,\n	' spreadsheet': -1.5,",
        "	' tapis': 2.0,\n	' canapé': 1.2,\n	' toit': 0.6,\n	' quai': -0.5,\n	' tableur': -1.5,",
        False,
    ),
    (
        S + "sampler-logic.ts",
        "export const FALLBACK_TOKEN = ' mat';",
        "export const FALLBACK_TOKEN = ' tapis';",
        False,
    ),
    # Messages des questions de contrôle
    (S + "checkpoints.ts", "'Pick an answer first.'", "'Choisissez d’abord une réponse.'", True),
    (
        S + "checkpoints.ts",
        "'Run it, then say how your prediction held up.'",
        "'Lancez-le, puis dites si votre prédiction a tenu.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Type your prediction first.'",
        "'Tapez d’abord votre prédiction.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Select an item first, then a bucket.'",
        "'Sélectionnez d’abord un élément, puis une case.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Write your fix, then reveal the model answer and compare.'",
        "'Écrivez votre correction, puis affichez la réponse modèle et comparez.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Compare with the model answer and grade yourself.'",
        "'Comparez avec la réponse modèle et notez-vous.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Edit your version and grade again.'",
        "'Modifiez votre version et notez-vous de nouveau.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Right.' : (r.dataset.why ?? 'Not this one.')",
        "'Juste.' : (r.dataset.why ?? 'Pas celle-ci.')",
        False,
    ),
    (
        S + "checkpoints.ts",
        "'Skipped. It stays available, and comes back in review.'",
        "'Passée. Elle reste disponible et reviendra en révision.'",
        True,
    ),
    (S + "checkpoints.ts", "`The answer is marked. ${", "`La réponse est indiquée. ${", False),
    (
        S + "checkpoints.ts",
        "'The correct items are marked.'",
        "'Les bons éléments sont indiqués.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "`Each row now shows its answer. ${",
        "`Chaque ligne affiche maintenant sa réponse. ${",
        False,
    ),
    (
        S + "checkpoints.ts",
        "'The output is shown below.'",
        "'La sortie est affichée ci-dessous.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'The steps are now in the right order.'",
        "'Les étapes sont maintenant dans le bon ordre.'",
        True,
    ),
    (
        S + "checkpoints.ts",
        "'Every item is now in its bucket.'",
        "'Chaque élément est maintenant dans sa case.'",
        True,
    ),
    (
        S + "checkpoint-logic.ts",
        "text: consequence ? `Correct. ${consequence}` : 'Correct.' };",
        "text: consequence ? `Juste. ${consequence}` : 'Juste.' };",
        False,
    ),
    (S + "checkpoint-logic.ts", "'Not quite. Try again.'", "'Pas tout à fait. Réessayez.'", True),
    (
        S + "checkpoint-logic.ts",
        "'Correct. That is exactly the output.'",
        "'Juste. C’est exactement la sortie.'",
        True,
    ),
    (
        S + "checkpoint-logic.ts",
        "'Not quite. Trace it once more.'",
        "'Pas tout à fait. Suivez-le encore une fois.'",
        True,
    ),
    (S + "checkpoint-logic.ts", "'Recorded as a pass.'", "'Enregistrée comme réussie.'", True),
    (
        S + "checkpoint-logic.ts",
        "'Recorded. Adjust your prediction and try once more when you are ready.'",
        "'Enregistrée. Ajustez votre prédiction et réessayez quand vous êtes prêt.'",
        True,
    ),
    (
        S + "checkpoint-logic.ts",
        "'Recorded as partial. Only a pass counts; improve it and grade again.'",
        "'Partielle. Seule une réussite compte : améliorez-la et notez de nouveau.'",
        True,
    ),
    (
        S + "checkpoint-logic.ts",
        "{ kind: 'ok', text: 'Correct order.' } : { kind: 'nope', text: 'Not the right order yet.' }",
        "{ kind: 'ok', text: 'Ordre juste.' } : { kind: 'nope', text: 'Pas encore le bon ordre.' }",
        False,
    ),
    (S + "checkpoint-logic.ts", "'All placed correctly.'", "'Tout est bien classé.'", True),
    (
        S + "checkpoint-logic.ts",
        "'Some items are in the wrong bucket.'",
        "'Certains éléments sont dans la mauvaise case.'",
        True,
    ),
    (
        S + "checkpoint-logic.ts",
        "text: `Pick ${wanted} answers first.` }",
        "text: `Choisissez d’abord ${wanted} réponses.` }",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "'One of your picks is not right.'",
        "'L’un de vos choix n’est pas juste.'",
        True,
    ),
    (
        S + "checkpoint-logic.ts",
        "feedback: { kind: 'ok', text: 'Correct.' } };",
        "feedback: { kind: 'ok', text: 'Juste.' } };",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "text: `Correct. ${rationale}`.trim() }",
        "text: `Juste. ${rationale}`.trim() }",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "const questions = (n: number) => `${n} question${n === 1 ? '' : 's'}`;",
        "const questions = (n: number) => `${n} question${n === 1 ? '' : 's'}`;",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "return `Answer ${questions(open)}`;",
        "return `Répondre à ${questions(open)}`;",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "if (answered < total) return `Passed ${passed} of ${answered} so far.`;",
        "if (answered < total) return `${passed} sur ${answered} réussie${passed > 1 ? 's' : ''} pour l’instant.`;",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "'Every objective is covered. Go on to the recap.' : 'The ones you missed are taught below.'",
        "'Objectifs couverts. Passez à « À retenir ».' : 'Les manques sont enseignés plus bas.'",
        False,
    ),
    (
        S + "checkpoint-logic.ts",
        "return `Passed ${passed} of ${total}. ${tail}`;",
        "return `${passed} sur ${total} réussie${passed > 1 ? 's' : ''}. ${tail}`;",
        False,
    ),
    (S + "checkpoint-logic.ts", "label: 'retired' };", "label: 'acquise' };", False),
    (
        S + "checkpoint-logic.ts",
        "label: `stage ${stage ?? '-'} of 5` };",
        "label: `étape ${stage ?? '-'} sur 5` };",
        False,
    ),
    (
        S + "habits.ts",
        "'Offered once you finish the lesson.'",
        "'Proposée une fois la leçon terminée.'",
        True,
    ),
    (
        S + "habits.ts",
        "return `Next on ${entry?.next ?? ''}.`;",
        "return `Prochaine fois : ${entry?.next ?? ''}.`;",
        False,
    ),
    (
        S + "habits.ts",
        "'Due today. Did you do it?'",
        "'Prévue aujourd’hui. L’avez-vous faite ?'",
        True,
    ),
    (S + "habits.ts", "'Done with this habit.'", "'Habitude acquise.'", True),
    (
        S + "markdown-content-logic.ts",
        "label: finished ? `Finished ✓ (${lesson.at})` : 'Mark lesson finished',",
        "label: finished ? `Terminée ✓ (${lesson.at})` : 'Marquer la leçon comme terminée',",
        False,
    ),
    (
        S + "markdown-content-logic.ts",
        "? `Pass or skip ${open} more checkpoint${open === 1 ? '' : 's'} to finish this lesson.`",
        "? `Réussissez ou passez encore ${open} question${open === 1 ? '' : 's'} de contrôle pour terminer cette leçon.`",
        False,
    ),
    (
        S + "markdown-content-logic.ts",
        "label: lesson?.state === 'skipped' ? `Skipped (${lesson.at})` : 'I know this, skip it',",
        "label: lesson?.state === 'skipped' ? `Passée (${lesson.at})` : 'Je connais déjà, passer',",
        False,
    ),
    (
        S + "markdown-content.ts",
        "'One checkpoint per objective this lesson teaches, one try each. A pass counts as if you answered it in the lesson, and the review schedule picks it up.'",
        "'Une question de contrôle par objectif de cette leçon, un essai chacune. Une réussite compte comme si vous y aviez répondu dans la leçon, et le calendrier de révision la prend en compte.'",
        True,
    ),
    (
        S + "markdown-content.ts",
        "dismiss.textContent = 'Close';",
        "dismiss.textContent = 'Fermer';",
        False,
    ),
    (
        S + "tutor-block.ts",
        "button.textContent = 'Copied';",
        "button.textContent = 'Copié';",
        False,
    ),
    (
        S + "tutor-block.ts",
        "button.textContent = 'Select and copy';",
        "button.textContent = 'Sélectionner et copier';",
        False,
    ),
    # Ligne de révision et sommaire des leçons
    (
        "src/lib/review-line.ts",
        "date.toLocaleDateString('en-US', { dateStyle: 'long', timeZone: 'UTC' })",
        "date.toLocaleDateString('fr-FR', { dateStyle: 'long', timeZone: 'UTC' })",
        False,
    ),
    (
        "src/lib/review-line.ts",
        "const due = `Review due by ${longDate(reviewBy)}.`;",
        "const due = `Révision prévue d’ici le ${longDate(reviewBy)}.`;",
        False,
    ),
    (
        "src/lib/review-line.ts",
        "return `Sources checked on ${longDate(sourcesChecked)}. ${due}`;",
        "return `Sources vérifiées le ${longDate(sourcesChecked)}. ${due}`;",
        False,
    ),
    # Widget du fichier d’instructions (customizing-agents/instructions)
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "Tick what is true for your project and fill in the short fields. The\n      file on the right updates as you type.",
        "Cochez ce qui est vrai pour votre projet et remplissez les champs courts.\n      Le fichier de droite se met à jour pendant que vous tapez.",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>Project name</span>",
        "<span>Nom du projet</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>One line: what it is</span>",
        "<span>En une ligne : ce que c’est</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        'placeholder="Sends monthly invoices as PDF over SMTP."',
        'placeholder="Envoie les factures mensuelles en PDF par SMTP."',
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<legend>Commands</legend>",
        "<legend>Commandes</legend>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>Language and runtime</span>",
        "<span>Langage et environnement d’exécution</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        'placeholder="Python 3.13, dependencies via uv"',
        'placeholder="Python 3.13, dépendances avec uv"',
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>Test command</span>",
        "<span>Commande de test</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>Lint and format command</span>",
        "<span>Commande de style et de mise en forme</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<legend>Rules</legend>",
        "<legend>Règles</legend>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>Branch rule</span>",
        "<span>Règle de branche</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        'placeholder="Never commit to main; branch as feat/… or fix/…"',
        'placeholder="Ne jamais committer sur main, créer des branches feat/… ou fix/…"',
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>Files never to touch</span>",
        "<span>Fichiers à ne jamais modifier</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        'placeholder="migrations/, uv.lock, anything under vendor/"',
        'placeholder="migrations/, uv.lock, tout ce qui est sous vendor/"',
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        "<span>A recurring mistake to stop</span>",
        "<span>Une erreur récurrente à arrêter</span>",
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        'placeholder="Do not add retries around SMTP calls; the queue already retries."',
        'placeholder="Ne pas ajouter de nouvelles tentatives autour des appels SMTP : la file d’attente réessaie déjà."',
        False,
    ),
    (
        "src/components/widgets/InstructionsBuilder.astro",
        'class="ib-copy">Copy</button>',
        'class="ib-copy">Copier</button>',
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "input.name || 'my-project'",
        "input.name || 'mon-projet'",
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "`- Runtime: ${valueOr(l.runtime, '<language and version>')}`",
        "`- Environnement : ${valueOr(l.runtime, '<langage et version>')}`",
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "`- Test: \\`${valueOr(l.test, '<test command>')}\\``",
        "`- Tests : \\`${valueOr(l.test, '<commande de test>')}\\``",
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "`- Lint and format: \\`${valueOr(l.lint, '<lint command>')}\\``",
        "`- Style et mise en forme : \\`${valueOr(l.lint, '<commande de style>')}\\``",
        False,
    ),
    (S + "instructions-builder-logic.ts", "'## Commands'", "'## Commandes'", False),
    (
        S + "instructions-builder-logic.ts",
        "valueOr(l.branch, '<branch rule>')",
        "valueOr(l.branch, '<règle de branche>')",
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "`- Never edit: ${valueOr(l.notouch, '<paths>')}`",
        "`- Ne jamais modifier : ${valueOr(l.notouch, '<chemins>')}`",
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "'<the mistake to stop, and what to do instead>'",
        "'<l’erreur à arrêter, et quoi faire à la place>'",
        False,
    ),
    (S + "instructions-builder-logic.ts", "'## Rules'", "'## Règles'", False),
    (
        S + "instructions-builder-logic.ts",
        "/** The line count next to the file name, counting only lines with text: `1 non-empty line`, `7 non-empty lines`. */",
        "/** The line count next to the file name, counting only lines with text: `1 ligne non vide`, `7 lignes non vides`. French takes the singular for 0 and 1. */",
        False,
    ),
    (
        S + "instructions-builder-logic.ts",
        "return `${n} non-empty line${n === 1 ? '' : 's'}`;",
        "return n > 1 ? `${n} lignes non vides` : `${n} ligne non vide`;",
        False,
    ),
    (
        S + "instructions-builder.ts",
        "copy.textContent = 'Copied';",
        "copy.textContent = 'Copié';",
        False,
    ),
    (
        S + "instructions-builder.ts",
        "copy.textContent = 'Select and copy';",
        "copy.textContent = 'Sélectionnez et copiez';",
        False,
    ),
]

# Remplacements propres aux tests, pour les chaînes construites dans le code.
TESTS_SEULS: list[tuple[str, str]] = [
    ("'The cat sat on the mat.'", "'Le chat dort sur le tapis.'"),
    ("'The cat sat on the spreadsheet.'", "'Le chat dort sur le tableur.'"),
    ("sentence(' mat')", "sentence(' tapis')"),
    ("'Correct.'", "'Juste.'"),
    ("'Correct order.'", "'Ordre juste.'"),
    ("'Not the right order yet.'", "'Pas encore le bon ordre.'"),
]

# Remplacements propres à un fichier de test, pour les chaînes trop courantes
# pour être remplacées dans tous les tests (comme « Copy »).
TESTS_PAR_FICHIER: list[tuple[str, str, str]] = [
    *[
        (f, a, n)
        for f in (
            "tests/scripts/instructions-builder.test.ts",
            "tests/scripts/instructions-builder-logic.test.ts",
        )
        for a, n in [
            ("my-project", "mon-projet"),
            ("## Commands", "## Commandes"),
            ("## Rules", "## Règles"),
            ("- Runtime: <language and version>", "- Environnement : <langage et version>"),
            ("- Test: `", "- Tests : `"),
            ("- Lint and format: `", "- Style et mise en forme : `"),
            ("<test command>", "<commande de test>"),
            ("<lint command>", "<commande de style>"),
            ("<branch rule>", "<règle de branche>"),
            ("- Never edit: ", "- Ne jamais modifier : "),
            ("<paths>", "<chemins>"),
            (
                "<the mistake to stop, and what to do instead>",
                "<l’erreur à arrêter, et quoi faire à la place>",
            ),
            ("'5 non-empty lines'", "'5 lignes non vides'"),
            ("'2 non-empty lines'", "'2 lignes non vides'"),
            ("'3 non-empty lines'", "'3 lignes non vides'"),
            ("'1 non-empty line'", "'1 ligne non vide'"),
            ("'0 non-empty lines'", "'0 ligne non vide'"),
            (
                "uses the singular for one line and the plural for none",
                "uses the singular for one line or none, as French does",
            ),
        ]
    ],
    ("tests/scripts/instructions-builder.test.ts", "toBe('Copied')", "toBe('Copié')"),
    (
        "tests/scripts/instructions-builder.test.ts",
        "toBe('Select and copy')",
        "toBe('Sélectionnez et copiez')",
    ),
    ("tests/scripts/instructions-builder.test.ts", "toBe('Copy')", "toBe('Copier')"),
]


def main() -> int:
    manquants = 0
    for rel, ancien, neuf, _ in TABLE:
        chemin = SITE / rel
        texte = chemin.read_text(encoding="utf-8")
        if ancien == neuf:
            continue
        if ancien not in texte:
            if neuf in texte:
                continue
            print(f"absent : {rel} : {ancien[:60]}")
            manquants += 1
            continue
        chemin.write_text(texte.replace(ancien, neuf), encoding="utf-8")
    paires = [(a, n) for _, a, n, t in TABLE if t] + TESTS_SEULS
    for test in TESTS:
        texte = test.read_text(encoding="utf-8")
        nouveau = texte
        for ancien, neuf in paires:
            nouveau = nouveau.replace(ancien, neuf)
        if nouveau != texte:
            test.write_text(nouveau, encoding="utf-8")
            print(f"test mis à jour : {test.relative_to(RACINE)}")
    for rel, ancien, neuf in TESTS_PAR_FICHIER:
        chemin = SITE / rel
        texte = chemin.read_text(encoding="utf-8")
        if ancien in texte:
            chemin.write_text(texte.replace(ancien, neuf), encoding="utf-8")
            print(f"test mis à jour : {chemin.relative_to(RACINE)}")
    return 1 if manquants else 0


if __name__ == "__main__":
    sys.exit(main())
