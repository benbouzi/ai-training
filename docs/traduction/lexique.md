# Traduction française : règles et lexique

Ce fichier fixe les choix de traduction du site. Toute page traduite les
suit, pour que les termes restent les mêmes d’une page à l’autre. Un
changement de terme se fait ici d’abord, puis dans toutes les pages.

## Ce qui ne se traduit pas

- Les noms de fichiers, les adresses des pages (slugs) et les identifiants :
  `id`, `objective`, `concepts={[...]}`, `covers`, `serves`, `phase`,
  les clés de citation `(@Academy ai-capabilities-and-limitations)`.
- Le code, les commandes, les sorties de programme réelles et les fichiers
  d’exemple sous `site/examples/`.
- Les noms de produits, d’outils et de formats : Claude Code, opencode, MCP,
  AGENTS.md, JSON, YAML.
- Les titres des références bibliographiques.
- Les champs `notes` des fichiers YAML, qui servent aux auteurs et ne
  s’affichent pas.

## Ce qui se traduit

- Le texte des leçons, y compris les titres de section, les propriétés
  textuelles des composants (`title`, `hint`, `context`, `text`, `why`,
  `steps`, etc.) et les prompts d’exemple que l’apprenant lit ou recopie.
- Les réponses de modèle données comme illustration dans la prose.
- Dans les YAML : `name`, `title`, `description`, `definition`,
  `statement`, `claim`, `why`, `example`, `brief`, `shorts`, et les titres
  des parties de parcours.
- Les libellés de l’interface dans les composants.

## Règles d’écriture

- Vouvoiement. Phrases simples, vocabulaire courant, registre professionnel.
- Pas de tiret cadratin ni demi-cadratin comme ponctuation. Une virgule, deux
  points, des parenthèses ou deux phrases.
- Pas de construction en balancement (« non pas X mais Y », « X ne remplace
  pas Y, il permet Z »). On énonce l’affirmation positive.
- Apostrophe typographique `’` partout dans le texte français, y compris dans
  les chaînes des propriétés JSX, où une apostrophe droite casserait la
  chaîne entre apostrophes.
- Guillemets français « » pour les citations et les mots cités.
- Un sigle est développé à sa première occurrence dans une leçon.
- Les titres de section changent l’ancre de la page. Après traduction, le
  script `docs/traduction/outils/ancres.py` met à jour les ancres et les champs
  `section:` des YAML.
- Le nom d’un concept dans le YAML du thème doit apparaître tel quel (au
  singulier) dans la leçon qui le couvre : le site transforme sa première
  mention en lien vers le glossaire.

## Exemples et sorties de programme

Les fichiers d’exemple (`site/examples/`) alimentent les widgets et les blocs
de sortie des leçons, et `mise run examples` vérifie que chaque ligne qu’un
script affiche figure dans un bloc `text` de la page. Quand le contenu d’un
exemple se traduit (notes, politiques, prompts), le script et la page changent
ensemble :

- Les données lues par le programme sont traduites (textes de notes, tâches,
  questions). Les étiquettes que le programme affiche (`task:`, `loop: ran`,
  `ok`, `FAIL`, `match`) restent en anglais, comme dans un vrai outil, et la
  leçon en donne le sens à leur première apparition.
- Les noms de champs d’un format d’import (`owner`, `task`, `due`,
  `priority`) et leurs valeurs (`high`, `medium`, `low`) restent en anglais.
- Après une modification, on relance le script et on recopie sa sortie telle
  quelle dans la leçon.

## Outils

- `docs/traduction/outils/ancres.py` : met à jour les ancres après la
  traduction des titres, et vérifie qu’aucun lien ne vise une ancre absente.
- `docs/traduction/outils/yaml_champs.py` : extrait les champs affichés des
  YAML en JSON, puis réinjecte la traduction sans toucher au reste du fichier.
- `docs/traduction/outils/interface.py` : table des libellés de l’interface,
  appliquée aux composants et aux tests qui les citent.

## Structure du site

| Anglais | Français |
| --- | --- |
| Foundations | Fondamentaux |
| Engineering | Ingénierie |
| area | domaine |
| course | parcours |
| lesson | leçon |
| topic | thème |
| topic map | carte des thèmes |
| competency | compétence |
| objective | objectif |
| behavior | comportement attendu |
| learner | apprenant |
| checkpoint | question de contrôle |
| recap | à retenir |
| pitfall | piège |
| exercise | exercice |
| hint | indice |
| review | révision |
| Concepts | Concepts |
| Safety | Sécurité |
| Using agents | Utiliser des agents |
| Coding with agents | Coder avec des agents |
| Customizing agents | Personnaliser des agents |
| Building agents | Construire des agents |

## Modèles et prompts

| Anglais | Français |
| --- | --- |
| language model | modèle de langage |
| large language model (LLM) | grand modèle de langage (LLM) |
| prompt | prompt (masculin) |
| prompting | rédaction de prompts |
| system prompt | prompt système |
| instruction | instruction |
| example (few-shot) | exemple (few-shot) |
| role | rôle |
| iteration | itération |
| structured output | sortie structurée |
| prompt template | gabarit de prompt |
| delimiter | délimiteur |
| house style | style maison |
| token | jeton |
| input / output tokens | jetons d’entrée / de sortie |
| context window | fenêtre de contexte |
| training / inference | entraînement / inférence |
| weights | poids |
| model family and size | famille et taille de modèle |
| sampling / temperature | échantillonnage / température |
| hallucination | hallucination |
| knowledge cutoff | date limite des connaissances |
| non-determinism | non-déterminisme |
| sycophancy | flagornerie |
| latency | latence |
| instruction dilution | dilution des instructions |
| factuality / faithfulness | factualité / fidélité |
| prompt caching | mise en cache du prompt |
| effort level | niveau d’effort |
| growing session cost | coût croissant d’une session |
| retrieval (RAG) | récupération (RAG, génération augmentée par récupération) |
| grounding | ancrage |
| short- / long-term memory | mémoire à court / long terme |
| context rot | dégradation du contexte |
| spot-check | vérification par sondage |
| reasoning / thinking | raisonnement / réflexion |

## Agents

| Anglais | Français |
| --- | --- |
| agent | agent |
| assistant | assistant |
| agent loop | boucle d’agent |
| harness | harnais |
| tool / tool call | outil / appel d’outil |
| environment | environnement |
| model request | requête au modèle |
| stateless model | modèle sans état |
| degree of autonomy | degré d’autonomie |
| autonomy scale | échelle d’autonomie |
| coding agent | agent de code |
| subagent | sous-agent |
| skill | skill |
| hook | hook |
| plugin | plugin |
| sandbox | bac à sable |
| permission mode | mode de permission |
| allowlist / denylist | liste d’autorisation / liste d’interdiction |
| task brief | consigne de la tâche |
| done-criteria | critères d’achèvement |
| handoff | passation |
| compaction | compactage |
| session | session |

## Sécurité et qualité

| Anglais | Français |
| --- | --- |
| blast radius | rayon d’impact |
| least privilege | moindre privilège |
| human in the loop | humain dans la boucle |
| prompt injection | injection de prompt |
| exfiltration | exfiltration |
| guardrails | garde-fous |
| overreliance | dépendance excessive |
| automation complacency | complaisance envers l’automatisation |
| bias | biais |
| "Trust but verify" | « Faire confiance, mais vérifier » |
| evaluation (eval) | évaluation |
| golden set | jeu de référence |
| rubric | grille d’évaluation |
| LLM as judge | LLM juge |
| trace / trajectory | trace / trajectoire |
| observability | observabilité |
| spec / specification | spécification |
| commit / pull request / diff | commit / pull request / diff |
| CI | intégration continue (CI) |
| worktree | worktree |
