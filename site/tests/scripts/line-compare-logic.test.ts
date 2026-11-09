/**
 * The rules of the line comparer (`scripts/line-compare-logic.ts`). The
 * expected reports for the lesson's two samples are what
 * `site/examples/safety/saying-ai-helped/compare.py` and
 * `compare_rewrite.py` print, run on python3 when the port was written.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { codeLines, compare } from '@scripts/line-compare-logic';
import { describe, expect, it } from 'vitest';

const DIR = join(import.meta.dirname, '../../examples/safety/saying-ai-helped');
const read = (path: string) => readFileSync(join(DIR, path), 'utf8');

describe('codeLines', () => {
	it('strips each line and skips blank ones', () => {
		expect(codeLines('  a = 1\n\n\tb = 2  \n   \n')).toEqual(['a = 1', 'b = 2']);
	});
	it('splits at CRLF, CR and LF', () => {
		expect(codeLines('a\r\nb\rc\nd')).toEqual(['a', 'b', 'c', 'd']);
	});
	it('returns nothing for an empty text', () => {
		expect(codeLines('')).toEqual([]);
	});
});

describe('compare', () => {
	it('prints what compare.py prints for the generated function', () => {
		const result = compare(read('sample/generated.py'), read('sources/truncate.py'), 'truncate.py');
		expect(result.lines).toEqual([
			'9 lignes sur 10 figurent aussi dans truncate.py',
			'lignes absentes de truncate.py :',
			'  def shorten(text, limit, marker="..."):',
		]);
		expect(result.shared).toBe(9);
		expect(result.total).toBe(10);
	});
	it('prints what compare_rewrite.py prints for the rewrite', () => {
		const result = compare(read('sample/rewritten.py'), read('sources/truncate.py'), 'truncate.py');
		expect(result.lines).toEqual([
			'3 lignes sur 6 figurent aussi dans truncate.py',
			'lignes absentes de truncate.py :',
			'  def shorten(text, limit, marker="..."):',
			'  """Return at most limit words, with a marker when words were dropped."""',
			'  return " ".join(words[:limit]).rstrip(",;:") + marker',
		]);
	});
	it('counts a line shared when only its indent differs', () => {
		expect(compare('    x = 1\ny = 2', 'x = 1', 'a.py').lines).toEqual([
			'1 ligne sur 2 figure aussi dans a.py',
			'lignes absentes de a.py :',
			'  y = 2',
		]);
	});
	it('counts a repeated line each time it appears in the pasted text', () => {
		expect(compare('x = 1\nx = 1\nz', 'x = 1', 'a.py')).toEqual({
			shared: 2,
			total: 3,
			onlyHere: ['z'],
			lines: ['2 lignes sur 3 figurent aussi dans a.py', 'lignes absentes de a.py :', '  z'],
		});
	});
	it('reports 0 of 0 for an empty paste, with no lines under the heading', () => {
		expect(compare('\n  \n', 'x = 1', 'a.py').lines).toEqual([
			'0 ligne sur 0 figure aussi dans a.py',
			'lignes absentes de a.py :',
		]);
	});
});
