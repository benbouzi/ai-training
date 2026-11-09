/**
 * French translation: the labels the site shows for values the data keeps in
 * English. The values stay as they are, because the checks, the progress
 * record and the URLs use them; only what a reader sees changes.
 */

/** Lesson `mode` (spec S03). */
export const MODE_LABEL: Readonly<Record<string, string>> = { tutorial: 'tutoriel', explanation: 'explication' };

/** Course plan entry status (`PlanStatus`). */
export const STATUS_LABEL: Readonly<Record<string, string>> = { live: 'en ligne', planned: 'prévue' };

/** The kind of a minutes cell in the course plan. */
export const MINUTES_KIND_LABEL: Readonly<Record<string, string>> = { estimate: 'estimation', target: 'cible' };

/** Exercise `kind`. */
export const EXERCISE_KIND_LABEL: Readonly<Record<string, string>> = { do: 'faire', judge: 'juger' };

/** Objective `level`. */
export const LEVEL_LABEL: Readonly<Record<string, string>> = { base: 'base', expert: 'expert' };

/** Checkpoint kind (spec S01), as the checkpoint header and the review page name it. */
export const CHECKPOINT_KIND_LABEL: Readonly<Record<string, string>> = {
	choice: 'choix',
	'multi-choice': 'choix multiple',
	match: 'association',
	scenario: 'scénario',
	predict: 'prédiction',
	order: 'ordre',
	sort: 'classement',
	repair: 'réparation',
};

/** Checkpoint `state` in the progress record. */
export const CHECKPOINT_STATE_LABEL: Readonly<Record<string, string>> = {
	passed: 'réussie',
	attempted: 'tentée',
	skipped: 'passée',
};

/** Habit result in the progress record. */
export const HABIT_RESULT_LABEL: Readonly<Record<string, string>> = { done: 'fait', skipped: 'passé' };

/** Bibliography entry `type`. */
export const SOURCE_TYPE_LABEL: Readonly<Record<string, string>> = {
	book: 'livre',
	course: 'cours',
	paper: 'article',
	reference: 'référence',
	video: 'vidéo',
};

/** The label of `value` in `labels`, or the value itself when the map has none. */
export function labelOf(labels: Readonly<Record<string, string>>, value: string): string {
	return labels[value] ?? value;
}

/** `n` and the noun, with the French plural from 2 on: `plural(1, 'leçon')` is `1 leçon`, `plural(3, 'leçon')` is `3 leçons`. */
export function plural(n: number, singular: string, pluralForm = `${singular}s`): string {
	return `${n} ${n > 1 ? pluralForm : singular}`;
}
