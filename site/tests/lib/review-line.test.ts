import { isoDate, longDate, reviewLine } from '@lib/review-line';
import { describe, expect, it } from 'vitest';

describe('review line', () => {
	it('formats dates in American English, in UTC', () => {
		expect(isoDate(new Date('2027-03-20'))).toBe('2027-03-20');
		expect(longDate(new Date('2027-03-20'))).toBe('20 mars 2027');
	});
	it('says when the sources were checked only when sources-checked is set', () => {
		expect(reviewLine(new Date('2027-03-20'), new Date('2026-09-20'))).toBe(
			'Sources vérifiées le 20 septembre 2026. Révision prévue d’ici le 20 mars 2027.',
		);
		expect(reviewLine(new Date('2027-03-20'), undefined)).toBe('Révision prévue d’ici le 20 mars 2027.');
	});
	it('is null without a review-by date', () => {
		expect(reviewLine(undefined, new Date('2026-09-20'))).toBeNull();
	});
});
