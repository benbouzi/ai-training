---
title: Rédiger des pages
description: Ajouter des pages Markdown, les placer dans la barre latérale et les relier entre elles.
---

Les pages sont des fichiers Markdown (`.md`) ou MDX (`.mdx`) placés sous
`site/src/content/docs/`. Le chemin sous ce dossier devient l’adresse de la
page, et chaque page a au minimum un `title` dans son en-tête (frontmatter).

## Ajouter une page

Créez `site/src/content/docs/guides/ma-page.md` :

```markdown
---
title: Ma page
description: Un court résumé, utilisé pour le référencement et les cartes de partage.
---

Votre contenu ici.
```

Cette page est servie à l’adresse `/guides/ma-page/` (sous le chemin de base
du déploiement).

## La placer dans la barre latérale

La barre latérale est définie explicitement dans `site/astro.config.mjs`.
Ajoutez votre page aux `items` d’un groupe :

```js
{
	label: 'Contribuer',
	items: [
		{ slug: 'guides/writing-pages', label: 'Rédiger des pages' },
		{ slug: 'guides/ma-page', label: 'Ma page' },
	],
},
```

## Liens et images

Écrivez les liens internes et les sources d’images **relatifs à la racine**
(`/guides/ma-page/`, `/schema.png`), sans le chemin de base du déploiement. Un
petit plugin rehype dans `astro.config.mjs` ajoute le chemin de base
(`/ai-training`) au moment du rendu. Le même Markdown fonctionne ainsi en
développement local et sur GitHub Pages.

```markdown
Voir la [page Contribuer](/contributing/).

![Un schéma](/schema.png)
```

Les liens d’action de l’en-tête de la page d’accueil et les balises HTML `<a>`
brutes font exception : ils sont utilisés tels quels et doivent inclure le
chemin de base.

## La page d’accueil

`index.mdx` utilise le gabarit `splash` de Starlight, qui affiche un en-tête et
une grille de cartes à la place de la mise en page habituelle de la
documentation. C’est une page d’accueil séparée, et la barre latérale commence
directement par le contenu.
