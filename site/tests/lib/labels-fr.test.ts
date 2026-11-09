import { labelOf, MODE_LABEL, plural, SOURCE_TYPE_LABEL } from '@lib/labels-fr';
import { describe, expect, it } from 'vitest';

describe('labelOf', () => {
	it('gives the French label of a known value', () => {
		expect(labelOf(MODE_LABEL, 'tutorial')).toBe('tutoriel');
		expect(labelOf(SOURCE_TYPE_LABEL, 'paper')).toBe('article');
	});
	it('keeps a value the map does not hold', () => {
		expect(labelOf(MODE_LABEL, 'how-to')).toBe('how-to');
	});
});

describe('plural', () => {
	it('keeps the singular for 0 and 1, and adds an s from 2 on', () => {
		expect(plural(0, 'leçon')).toBe('0 leçon');
		expect(plural(1, 'leçon')).toBe('1 leçon');
		expect(plural(3, 'leçon')).toBe('3 leçons');
	});
	it('takes an irregular plural', () => {
		expect(plural(2, 'question de contrôle', 'questions de contrôle')).toBe('2 questions de contrôle');
	});
});
