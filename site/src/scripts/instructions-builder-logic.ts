/**
 * The file the instructions builder (`widgets/InstructionsBuilder.astro`)
 * shows: an AGENTS.md drawn from the facts the learner ticked and the short
 * fields they filled in. Pure functions, no DOM, so they run under Node in
 * the unit tests. The DOM half is `instructions-builder.ts`.
 */

/** Every optional line of the file, in the order the form shows them. Each has a checkbox and a text field. */
export const OPTIONAL_LINES = ['runtime', 'test', 'lint', 'branch', 'notouch', 'mistake'] as const;

/** One optional line. */
export type OptionalLine = (typeof OPTIONAL_LINES)[number];

/** One optional line as the form holds it: whether it is ticked, and its trimmed text. */
export interface LineInput {
	on: boolean;
	text: string;
}

/** What the form holds, with every text already trimmed. */
export interface BuilderInput {
	name: string;
	purpose: string;
	lines: Record<OptionalLine, LineInput>;
}

/** The text of a ticked line, or its placeholder when the field is empty. */
function valueOr(line: LineInput, placeholder: string): string {
	return line.text || placeholder;
}

/** The AGENTS.md text for `input`, ending in one newline. A section with no ticked line is left out. */
export function buildInstructions(input: BuilderInput): string {
	const { lines: l } = input;
	const out: string[] = [`# ${input.name || 'mon-projet'}`];
	if (input.purpose) out.push('', input.purpose);

	const commands: string[] = [];
	if (l.runtime.on) commands.push(`- Environnement : ${valueOr(l.runtime, '<langage et version>')}`);
	if (l.test.on) commands.push(`- Tests : \`${valueOr(l.test, '<commande de test>')}\``);
	if (l.lint.on) commands.push(`- Style et mise en forme : \`${valueOr(l.lint, '<commande de style>')}\``);
	if (commands.length > 0) out.push('', '## Commandes', '', ...commands);

	const rules: string[] = [];
	if (l.branch.on) rules.push(`- ${valueOr(l.branch, '<règle de branche>')}`);
	if (l.notouch.on) rules.push(`- Ne jamais modifier : ${valueOr(l.notouch, '<chemins>')}`);
	if (l.mistake.on) rules.push(`- ${valueOr(l.mistake, '<l’erreur à arrêter, et quoi faire à la place>')}`);
	if (rules.length > 0) out.push('', '## Règles', '', ...rules);

	return `${out.join('\n')}\n`;
}

/** The line count next to the file name, counting only lines with text: `1 ligne non vide`, `7 lignes non vides`. French takes the singular for 0 and 1. */
export function lineCountText(file: string): string {
	const n = file.split('\n').filter((line) => line.trim().length > 0).length;
	return n > 1 ? `${n} lignes non vides` : `${n} ligne non vide`;
}
