import {
	type BuilderInput,
	buildInstructions,
	lineCountText,
	OPTIONAL_LINES,
	type OptionalLine,
} from '@scripts/instructions-builder-logic';
import { describe, expect, it } from 'vitest';

/** An input with every optional line in `on` ticked and empty, and no name or purpose. */
function form(on: OptionalLine[] = [], texts: Partial<Record<OptionalLine, string>> = {}): BuilderInput {
	const lines = {} as BuilderInput['lines'];
	for (const key of OPTIONAL_LINES) lines[key] = { on: on.includes(key), text: texts[key] ?? '' };
	return { name: '', purpose: '', lines };
}

describe('buildInstructions', () => {
	it('writes only the default heading when nothing is filled in or ticked', () => {
		expect(buildInstructions(form())).toBe('# mon-projet\n');
	});
	it('writes the name and the purpose paragraph', () => {
		expect(buildInstructions({ ...form(), name: 'invoice-mailer', purpose: 'Sends invoices.' })).toBe(
			'# invoice-mailer\n\nSends invoices.\n',
		);
	});
	it('writes a placeholder for each ticked line with an empty field', () => {
		expect(buildInstructions(form([...OPTIONAL_LINES]))).toBe(
			[
				'# mon-projet',
				'',
				'## Commandes',
				'',
				'- Environnement : <langage et version>',
				'- Tests : `<commande de test>`',
				'- Style et mise en forme : `<commande de style>`',
				'',
				'## Règles',
				'',
				'- <règle de branche>',
				'- Ne jamais modifier : <chemins>',
				'- <l’erreur à arrêter, et quoi faire à la place>',
				'',
			].join('\n'),
		);
	});
	it('writes the field text of each ticked line and leaves out unticked ones and empty sections', () => {
		const out = buildInstructions(
			form(['test', 'notouch'], { test: 'uv run pytest', notouch: 'uv.lock', runtime: 'Python 3.13' }),
		);
		expect(out).toBe(
			'# mon-projet\n\n## Commandes\n\n- Tests : `uv run pytest`\n\n## Règles\n\n- Ne jamais modifier : uv.lock\n',
		);
		expect(out).not.toContain('Python');
	});
	it('leaves out the Commands section when only rules are ticked, and the Rules section when only commands are', () => {
		expect(buildInstructions(form(['branch'], { branch: 'Never commit to main' }))).toBe(
			'# mon-projet\n\n## Règles\n\n- Never commit to main\n',
		);
		expect(buildInstructions(form(['lint', 'runtime'], { lint: 'ruff check .' }))).toBe(
			'# mon-projet\n\n## Commandes\n\n- Environnement : <langage et version>\n- Style et mise en forme : `ruff check .`\n',
		);
	});
	it('writes the mistake line as given', () => {
		expect(buildInstructions(form(['mistake'], { mistake: 'Do not add retries.' }))).toContain(
			'## Règles\n\n- Do not add retries.\n',
		);
	});
});

describe('lineCountText', () => {
	it('counts only lines with text', () => {
		expect(lineCountText('# a\n\n  \nb\n')).toBe('2 lignes non vides');
	});
	it('uses the singular for one line or none, as French does', () => {
		expect(lineCountText('# mon-projet\n')).toBe('1 ligne non vide');
		expect(lineCountText('\n')).toBe('0 ligne non vide');
	});
});
