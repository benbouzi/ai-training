import {
	answersMatch,
	choiceFeedback,
	countsForLesson,
	dropPlacement,
	historyDisplay,
	isPracticeSection,
	isSequential,
	matchVerdict,
	multiChoiceVerdict,
	normalizeAnswer,
	orderFeedback,
	predictFeedback,
	rotateIfSolved,
	selfGradeFeedback,
	shuffle,
	skillsCheckNote,
	skillsCheckOffer,
	sortFeedback,
	stageDisplay,
} from '@scripts/checkpoint-logic';
import { describe, expect, it } from 'vitest';

describe('answers', () => {
	it('collapses whitespace and case', () => {
		expect(normalizeAnswer('  27°C,\n  Sun ')).toBe('27°c, sun');
		expect(answersMatch(' 27°c, sun', '27°C, sun')).toBe(true);
		expect(answersMatch('27°C, rain', '27°C, sun')).toBe(false);
	});
});

describe('shuffle', () => {
	it('returns a permutation and leaves the input alone', () => {
		const input = [1, 2, 3, 4, 5];
		const out = shuffle(input);
		expect(out).toHaveLength(5);
		expect([...out].sort()).toEqual(input);
		expect(input).toEqual([1, 2, 3, 4, 5]);
	});
	it('follows the injected random source', () => {
		// random() = 0 always picks index 0, which walks the first element to the back.
		expect(shuffle([1, 2, 3], () => 0)).toEqual([2, 3, 1]);
		// random() just under 1 keeps every element in place.
		expect(shuffle([1, 2, 3], () => 0.999)).toEqual([1, 2, 3]);
	});
	it('isSequential recognizes 1..n', () => {
		expect(isSequential([1, 2, 3])).toBe(true);
		expect(isSequential([2, 1, 3])).toBe(false);
		expect(isSequential([])).toBe(true);
	});
	it('rotateIfSolved moves the first item to the end only when solved', () => {
		const pos = (n: number) => n;
		expect(rotateIfSolved([1, 2, 3], pos)).toEqual([2, 3, 1]);
		expect(rotateIfSolved([2, 1, 3], pos)).toEqual([2, 1, 3]);
		expect(rotateIfSolved([1], pos)).toEqual([1]);
	});
});

describe('dropPlacement', () => {
	it('lands before the hovered row in its top half and after it otherwise', () => {
		const rect = { top: 100, height: 40 };
		expect(dropPlacement(100, rect)).toBe('before');
		expect(dropPlacement(119, rect)).toBe('before');
		expect(dropPlacement(120, rect)).toBe('after');
		expect(dropPlacement(139, rect)).toBe('after');
	});
});

describe('feedback', () => {
	it('choice: correct with or without a consequence', () => {
		expect(choiceFeedback(true, 'why', undefined)).toEqual({ kind: 'ok', text: 'Juste.' });
		expect(choiceFeedback(true, undefined, 'It runs.')).toEqual({ kind: 'ok', text: 'Juste. It runs.' });
	});
	it('choice: a wrong pick shows consequence, then why, then a default', () => {
		expect(choiceFeedback(false, 'why', 'bad')).toEqual({ kind: 'nope', text: 'bad' });
		expect(choiceFeedback(false, 'why', undefined)).toEqual({ kind: 'nope', text: 'why' });
		expect(choiceFeedback(false, undefined, undefined).text).toBe('Pas tout à fait. Réessayez.');
	});
	it('predict, order and self-grade texts', () => {
		expect(predictFeedback(true).kind).toBe('ok');
		expect(predictFeedback(false).text).toBe('Pas tout à fait. Suivez-le encore une fois.');
		expect(orderFeedback(true).text).toBe('Ordre juste.');
		expect(orderFeedback(false).kind).toBe('nope');
		expect(selfGradeFeedback(true, 'predict').text).toBe('Enregistrée comme réussie.');
		expect(selfGradeFeedback(false, 'predict').text).toContain('Ajustez votre prédiction');
		expect(selfGradeFeedback(false, 'repair').text).toContain('Partielle');
	});
	it('sort: unplaced items block grading', () => {
		expect(sortFeedback(1, true)).toEqual({ kind: 'note', text: 'Encore 1 élément à classer.' });
		expect(sortFeedback(2, false).text).toBe('Encore 2 éléments à classer.');
		expect(sortFeedback(0, true).kind).toBe('ok');
		expect(sortFeedback(0, false).text).toBe('Certains éléments sont dans la mauvaise case.');
	});
});

describe('phases', () => {
	it('only a first checkpoint counts on its lesson page, and a missing phase is first', () => {
		expect(countsForLesson('first')).toBe(true);
		expect(countsForLesson(undefined)).toBe(true);
		expect(countsForLesson('practice')).toBe(false);
		expect(countsForLesson('review')).toBe(false);
	});
	it('marks a practice section', () => {
		expect(isPracticeSection('practice')).toBe(true);
		expect(isPracticeSection('first')).toBe(false);
		expect(isPracticeSection(undefined)).toBe(false);
	});
});

describe('skills check texts', () => {
	it('pluralizes the offer', () => {
		expect(skillsCheckOffer(1)).toBe('Répondre à 1 question');
		expect(skillsCheckOffer(2)).toBe('Répondre à 2 questions');
	});
	it('counts passes while open, then sums up', () => {
		expect(skillsCheckNote(1, 1, 2)).toBe('1 sur 1 réussie pour l’instant.');
		expect(skillsCheckNote(2, 2, 2)).toBe('2 sur 2 réussies. Objectifs couverts. Passez à « À retenir ».');
		expect(skillsCheckNote(2, 1, 2)).toBe('1 sur 2 réussie. Les manques sont enseignés plus bas.');
	});
});

describe('stageDisplay', () => {
	it('lights one pill per stage, all five when retired, none when unknown', () => {
		expect(stageDisplay(3)).toEqual({ lit: 3, label: 'étape 3 sur 5' });
		expect(stageDisplay('done')).toEqual({ lit: 5, label: 'acquise' });
		expect(stageDisplay(undefined)).toEqual({ lit: 0, label: 'étape - sur 5' });
	});
});

describe('multiChoiceVerdict', () => {
	it('asks for picks, names the first wrong why, counts what is still missing, then passes', () => {
		expect(multiChoiceVerdict(3, 0, 0, undefined)).toEqual({
			ok: null,
			feedback: { kind: 'note', text: 'Choisissez d’abord 3 réponses.' },
		});
		expect(multiChoiceVerdict(3, 2, 1, 'Clear to whom?')).toEqual({
			ok: false,
			feedback: { kind: 'nope', text: 'Clear to whom?' },
		});
		expect(multiChoiceVerdict(3, 1, 1, undefined).feedback.text).toBe('L’un de vos choix n’est pas juste.');
		expect(multiChoiceVerdict(3, 1, 0, undefined)).toEqual({
			ok: false,
			feedback: { kind: 'nope', text: '1 sur 3 pour l’instant, sans erreur. Encore 2 à trouver.' },
		});
		expect(multiChoiceVerdict(3, 3, 0, undefined)).toEqual({ ok: true, feedback: { kind: 'ok', text: 'Juste.' } });
	});
});

describe('matchVerdict', () => {
	it('blocks on empty rows, counts wrong rows, and shows the rationale on a full pass', () => {
		expect(matchVerdict(1, 0, 'r')).toEqual({ ok: null, feedback: { kind: 'note', text: 'Encore 1 ligne à remplir.' } });
		expect(matchVerdict(3, 0, 'r').feedback.text).toBe('Encore 3 lignes à remplir.');
		expect(matchVerdict(0, 1, 'r')).toEqual({
			ok: false,
			feedback: { kind: 'nope', text: '1 ligne fausse. Chaque ligne indique laquelle.' },
		});
		expect(matchVerdict(0, 2, 'r').feedback.text).toBe('2 lignes fausses. Chaque ligne indique laquelle.');
		expect(matchVerdict(0, 0, 'Because.')).toEqual({ ok: true, feedback: { kind: 'ok', text: 'Juste. Because.' } });
		expect(matchVerdict(0, 0, '').feedback.text).toBe('Juste.');
	});
});

describe('historyDisplay', () => {
	it('says when an item was never answered', () => {
		expect(historyDisplay([])).toBe('pas encore répondu');
	});
	it('counts the answers and names the last one with its day', () => {
		expect(
			historyDisplay([
				{ at: '2026-03-08', result: 'fail' },
				{ at: '2026-03-10', result: 'pass' },
			]),
		).toBe('2 réponses, la dernière réussie le 2026-03-10');
	});
});
