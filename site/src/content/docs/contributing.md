---
title: Contribuer
description: Construire le site et y contribuer.
---

Ce site est construit avec [Astro Starlight](https://starlight.astro.build/)
et publié sur GitHub Pages. Pour une remarque sur la traduction française,
ouvrez un ticket sur le
[dépôt de la traduction](https://github.com/benbouzi/ai-training/issues). Pour
le contenu d’origine, le fichier
[CONTRIBUTING.md](https://github.com/schubergphilis/ai-training/blob/main/CONTRIBUTING.md)
du dépôt d’origine explique comment contribuer.

## Le site

Les outils sont fixés dans `.mise.toml`. Lancez `mise install` une fois,
puis :

- `mise run site-install` : installe les dépendances du site (bun).
- `mise run site-dev` : démarre le serveur de développement, qui se recharge à
  chaque modification.
- `mise run site-build` : construit le site statique dans `site/dist`.
- `mise run site-check` : lance la vérification des types et du contenu
  d’Astro.
- `mise run lint` : lance les hooks prek sur tous les fichiers, plus
  `actionlint`.
- `mise run ci` : le contrôle complet (installation, lint, vérification,
  construction). L’intégration continue lance le même.

Le contenu se trouve dans `site/src/content/docs/`, et les fichiers statiques
dans `site/public/`.

## Conventions

Les messages de commit suivent les
[Conventional Commits](https://www.conventionalcommits.org/). Les hooks Git
(mise en forme, lint, vérification des liens, détection de secrets, contrôle
des messages de commit) sont gérés avec [prek](https://prek.j178.dev).
Installez-les une fois par clone avec
`prek install -t pre-commit -t commit-msg -t pre-push`.
