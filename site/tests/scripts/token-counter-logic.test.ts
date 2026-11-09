/**
 * The token counter's rules against what `count_tokens.py` and
 * `pages_per_window.py` print. Every expected report here is the Python
 * scripts' own output for the same input, run on python3 when the port was
 * written, so a change that makes the two disagree fails here. The lesson
 * sample is read from `site/examples/` itself.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { countReport, countWords, estimateTokens, grouped, pagesReport } from '@scripts/token-counter-logic';
import { describe, expect, it } from 'vitest';

const SAMPLE = join(import.meta.dirname, '../../examples/concepts/context-window/sample/notes.txt');

describe('countReport', () => {
	it('prints the three lines count_tokens.py prints for the lesson sample', () => {
		expect(countReport(readFileSync(SAMPLE, 'utf8'))).toEqual([
			'caractères : 505',
			'mots : 86',
			'jetons (estimation) : 141',
		]);
	});
	it('counts an empty text as zero of each', () => {
		expect(countReport('')).toEqual(['caractères : 0', 'mots : 0', 'jetons (estimation) : 0']);
	});
	it('counts each punctuation mark as a token of its own', () => {
		expect(countReport('Hello, world!')).toEqual(['caractères : 13', 'mots : 2', 'jetons (estimation) : 4']);
	});
	it('counts characters as code points, and long words, underscores and non-ASCII letters as Python does', () => {
		expect(countReport('internationalization _underscored_name ünïcödéwörd 12345678 😀 x')).toEqual([
			'caractères : 63',
			'mots : 6',
			'jetons (estimation) : 13',
		]);
	});
	it('splits words on any run of whitespace, as str.split() does', () => {
		expect(countReport('  two\twords\n')).toEqual(['caractères : 12', 'mots : 2', 'jetons (estimation) : 2']);
	});
});

describe('estimateTokens', () => {
	it('counts a word of up to six characters as one token and a longer one per four characters', () => {
		expect(estimateTokens('window')).toBe(1);
		expect(estimateTokens('windows')).toBe(2);
		expect(estimateTokens('delivery')).toBe(2);
		expect(estimateTokens('deliveries')).toBe(3);
	});
	it('counts a piece that starts with an underscore as one token, whatever its length', () => {
		expect(estimateTokens('_a_very_long_name')).toBe(1);
	});
});

describe('countWords', () => {
	it('is zero for whitespace only', () => {
		expect(countWords(' \n\t ')).toBe(0);
	});
});

describe('grouped', () => {
	it('writes the thousands the way Python f"{n:,}" does', () => {
		expect(grouped(0)).toBe('0');
		expect(grouped(999)).toBe('999');
		expect(grouped(1739)).toBe('1 739');
		expect(grouped(1_000_000)).toBe('1 000 000');
	});
});

describe('pagesReport', () => {
	it('prints the lines pages_per_window.py prints for the sample count', () => {
		expect(pagesReport(141)).toEqual([
			'une page : 141 jetons',
			'fenêtre de 8 000 jetons : 56 pages',
			'fenêtre de 32 000 jetons : 226 pages',
			'fenêtre de 200 000 jetons : 1 418 pages',
			'fenêtre de 1 000 000 jetons : 7 092 pages',
		]);
	});
	it('prints the numbers of the exercise example, a page of 750 tokens', () => {
		expect(pagesReport(750)).toEqual([
			'une page : 750 jetons',
			'fenêtre de 8 000 jetons : 10 pages',
			'fenêtre de 32 000 jetons : 42 pages',
			'fenêtre de 200 000 jetons : 266 pages',
			'fenêtre de 1 000 000 jetons : 1 333 pages',
		]);
	});
	it('writes the page count without grouping and a window too small as zero pages', () => {
		expect(pagesReport(1_000_001)).toEqual([
			'une page : 1000001 jetons',
			'fenêtre de 8 000 jetons : 0 page',
			'fenêtre de 32 000 jetons : 0 page',
			'fenêtre de 200 000 jetons : 0 page',
			'fenêtre de 1 000 000 jetons : 0 page',
		]);
	});
	it('prints the page line alone for an empty page, where the Python script divides by zero', () => {
		expect(pagesReport(0)).toEqual(['une page : 0 jetons']);
	});
});
