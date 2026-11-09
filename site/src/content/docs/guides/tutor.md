---
title: Étudier avec le tuteur
description: Installer le skill ai-tutor dans Claude Code ou opencode, ouvrir une leçon avec lui, et savoir ce qu’il fait et ne fait pas.
---

Le tuteur est Claude dans le rôle d’un partenaire d’étude pour une leçon de
ce site. Il tourne dans votre propre agent de code, lit la leçon que vous lui
indiquez, et donne des indices en gardant les réponses pour lui. Cette page
vous mène de zéro à une première session. Sa lecture ne compte pas dans la
progression des parcours.

## Installer

Il vous faut l’un des deux agents dans lesquels le tuteur fonctionne,
[Claude Code](https://code.claude.com/docs/en/overview) ou
[opencode](https://opencode.ai/docs/), et Node.js, parce que la commande
d’installation passe par `npx`.

Installez le skill dans votre dossier utilisateur, pour que l’agent le trouve
quel que soit le dossier où vous le lancez :

```sh
npx skills add benbouzi/ai-training --skill ai-tutor -g
```

La commande `skills` détecte les agents installés et installe le skill pour
chacun d’eux. Vérifiez ensuite qu’il figure dans la liste :

```sh
npx skills list -g
```

La sortie contient une ligne pour `ai-tutor`. Quand les instructions du site
demandent une version plus récente du skill, le tuteur vous dit de relancer
la même commande d’installation.

## Première session

Ouvrez la leçon
[Votre première session avec un agent de code](/coding-with-agents/first-session/)
dans votre navigateur et copiez son adresse. Lancez votre agent dans
n’importe quel dossier et donnez-lui la leçon.

Dans Claude Code, le skill a une commande slash :

```text
/ai-tutor https://benbouzi.github.io/ai-training/coding-with-agents/first-session/
```

opencode n’a pas de commande slash par skill. Écrivez donc une demande
simple qui nomme le skill :

```text
Utilise le skill ai-tutor sur https://benbouzi.github.io/ai-training/coding-with-agents/first-session/
```

Le tuteur commence par récupérer ses instructions et la leçon sur le site,
avec une commande `curl` pour chacune. Votre agent peut vous demander
d’approuver chaque commande. Acceptez les deux.

Une première réponse correcte nomme la leçon par son titre, dit qu’il a la
page à cette adresse, et propose les actions listées plus bas. Si vous avez
collé un export de votre progression et qu’une révision est due, il pose
d’abord une question de rappel.

## Ce que fait le tuteur

Chaque action porte sur la leçon que vous avez indiquée, et sur rien d’autre.
Le tuteur vous parle en français et comprend aussi le nom anglais de chaque
action.

- **expliquer** (*explain*) : explique un concept avec les mots de la leçon,
  puis donne un exemple.
- **points clés** (*key points*) : liste les points principaux de la leçon, à
  partir de sa partie « À retenir ».
- **explique-moi comme à un enfant de cinq ans** (*explain like I am five*) :
  réexplique un concept avec une comparaison de la vie courante, puis le
  rattache à la définition.
- **pourquoi c’est important** (*why it matters*) : relie ce que la leçon
  enseigne à votre propre travail.
- **interroge-moi** (*quiz me*) : pose une question à la fois, avec un indice
  quand vous vous trompez.
- **teste-moi** (*test me*) : vous demande de montrer un comportement attendu
  de la leçon et note votre essai.
- **critique ceci** (*critique this*) : écrit une réponse qui contient des
  défauts volontaires, que vous devez trouver, puis note votre critique.

Le tuteur ne donne que des indices. Sur une mauvaise réponse à une question
de contrôle, il pose une question. À la mauvaise réponse suivante, il vous
renvoie à la section qui enseigne l’idée, puis il donne un exemple plus
simple de la même idée. Après trois essais, il vous renvoie à la page. Lui
demander de « juste donner la réponse » mène à la même échelle d’indices.

## Ce que le tuteur ne fait pas

- Il ne peut pas lire votre progression dans le navigateur. Exportez votre
  progression depuis la page [Votre progression](/progress/) et collez le
  fichier dans la session si vous voulez la question de rappel.
- Il reste sur la leçon que vous avez indiquée. Pour une autre leçon,
  recommencez avec l’adresse de cette leçon.
- Il ne donne jamais la réponse à une question de contrôle ou à un exercice,
  ni avant ni après un indice.
- Il ne modifie jamais de fichier sur votre machine. Le seul fichier qu’il lit
  est l’export de progression que vous lui donnez.

## Réglages conseillés

Le tuteur lance une commande `curl` par récupération, et aucune autre
commande. Quand votre agent n’a pas d’outil shell, il utilise à la place
l’outil de récupération intégré de l’agent, et vous prévient que le texte de
la leçon peut être incomplet. Les réglages ci-dessous font de chaque
récupération une approbation que vous voyez, et bloquent tout le reste. Le
tuteur fonctionne aussi sans eux.

Pour Claude Code, démarrez dans le mode qui demande avant chaque commande,
sauf si vos réglages autorisent déjà cette commande :

```sh
claude --permission-mode manual
```

La valeur `manual` demande Claude Code 2.1.200 ou plus récent. Sur une
version plus ancienne, utilisez `--permission-mode default`, qui est le même
mode sous son nom de configuration. Pour refuser en plus toute modification
de fichier, ajoutez `--disallowedTools Edit Write`.

Pour opencode, utilisez l’agent de planification intégré (plan), qui demande
avant chaque modification et chaque commande :

```sh
opencode --agent plan
```

Vous pouvez aussi appuyer sur Tab dans une session opencode en cours jusqu’à
ce que la ligne d’état affiche l’agent plan.

## En cas d’échec

Quand une récupération échoue, le tuteur le dit en une phrase, nomme
l’adresse qui a échoué, et propose de continuer à partir de la page que vous
avez ouverte, sous forme de conversation simple et sans les actions. C’est le
comportement prévu : le tuteur n’a pas pu lire le site, et ses indices
viendraient de sa mémoire au lieu de la page. Vérifiez deux choses :

1. Votre réseau. Ouvrez l’adresse qui a échoué dans votre navigateur. Si elle
   ne se charge pas non plus, le site ou votre connexion est en panne.
2. L’adresse que vous avez collée. Seules les pages de leçon ont un paquet
   pour le tuteur. Les pages de parcours, les guides comme celui-ci et les
   pages de référence n’en ont pas, et le tuteur vous demande alors
   l’adresse d’une leçon.

Si les deux vont bien et que l’échec continue, ouvrez un ticket dans le
[suivi des tickets](https://github.com/benbouzi/ai-training/issues) avec
l’adresse qui a échoué et le message du tuteur.
