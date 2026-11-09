/**
 * The claim checker's rules against what `check_claims.py` prints. The
 * lesson's summaries and sources are read from `site/examples/` itself, and
 * every expected report and claim list here is the Python checker's own
 * output for the same text, run on python3 and python3.9 when the port was
 * written, so a change that makes the two disagree fails here.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { check, findClaims, lookUp, matcher, source, squash } from '@scripts/claim-checker-logic';
import { describe, expect, it } from 'vitest';

const DIR = join(import.meta.dirname, '../../examples/safety/spotting-hallucination');
const read = (name: string) => readFileSync(join(DIR, name), 'utf8');
// Given in reverse name order, so the test also sees the checker search in name order.
const SOURCES = [source('report.txt', read('sources/report.txt')), source('minutes.txt', read('sources/minutes.txt'))];

/** What `check_claims.py sample/summary_1.txt` prints (the proof `all_claims.py`). */
const SUMMARY_1 = [
	'trouvé       2025',
	'             minutes.txt:1  Conseil municipal du 12 juin 2025, point 4 : stationnement des vélos à la gare.',
	'trouvé       890 vélos',
	'             report.txt:3  Un matin de semaine en mars, l’équipe a compté 890 vélos garés à la gare pour 640 arceaux.',
	'trouvé       640 arceaux',
	'             report.txt:3  Un matin de semaine en mars, l’équipe a compté 890 vélos garés à la gare pour 640 arceaux.',
	'trouvé       article 7(3)',
	'             report.txt:5  L’article 7(3) du règlement sur le stationnement des vélos fixe un minimum d’un arceau pour 100 voyageurs montants.',
	'SANS SOURCE  50 voyageurs',
	'SANS SOURCE  38 %',
	'trouvé       2022',
	'             report.txt:7  Les vols de vélos déclarés à la gare ont baissé d’environ un tiers entre 2022 et 2024, après la fermeture nocturne de la partie couverte.',
	'trouvé       2024',
	'             report.txt:7  Les vols de vélos déclarés à la gare ont baissé d’environ un tiers entre 2022 et 2024, après la fermeture nocturne de la partie couverte.',
	'trouvé       300 arceaux',
	'             report.txt:8  L’équipe recommande d’ajouter 300 arceaux, dont 120 couverts, sur le parvis est.',
	'trouvé       120 couverts',
	'             report.txt:8  L’équipe recommande d’ajouter 300 arceaux, dont 120 couverts, sur le parvis est.',
	'SANS SOURCE  9 000 voyageurs',
	'SANS SOURCE  « Des arceaux avant les parkings, toujours. »',
	'4 affirmations sur 12 n’ont pas de source',
];

describe('the lesson samples', () => {
	it('prints the report check_claims.py prints for the first summary', () => {
		const report = check(read('sample/summary_1.txt'), SOURCES);
		expect(report.lines).toEqual(SUMMARY_1);
		expect(report.missing).toBe(4);
		expect(report.entries.filter((e) => e.hit === null).map((e) => e.claim.label)).toEqual([
			'50 voyageurs',
			'38 %',
			'9 000 voyageurs',
			'« Des arceaux avant les parkings, toujours. »',
		]);
	});
	it('finds all but two claims of the second summary, the quote among them', () => {
		const report = check(read('sample/summary_2.txt'), SOURCES);
		expect(report.lines.filter((l) => l.startsWith('SANS SOURCE'))).toEqual([
			'SANS SOURCE  139 %',
			'SANS SOURCE  410 000',
		]);
		expect(report.lines).toContain('trouvé       « Il nous faut des arceaux avant un nouveau parking. »');
		expect(report.lines).toContain('trouvé       7 200 voyageurs');
		expect(report.lines.at(-1)).toBe('2 affirmations sur 12 n’ont pas de source');
	});
});

describe('findClaims', () => {
	it('finds references, figures and quotes in order, and skips a figure inside a quote or a reference', () => {
		expect(findClaims('Section 12 says 1,500 cars. "hi 3 there" and article  7(3) in "x".')).toEqual([
			{ kind: 'reference', label: 'Section 12', needle: 'Section 12' },
			{ kind: 'figure', label: '1,500 cars', needle: '1,500' },
			{ kind: 'quote', label: '« hi 3 there »', needle: 'hi 3 there' },
			{ kind: 'reference', label: 'article  7(3)', needle: 'article  7(3)' },
			{ kind: 'quote', label: '« x »', needle: 'x' },
		]);
	});
	it('reads French text: « » quotes, thousands grouped with a space, accents and % after a figure', () => {
		const text =
			'L’équipe a compté 7 200 voyageurs, soit 38 % de plus. Elle a dit : « bonjour 3 fois ». Puis 12 de plus, 2 à 3 élus et 1 500 000 €.';
		expect(findClaims(text)).toEqual([
			{ kind: 'figure', label: '7 200 voyageurs', needle: '7 200' },
			{ kind: 'figure', label: '38 %', needle: '38' },
			{ kind: 'quote', label: '« bonjour 3 fois »', needle: 'bonjour 3 fois' },
			{ kind: 'figure', label: '12', needle: '12' },
			{ kind: 'figure', label: '2', needle: '2' },
			{ kind: 'figure', label: '3 élus', needle: '3' },
			{ kind: 'figure', label: '1 500 000', needle: '1 500 000' },
		]);
	});
	it('shows a figure without the next word when that word is a stop word or not a word', () => {
		expect(findClaims('About 40 of them and 12 the most and 3.5 percent at 2025.').map((c) => c.label)).toEqual([
			'40',
			'12',
			'3.5 percent',
			'2025',
		]);
	});
	it('finds nothing in a summary without specifics', () => {
		expect(findClaims('Nothing specific here.')).toEqual([]);
		expect(check('Nothing specific here.', SOURCES)).toEqual({
			entries: [],
			missing: 0,
			lines: ['aucune citation, référence ou chiffre trouvé dans le résumé'],
		});
	});
});

describe('matcher', () => {
	const figure = (needle: string) => matcher({ kind: 'figure', label: needle, needle });
	it('matches a figure with or without a thousands comma, as a whole number', () => {
		expect(figure('1500')('we saw 1,500 cars')).toBe(true);
		expect(figure('50')('1.50')).toBe(false);
		expect(figure('50')('50.5')).toBe(false);
		expect(figure('50')('end at 50.')).toBe(true);
	});
	it('copies the Python lookahead, which lets 1,500 match the start of 15000', () => {
		expect(figure('1,500')('15000')).toBe(true);
	});
	it('matches a figure with its thousands grouped by a space, and never the end or start of a longer one', () => {
		const seven = figure('7 200');
		expect(
			['compte 7 200 voyageurs', 'compte 7200', 'compte 7,200', 'compte 17 200', 'compte 7 200 000'].map(seven),
		).toEqual([true, true, true, false, false]);
		expect(['compte 7 200 voyageurs', 'compte 200 voyageurs', '200 000'].map(figure('200'))).toEqual([
			false,
			true,
			false,
		]);
	});
	it('matches a reference with any case and any amount of whitespace', () => {
		expect(matcher({ kind: 'reference', label: '', needle: 'article  7(3)' })('Article 7(3) of')).toBe(true);
		expect(matcher({ kind: 'reference', label: '', needle: 'article 7(3)' })('Article 7(4) of')).toBe(false);
	});
	it('matches a quote ignoring case and whitespace', () => {
		expect(matcher({ kind: 'quote', label: '', needle: 'We  NEED racks' })('said "we need\tracks before')).toBe(true);
		expect(squash('  A \n b  ')).toBe('a b');
	});
});

describe('source and lookUp', () => {
	it('splits a source into lines without an empty last one', () => {
		expect(source('a.txt', 'one\r\ntwo\n')).toEqual({ name: 'a.txt', lines: ['one', 'two'] });
		expect(source('a.txt', '')).toEqual({ name: 'a.txt', lines: [] });
	});
	it('returns the first line in the first file by name, or null', () => {
		const sources = [source('b.txt', 'x 7 y'), source('a.txt', 'no\nhas 7 here')];
		const claim = { kind: 'figure' as const, label: '7', needle: '7' };
		expect(lookUp(claim, sources)).toEqual({ name: 'a.txt', number: 2, line: 'has 7 here' });
		expect(lookUp({ ...claim, needle: '8' }, sources)).toBeNull();
	});
});
