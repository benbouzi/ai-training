/**
 * The toy model of the repeated-runs widget (`widgets/RepeatedRuns.astro`),
 * a port of `site/examples/concepts/same-prompt-twice/sample.py`, which
 * stays in CI as the lesson's proof. Five candidate answers to one question
 * have fixed scores. Each run turns the scores into probabilities at a
 * temperature, draws one answer, and the report counts how many runs agree
 * with run 1 and, with the check on, how many name Canberra.
 *
 * The widget prints the lines the Python program prints, in the same
 * format. The draws differ: the Python program takes its random numbers
 * from a fixed seed, so the page can show one recorded set of runs, and the
 * widget takes fresh ones on every press, so the learner sees the counts
 * move. No DOM access, so it runs under Node in the unit tests.
 */

/** `QUESTION` in `sample.py`. */
export const QUESTION = 'Quelle est la capitale de l’Australie ?';

/** `CANDIDATES` in `sample.py`: each answer and its made-up score. Only the order and the distances matter. */
export const CANDIDATES: readonly (readonly [string, number])[] = [
	['Canberra', 3.0],
	['Canberra.', 2.4],
	['La capitale de l’Australie est Canberra.', 2.0],
	['C’est Canberra.', 1.2],
	['Sydney', 0.4],
];

/** `JITTER` in `sample.py`: the standard deviation of the shake each score gets before a pick. */
export const JITTER = 0.4;

/** The number of runs one press makes, the `--runs 10` the lesson uses. */
export const RUNS = 10;

/** `probabilities` in `sample.py`: temperature 0 or below puts all of the probability on the top score. */
export function probabilities(scores: readonly number[], temperature: number): number[] {
	if (temperature <= 0) {
		const top = Math.max(...scores);
		return scores.map((s) => (s === top ? 1 : 0));
	}
	const weights = scores.map((s) => Math.exp(s / temperature));
	const total = weights.reduce((a, w) => a + w, 0);
	return weights.map((w) => w / total);
}

/** A number from the normal distribution with mean 0 and standard deviation `sd`, by the Box-Muller method. */
export function gauss(random: () => number, sd: number): number {
	const u = 1 - random();
	const v = random();
	return sd * Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

/** `pick` in `sample.py`: one run. Shakes the scores when `jitter` is on, then draws one answer. */
export function pick(random: () => number, temperature: number, jitter: boolean): string {
	let scores = CANDIDATES.map(([, score]) => score);
	if (jitter) scores = scores.map((score) => score + gauss(random, JITTER));
	const probs = probabilities(scores, temperature);
	const draw = random();
	let running = 0;
	for (const [i, [answer]] of CANDIDATES.entries()) {
		running += probs[i] ?? 0;
		if (draw < running) return answer;
	}
	// Rounding can leave the running total just under 1. sample.py takes the last candidate then.
	return CANDIDATES[CANDIDATES.length - 1]?.[0] ?? '';
}

/** `passes` in `sample.py`: the check a workflow can apply, that the answer names Canberra in any wording. */
export function passes(answer: string): boolean {
	return answer.toLowerCase().includes('canberra');
}

/** `essais` in `sample.py`: `n essai` or `n essais`, the French plural from 2 on. */
export function essais(n: number): string {
	return `${n} essai${n > 1 ? 's' : ''}`;
}

/** The settings of one press: the temperature, and the `--jitter` and `--check` switches. */
export interface RunSettings {
	temperature: number;
	jitter: boolean;
	check: boolean;
}

/** What one press shows: a heading, one line per run, and the summary lines. */
export interface RunReport {
	heading: string;
	lines: { text: string; ok: boolean }[];
	summary: string[];
}

/** The report for `answers`, in the lines `main` in `sample.py` prints without `--quiet`. */
export function report(answers: readonly string[], settings: RunSettings): RunReport {
	const heading = `${QUESTION} (température ${settings.temperature.toFixed(1)}, ${essais(answers.length)})`;
	const lines = answers.map((answer, i) => {
		const number = String(i + 1).padStart(2);
		const ok = passes(answer);
		if (!settings.check) return { text: `${number}  ${answer}`, ok: true };
		return { text: `${number}  ${(ok ? 'ok' : 'ÉCHEC').padEnd(5)}  ${answer}`, ok };
	});
	const same = answers.filter((a) => a === answers[0]).length;
	const summary = [
		`${essais(same)} sur ${answers.length} ${same > 1 ? 'donnent' : 'donne'} la même réponse que l’essai 1`,
	];
	if (settings.check) {
		const ok = answers.filter(passes).length;
		summary.push(
			`${essais(ok)} sur ${answers.length} ${ok > 1 ? 'passent' : 'passe'} le contrôle : la réponse nomme Canberra`,
		);
	}
	return { heading, lines, summary };
}

/** One press: `runs` draws with `settings`, and their report. */
export function runMany(random: () => number, settings: RunSettings, runs: number = RUNS): RunReport {
	const answers = Array.from({ length: runs }, () => pick(random, settings.temperature, settings.jitter));
	return report(answers, settings);
}
