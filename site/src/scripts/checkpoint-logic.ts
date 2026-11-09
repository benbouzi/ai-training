import type { ReviewTrace } from './progress-model';
/**
 * The parts of checkpoint grading that need no DOM: answer comparison, the
 * shuffle rules, and the feedback texts. `checkpoints.ts` binds these to the
 * rendered markup.
 */

/**
 * Whether a checkpoint section's `data-phase` marks a `practice` checkpoint
 * (spec S03 "More practice"): recorded apart, never needed to finish.
 */
export function isPracticeSection(phase: string | undefined): boolean {
	return phase === 'practice';
}

/**
 * Whether a checkpoint section counts on its lesson page (spec S04 "Lesson
 * states"): toward finishing, the finish note and the routing cards. Only a
 * `first` checkpoint does. A section without `data-phase` is `first`.
 */
export function countsForLesson(phase: string | undefined): boolean {
	return phase === undefined || phase === 'first';
}

/** A feedback line and how it is styled. */
export interface Feedback {
	kind: 'ok' | 'nope' | 'note';
	text: string;
}

/** `predict` compares answers with whitespace collapsed and case folded. */
export function normalizeAnswer(s: string): string {
	return s.replace(/\s+/g, ' ').trim().toLowerCase();
}

export function answersMatch(given: string, expected: string): boolean {
	return normalizeAnswer(given) === normalizeAnswer(expected);
}

/** Fisher-Yates over a copy. `random` is injectable so a test can fix the order. */
export function shuffle<T>(arr: readonly T[], random: () => number = Math.random): T[] {
	const a = [...arr];
	for (let i = a.length - 1; i > 0; i--) {
		const j = Math.floor(random() * (i + 1));
		const ai = a[i] as T;
		a[i] = a[j] as T;
		a[j] = ai;
	}
	return a;
}

/** Whether `positions` reads 1, 2, 3, ... in order. */
export function isSequential(positions: readonly number[]): boolean {
	return positions.every((p, i) => p === i + 1);
}

/**
 * An `order` checkpoint never opens in the solved order: when the shuffle
 * lands on it, the first item moves to the end. Returns a copy.
 */
export function rotateIfSolved<T>(items: readonly T[], positionOf: (item: T) => number): T[] {
	const out = [...items];
	if (out.length > 1 && isSequential(out.map(positionOf))) {
		const first = out.shift() as T;
		out.push(first);
	}
	return out;
}

/**
 * Where a dragged row lands relative to the row under the pointer (`order`
 * drag-and-drop): before it when the pointer is in its top half, after it
 * otherwise. `rect` is the hovered row's bounding box.
 */
export function dropPlacement(pointerY: number, rect: { top: number; height: number }): 'before' | 'after' {
	return pointerY < rect.top + rect.height / 2 ? 'before' : 'after';
}

/** The `choice` and `scenario` verdict (spec S01 `choice`: a wrong pick shows its own `why`). */
export function choiceFeedback(ok: boolean, why: string | undefined, consequence: string | undefined): Feedback {
	if (ok) return { kind: 'ok', text: consequence ? `Juste. ${consequence}` : 'Juste.' };
	return { kind: 'nope', text: consequence ?? why ?? 'Pas tout à fait. Réessayez.' };
}

export function predictFeedback(ok: boolean): Feedback {
	return ok
		? { kind: 'ok', text: 'Juste. C’est exactement la sortie.' }
		: { kind: 'nope', text: 'Pas tout à fait. Suivez-le encore une fois.' };
}

/** The honor-system `predict` and `repair` self-grade; only `pass` counts (spec S01 `self-grade`). */
export function selfGradeFeedback(ok: boolean, kind: 'predict' | 'repair'): Feedback {
	if (ok) return { kind: 'ok', text: 'Enregistrée comme réussie.' };
	return kind === 'predict'
		? { kind: 'nope', text: 'Enregistrée. Ajustez votre prédiction et réessayez quand vous êtes prêt.' }
		: { kind: 'nope', text: 'Partielle. Seule une réussite compte : améliorez-la et notez de nouveau.' };
}

export function orderFeedback(ok: boolean): Feedback {
	return ok ? { kind: 'ok', text: 'Ordre juste.' } : { kind: 'nope', text: 'Pas encore le bon ordre.' };
}

/** `sort`: items still in the pool block grading; otherwise every chip must sit in its own bucket. */
export function sortFeedback(unplaced: number, allCorrect: boolean): Feedback {
	if (unplaced > 0) return { kind: 'note', text: `${unplaced} item${unplaced === 1 ? '' : 's'} still to place.` };
	return allCorrect
		? { kind: 'ok', text: 'Tout est bien classé.' }
		: { kind: 'nope', text: 'Certains éléments sont dans la mauvaise case.' };
}

/**
 * `multi-choice` (spec S01): exactly `wanted` correct boxes and nothing else.
 * `picked` is the number of boxes ticked, `wrong` how many of those are wrong,
 * and `firstWrongWhy` the `why` of the first wrong pick. A wrong pick shows
 * its why; a missed item is only counted, never named. `null` means nothing
 * to grade yet.
 */
export function multiChoiceVerdict(
	wanted: number,
	picked: number,
	wrong: number,
	firstWrongWhy: string | undefined,
): { ok: boolean | null; feedback: Feedback } {
	if (picked === 0) return { ok: null, feedback: { kind: 'note', text: `Choisissez d’abord ${wanted} réponses.` } };
	if (wrong > 0)
		return { ok: false, feedback: { kind: 'nope', text: firstWrongWhy ?? 'L’un de vos choix n’est pas juste.' } };
	const right = picked - wrong;
	if (right < wanted) {
		return {
			ok: false,
			feedback: {
				kind: 'nope',
				text: `${right} of ${wanted} so far, and nothing wrong. ${wanted - right} more to find.`,
			},
		};
	}
	return { ok: true, feedback: { kind: 'ok', text: 'Juste.' } };
}

const rows = (n: number) => `${n} row${n === 1 ? '' : 's'}`;

/** `match` (spec S01): every row filled, then every row right. The rationale shows only on a full pass. */
export function matchVerdict(
	empty: number,
	wrong: number,
	rationale: string,
): { ok: boolean | null; feedback: Feedback } {
	if (empty > 0) return { ok: null, feedback: { kind: 'note', text: `${rows(empty)} still to fill.` } };
	if (wrong > 0) return { ok: false, feedback: { kind: 'nope', text: `${rows(wrong)} wrong. Each row says which.` } };
	return { ok: true, feedback: { kind: 'ok', text: `Juste. ${rationale}`.trim() } };
}

const questions = (n: number) => `${n} question${n === 1 ? '' : 's'}`;

/** The skills check card's texts (spec S04 "Skills check"): the offer, and the note after each answer. */
export function skillsCheckOffer(open: number): string {
	return `Répondre à ${questions(open)}`;
}

export function skillsCheckNote(answered: number, passed: number, total: number): string {
	if (answered < total) return `${passed} réussie(s) sur ${answered} pour l’instant.`;
	const tail =
		passed === total ? 'Objectifs couverts. Passez à « À retenir ».' : 'Les manques sont enseignés plus bas.';
	return `${passed} réussie(s) sur ${total}. ${tail}`;
}

/** How many of the stage pills light up, and the label under them, for a review item. */
export function stageDisplay(stage: number | 'done' | undefined): { lit: number; label: string } {
	if (stage === 'done') return { lit: 5, label: 'acquise' };
	return { lit: stage ?? 0, label: `étape ${stage ?? '-'} sur 5` };
}

/** The settings page's one-line summary of a review item's answers, from its `history` (spec S05 "Storage"). */
export function historyDisplay(history: readonly ReviewTrace[]): string {
	const last = history[history.length - 1];
	if (!last) return 'not answered yet';
	return `${history.length} answered, last ${last.result} on ${last.at}`;
}
