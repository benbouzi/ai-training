import { continueLink, overallText } from '@scripts/overall-progress-model';
import type { Overall } from '@scripts/overview';
import { describe, expect, it } from 'vitest';

const a = { id: 'concepts/a', title: 'Lesson A', checkpoints: [] };
const b = { id: 'concepts/b', title: 'Lesson B', checkpoints: [] };
const base: Overall = {
	lessons: 2,
	finished: 0,
	skipped: 0,
	started: 0,
	checkpoints: 5,
	passed: 0,
	percent: 0,
	next: a,
	firstSkipped: null,
	any: false,
};

describe('overallText', () => {
	it('gives the totals before any progress', () => {
		expect(overallText(base)).toBe('2 leçons et 5 questions de contrôle dans six parcours. Rien n’est commencé.');
	});
	it('counts finished and passed, and adds the in-progress count only when there is one', () => {
		expect(overallText({ ...base, any: true, finished: 1, passed: 2 })).toBe(
			'Leçons terminées : 1 sur 2. Questions de contrôle réussies : 2 sur 5.',
		);
		expect(overallText({ ...base, any: true, started: 1 })).toBe(
			'Leçons terminées : 0 sur 2, 1 en cours. Questions de contrôle réussies : 0 sur 5.',
		);
	});
});

describe('continueLink', () => {
	it('keeps the rendered link without progress', () => {
		expect(continueLink(base, '/ai-training')).toBeNull();
	});
	it('points at the next unfinished lesson', () => {
		expect(continueLink({ ...base, any: true, next: b }, '/ai-training')).toEqual({
			href: '/ai-training/concepts/b/',
			text: 'Continuer avec : Lesson B',
		});
	});
	it('with everything skipped, continues with the first skipped lesson', () => {
		expect(continueLink({ ...base, any: true, next: null, firstSkipped: a, skipped: 2 }, '')).toEqual({
			href: '/concepts/a/',
			text: 'Continuer avec : Lesson A',
		});
	});
	it('with the rest finished, names the skipped count', () => {
		expect(continueLink({ ...base, any: true, next: null, firstSkipped: a, finished: 1, skipped: 1 }, '')).toEqual({
			href: '/concepts/a/',
			text: 'Toutes les leçons sont terminées, 1 passée',
		});
	});
	it('with every lesson finished, points at the topic map', () => {
		expect(continueLink({ ...base, any: true, next: null, finished: 2 }, '')).toEqual({
			href: '/map/',
			text: 'Toutes les leçons sont terminées : voir la carte des thèmes',
		});
	});
});
