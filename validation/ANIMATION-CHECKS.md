# Engineering skills animation: local preview evidence

Observed 2026-10-31 using connected Playwright browser tools. The animation is an illustrative local workflow, not evidence that any depicted engineering checks ran.

- Source: `docs/fragments/se-skills-animation.html`
- SHA-256: `d84edfdf5c6318e3ef6758aae59d06c52b66c111f8257c05559e7ca32a9f8276`
- Preview: `docs/index.html`
- URL: `http://127.0.0.1:8771/visual-animation-preview.html`
- Complete source exactly matches the fragment embedded in the HTML-decoded preview.

## Meaningful runtime observations

- Playback advanced from stage 0 to 1 and remained playing; Pause held stage 1 for more than the 1.9-second interval.
- Step advanced through the optional split and integration stages.
- Actual token B displacement was measured, rather than inferred from stage text: its CSS transform changed from approximately `(9,143)` to `(187,263)` to `(390,275)` through branch motion.
- Two tokens were visible at split and early merge. Token B moved toward the merge point (approximately `(66,310)` mid-motion); only one remained after completion.
- Revision A failure text appeared at the failed verification stage and remained during repair. Repair explicitly rechecks affected trust assumptions while reusing valid review.
- Revision B verification displayed “Revision A: FAIL retained → revision B: required checks PASS”.
- Playback from stage 10 automatically stopped at final stage 11, with Play disabled. Replay reset to stage 0 and started playback; Pause then stopped it.
- Dark mode with reduced motion paused playback. Keyboard Enter on Step advanced to stage 1, with zero running animations.
- At 320 × 1100, the narrow-layout probe reported no elements extending beyond the right edge. All diagram labels and controls remained accessible in the page.
- Console inspection reported zero errors and zero warnings.

## Visual inspection and fixes

- Inspected light desktop at 768 × 1100: `validation/visual-animation-desktop.png`.
- Inspected dark mobile at 320 × 1100: `validation/visual-animation-mobile-dark.png`.
- Initial playback check failed because preview state echoes restored the current stage and stopped playback; a Pause locator timed out. Fixed by ignoring same-stage restoration echoes. The repeated check passed.
- Prevented ResizeObserver height-only notifications from canceling stage motion; viewport-width changes still reposition geometry. Split and merge motion use elbow keyframes, with both tokens reaching integration before the second hides.

## Boundaries

Source inspection found no external imports, API calls, follow-up messages, or privileged actions. Restored state is restricted to a fixed example ID and integer stage range; text uses textContent. Host access is limited to optional widget state. This is a scoped source review, not a host-isolation assessment.

Actual Codex inline rendering, production host persistence, real touch input, screen-reader behavior, and cross-browser behavior were not tested. Browser engine/version was not recorded. Uninterrupted playback of all twelve stages was not timed end-to-end.

## Independent parent checks

Parent inspected both screenshots and reloaded the preview in a fresh browser session. Replay advanced to stage 1; Pause held that stage for 2.1 seconds; Step advanced to stage 2; resumed playback ran continuously through stage 11 and stopped automatically with Play disabled. The final state retained revision A's FAIL alongside revision B's passing checks. Independent semantic review found no remaining issues after the repair trust-review clarification. The skill ZIP remained unchanged. Temporary preview server cleanup followed these checks.
