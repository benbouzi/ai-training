---
title: Animer un atelier
description: Préparer et animer un atelier d’une journée en présentiel sur un domaine de ce site, avec trois tables pour trois niveaux.
---

## À qui s’adresse ce guide

Ce guide s’adresse à un formateur qui anime le parcours d’un domaine sous
forme d’atelier en présentiel. La salle accueille de 6 à 20 personnes avec
leur propre ordinateur portable, et un formateur travaille avec quelques
assistants. Le site est la référence pour tout ce qui est enseigné. L’exemple
développé est le parcours [Coder avec des agents](/coding-with-agents/). Le
plan convient aussi aux autres domaines, avec les changements pour les
domaines des Fondamentaux que donne la section suivante.

## Trois tables

La salle compte trois tables, une par niveau. Chaque personne s’assoit à la
table qui correspond le mieux à sa manière d’apprendre ce jour-là, et le
questionnaire de placement suggère laquelle.

- **(A) Instruction guidée.** Un niveau propre à l’atelier, sans réglage sur
  le site, pour les personnes qui ne peuvent raisonnablement pas apprendre
  ce contenu seules à partir du site. Le formateur leur consacre le plus de
  temps : d’abord une démonstration, puis la même tâche faite ensemble, puis
  seul. Les personnes qui finissent tôt refont l’exercice sans l’exemple
  développé.
- **(B) Moins à l’aise.** Le niveau d’aisance `less` du site. Ces personnes
  peuvent travailler à partir du site avec des indices : elles essaient
  d’abord l’exercice et en discutent ensuite. Celles qui finissent tôt
  prennent l’objectif « Pour aller plus loin ».
- **(C) Plus à l’aise.** Le niveau d’aisance `more` du site. Ces personnes
  avancent seules et comparent le temps passé à leur prévision. Celles qui
  finissent tôt aident la table B.

Chaque apprenant choisit son niveau d’aisance sur la page
[Réglages](/settings/) : demandez aux tables B et C de le régler en début de
journée. La table C aide la table B, et jamais la table A, parce que la
table A a besoin d’un rythme plus lent et d’une méthode fixe. Chacun peut
changer de table après le premier bloc. Les domaines des Fondamentaux
(Concepts, Sécurité, Utiliser des agents) n’ont pas de niveau d’aisance sur
le site. Dans ces ateliers, B et C sont aussi des niveaux propres à
l’atelier, et un exercice terminé prend la forme d’une réponse écrite.

## Avant la journée

- Envoyez le questionnaire de placement et les instructions d’installation
  une semaine avant.
- Proposez un appel d’installation libre de 30 minutes. À la fin de l’appel,
  chaque personne a installé l’agent et s’y est connectée, a cloné vos dépôts
  d’exercice et y a lancé une commande.
- Prévoyez un assistant pour huit participants, et placez la plupart d’entre
  eux à la table A.
- Faites vous-même chaque exercice dans la version actuelle du site.
- Apportez des notes autocollantes de deux couleurs pour chaque personne.
- Fixez la date de la séance de suivi.

Pour Coder avec des agents, chaque leçon a son propre dépôt d’exercice (sa
fixture). Faites votre propre copie de chaque fixture utilisée en suivant les
étapes de la section [The fixture](/coding-with-agents/first-session/#the-fixture)
de la première leçon. Dans chaque copie, faites un commit et posez une
étiquette (tag) sur l’état de départ et sur l’état final de chaque exercice.
Poussez ensuite les copies avec leurs étiquettes à un endroit où les binômes
les clonent pendant l’appel d’installation.

## Le questionnaire de placement

Le questionnaire prend dix minutes. Présentez-le comme le premier exercice de
l’atelier. Vous ne notez aucune réponse, et personne ne voit de score. Tirez
chaque question des leçons du domaine. Les exemples ci-dessous viennent de
Coder avec des agents.

- **Auto-placement, deux questions.** Chaque question donne une phrase par
  niveau, et la personne choisit celle qui la décrit le mieux. Exemple : « Je
  veux voir quelqu’un le faire avant d’essayer » (A), « Je sais suivre des
  étapes écrites et demander quand je bloque » (B), « Je préfère commencer
  seul et comparer ensuite » (C).
- **Que faites-vous ensuite, deux questions.** Chaque question montre une
  tâche et une partie de la sortie d’un agent, avec quatre options. Chaque
  option correspond à un niveau. Exemple : l’agent dit avoir corrigé l’erreur
  de décalage d’une unité dans `done()` et montre un diff sans résultat de
  tests. Les options sont « faire le commit » (A), « lui demander d’expliquer
  le diff » (A), « lire le diff » (B) et « lancer les tests soi-même » (C).
- **Remettre dans l’ordre, une question.** Les étapes d’une modification,
  mélangées, à remettre dans l’ordre. Exemple : « laisser l’agent faire la
  modification », « lancer les tests pour vérifier la modification »,
  « demander un plan à l’agent et le lire ». L’ordre est le plan, puis la
  modification, puis les tests.
- **Qu’est-ce qui s’affiche, une question.** Un court morceau de vrai code,
  comme dans les questions de prédiction du site. Exemple : dans la fixture
  de la première leçon, partez d’une liste vide dans `/tmp/quiz.json`, pour
  que rien n’écrive dans le `todos.json` de la fixture. Après
  `TODO_FILE=/tmp/quiz.json python3 todo.py add "Buy milk"` et
  `TODO_FILE=/tmp/quiz.json python3 todo.py add "Call Sam"`, qu’affiche
  `TODO_FILE=/tmp/quiz.json python3 todo.py done 1` ? Il affiche
  `done #1: Call Sam`. Cette question dévoile le bogue de décalage d’une unité
  qu’enseigne la première leçon.
- **Usage, une question.** « La dernière fois que vous avez utilisé un
  assistant, à quel moment lui avez-vous demandé du code pour la première
  fois ? » Proposez trois réponses : « au début » (A), « après avoir décrit
  la tâche » (B) et « après avoir écrit un plan ou un contrôle » (C).

Une mauvaise réponse à la question d’ordre ou d’affichage compte comme A, et
une bonne réponse compte comme C. Pour le score, comptez les réponses A, B
et C de chaque personne. La personne commence à la table qui a le plus de
réponses. En cas d’égalité, prenez la table qui apporte le plus de soutien :
A avant B, et B avant C. Ce questionnaire n’a pas été validé, donc notez les
réponses de chaque personne à côté de la table où elle a fini la journée.

## La journée

Ces horaires sont indicatifs et n’ont pas été validés. Corrigez-les après
votre premier atelier et notez ce qui a changé.

| Quand | Quoi                                                                                                                                                          |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0:00  | Ouverture commune, 30 min : une courte énigme sans code, pourquoi trois tables, le résultat du placement, le droit de changer, une note de confiance de 1 à 5 |
| 0:30  | Bloc 1, 60 min                                                                                                                                                |
| 1:30  | Pause, 15 min, fiches minute, changements de table                                                                                                            |
| 1:45  | Bloc 2, 60 min                                                                                                                                                |
| 2:45  | Plénière, 15 min : une question à toute la salle, réponse seul, discussion en binôme, nouvelle réponse                                                        |
| 3:00  | Déjeuner, 45 min, fiches minute, changements de table                                                                                                         |
| 3:45  | Bloc 3, 60 min                                                                                                                                                |
| 4:45  | Pause, 15 min, fiches minute                                                                                                                                  |
| 5:00  | Bloc 4, 60 min                                                                                                                                                |
| 6:00  | Clôture commune, 30 min                                                                                                                                       |

Un atelier de deux jours reprend les blocs 1 à 4 le deuxième jour. Le premier
jour se termine alors par les fiches minute et un changement de table. Le
formateur choisit les leçons de chaque bloc pour chaque domaine. Pour Coder
avec des agents, les blocs 1 et 2 peuvent ressembler à ceci :

| Bloc | Table A                                                                                                    | Table B                                                                                               | Table C                                                                                                         |
| ---- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1    | [Votre première session avec un agent de code](/coding-with-agents/first-session/), avec une démonstration | Comme la table A                                                                                      | Comme la table A, puis [Garder les clés d’API hors de portée de l’agent](/coding-with-agents/keys-and-secrets/) |
| 2    | [Garder les clés d’API hors de portée de l’agent](/coding-with-agents/keys-and-secrets/)                   | Comme la table A, puis [Décider s’il faut le construire](/coding-with-agents/deciding-what-to-build/) | [Découper le travail en composants que l’agent construit un par un](/coding-with-agents/decomposing-the-work/)  |

**Ouverture commune.** Tout le monde est réuni pour l’énigme et les raisons
des trois tables. Ensuite, chaque personne écrit une première note de
confiance de 1 à 5 et rejoint la table que le questionnaire a suggérée.

**Un bloc de 60 minutes.** Chaque bloc a quatre parties. Relier (5 min)
rattache le bloc à ce que les personnes ont déjà fait. Concepts (0 à 10 min)
dure le plus longtemps à la table A et peut tomber à zéro à la table C.
Pratique (35 à 45 min) est l’exercice, en binôme. Conclusions (10 min) est un
court débriefing à chaque table.

**Pause.** Ramassez les fiches minute, lisez-les pendant la pause, et
servez-vous-en pour proposer des changements de table avant le bloc suivant.

**Question de plénière.** Posez à toute la salle une question avec quelques
réponses possibles. Chacun répond seul, discute en binôme, puis répond de
nouveau. L’écart entre les deux réponses vous dit ce qu’il faut expliquer.

**Clôture.** Les binômes présentent leur travail, et chacun choisit une
habitude et écrit une seconde note de confiance. La section « Clôture et
suivi » ci-dessous donne le détail.

## Règles des exercices

- Donnez à chaque exercice un état de départ, un état final et le diff entre
  les deux, sous forme d’étiquettes comme `ex1-start` et `ex1-done`. Les
  binômes lancent `git checkout -f ex1-start` pour revenir au départ et
  `git checkout -f ex1-done` pour voir l’état final. Les deux commandes
  effacent leurs modifications mais gardent les nouveaux fichiers, que
  `git clean -fd` supprime.
- Laissez une seule chose à trouver au binôme, et préparez tout le reste à
  l’avance.
- Donnez toujours à l’agent un contrôle qu’il peut lancer, comme un test, ou
  une commande dont la sortie est connue.
- La table A part d’un exemple développé du même exercice, avec la consigne
  et le contrôle fournis, et seulement le prompt à écrire. Les tables B et C
  partent de l’exercice tel que la leçon le formule, et l’objectif « Pour
  aller plus loin » est pour qui termine.
- Demandez à chaque binôme trois options avant d’en retenir une.
- Écrivez « relisez chaque ligne du diff » dans les instructions de la
  table A.

## Règles de la salle

- Les personnes travaillent en binôme à leur propre table. Elles échangent
  les rôles trois ou quatre fois par heure, et la personne la moins
  expérimentée tape au clavier.
- Vérifiez la compréhension toutes les 10 à 15 minutes avec un moyen simple :
  une note autocollante sur l’ordinateur, un nombre de 1 à 5, ou une question
  de rappel en une ligne.
- Distribuez des fiches minute à chaque pause. Chaque fiche porte une chose
  apprise et une question restée ouverte, et vous vous en servez pour
  changer les personnes de table.
- N’animez jamais seul. Une deuxième personne fait avancer la salle pendant
  que vous aidez un binôme.
- Laissez les participants avancés aider à la table B, et tenez-les loin du
  micro.
- Commencez et terminez les pauses à l’heure, et limitez un atelier à deux
  jours.

## Par table

**Table A.** Faites la démonstration de l’exercice avec une erreur
volontaire, lancez-le, et laissez la salle le voir échouer. Faites ensuite
l’exercice ensemble, puis laissez les binômes le faire seuls. Donnez à chaque
binôme le [tuteur](/guides/tutor/) dans une seconde session, à côté de
l’agent de code, pour les questions sur la leçon. Il donne des indices et
garde les réponses pour lui. Après une mauvaise réponse, il pose une
question, et après la suivante, il renvoie à la section qui enseigne l’idée.

**Table B.** Les personnes essaient d’abord l’exercice et débriefent
ensuite. Apprenez-leur à écrire le contrôle avant le prompt. Avant qu’elles
laissent l’agent lancer une commande, demandez quel serait le pire résultat
possible de cette commande.

**Table C.** Les personnes prévoient le temps que prend un exercice et le
comparent au temps réel. Donnez-leur du travail sur le harnais, comme les
instructions de projet, les hooks et les worktrees en parallèle. Demandez-leur
de décider ce qu’elles ne confieraient pas à l’agent, et pourquoi.

## Clôture et suivi

- Chaque binôme explique en deux minutes une modification qu’il a faite et
  la manière dont il l’a vérifiée.
- Chaque personne choisit une habitude dans une leçon qu’elle a terminée. Le
  site propose des habitudes après une leçon terminée et les fait revenir
  selon un calendrier fixe.
- Organisez un suivi d’une heure deux à quatre semaines plus tard.
- Demandez une note de confiance de 1 à 5 au début et à la fin de la
  journée, sur la même échelle.

## Ce qu’il faut noter

- Les réponses de chaque personne au questionnaire, à côté de la table où
  elle a fini la journée.
- Un formulaire de retour par exercice, avec une ligne par exercice (trop
  facile, adapté ou trop difficile) et un commentaire.
- Les fiches minute.
- Les prévisions de temps de la table C, à côté des temps réels.
- Les deux notes de confiance de chaque personne.

Ces relevés servent à corriger les horaires ci-dessus et le calcul du
questionnaire : gardez-les pour chaque atelier.

## Pour aller plus loin

Les ressources ci-dessous sont en anglais.

- [Teaching Tech Together](https://teachtogether.tech/en/) : le livre de
  Greg Wilson sur l’approche que suit ce guide, en particulier les chapitres
  [In the Classroom](https://teachtogether.tech/en/index.html#s:classroom) et
  [Teaching Online](https://teachtogether.tech/en/index.html#s:online), et la
  section
  [Plan for Mixed Abilities](https://teachtogether.tech/en/index.html#s:classroom-mixed).
- [The Carpentries instructor training](https://carpentries.github.io/instructor-training/) :
  le support de formation à l’origine des notes autocollantes, des fiches
  minute et du travail avec des assistants.
- [CS50 Educator Workshop](https://cs50.harvard.edu/workshop/) : des liens
  vers les enregistrements annuels de l’atelier sur YouTube, sur
  l’enseignement aux étudiants moins à l’aise et sur l’enseignement avec
  l’IA.
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) :
  la liste d’Anthropic de cinq erreurs fréquentes, qui sert de liste de
  contrôle dans les débriefings.
- [How I Teach](https://kentcdodds.com/blog/how-i-teach) : Kent C. Dodds sur
  l’exercice fait avant l’explication, et sur un formulaire de retour après
  chaque exercice.
