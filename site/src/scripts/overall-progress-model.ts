/**
 * The DOM-free part of the overall progress bar (spec S04 "Progress
 * display"): the summary line and where the continue button points.
 * `overall-progress.ts` draws the bar from these and from `overview.ts`.
 */
import type { Overall } from './overview';

/** The summary line under the bar on the progress page. */
export function overallText(o: Overall): string {
	if (!o.any)
		return `${o.lessons} leçons et ${o.checkpoints} questions de contrôle dans six parcours. Rien n’est commencé.`;
	const started = o.started ? `, ${o.started} en cours` : '';
	return `Leçons terminées : ${o.finished} sur ${o.lessons}${started}. Questions de contrôle réussies : ${o.passed} sur ${o.checkpoints}.`;
}

export interface ContinueLink {
	href: string;
	text: string;
}

/**
 * The continue button once there is progress: the next unfinished lesson;
 * with none left, the first skipped one; with nothing skipped either, the
 * topic map. Null without progress, so the rendered "Commencer par" link stays.
 */
export function continueLink(o: Overall, base: string): ContinueLink | null {
	if (!o.any) return null;
	const target = o.next ?? o.firstSkipped;
	if (target && (o.next || o.finished === 0))
		return { href: `${base}/${target.id}/`, text: `Continuer avec : ${target.title}` };
	if (target)
		return {
			href: `${base}/${target.id}/`,
			text: `Toutes les leçons sont terminées, ${o.skipped} passée${o.skipped > 1 ? 's' : ''}`,
		};
	return { href: `${base}/map/`, text: 'Toutes les leçons sont terminées : voir la carte des thèmes' };
}
