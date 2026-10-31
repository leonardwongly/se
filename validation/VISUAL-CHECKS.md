# Historical interactive skill map: observed validation

This record and its original screenshots are superseded by the [project-grounded baseline map record](code-baseline/VISUAL-CHECKS.md). “Current” below refers to that historical run.

Checks performed on 2026-10-31, Asia/Singapore, using the connected Playwright browser tools against a locally served standalone sandbox preview. Browser engine/version was not recorded.

- Fragment: `docs/fragments/se-skills-map.html`
- Preview: `docs/fragments/visual-preview.html`
- Tested URL: `http://127.0.0.1:8769/visual-preview.html`; interactions targeted its sandboxed iframe.
- Current fragment SHA-256: `da2a371a182838ebc4f33cef470461a3307e9e04b5953cffac7d13db2ba6618e` (9,383 bytes).

## Observed checks

| Action | Observed result |
|---|---|
| Count skill buttons | Nine buttons present. |
| Choose Define a feature | Relevant skills: what, why, who; detail selected what. |
| Choose Explain a design | Relevant skills: why, where, how; detail selected why. |
| Choose Implement independent changes | Relevant skills: what, where, how, when, concurrent, verify; detail selected how. |
| Choose Assess release readiness | Relevant skills: what, who, when, verify; detail selected when. |
| Choose Review an agent tool boundary | Relevant skills: where, zero-trust, verify; detail selected zero-trust. |
| Click each of the nine skills | Each detail began with the corresponding `/se-<name>` label; all nine assertions passed. |
| Dispatch `openai:set_globals` with saved release/who state | Detail changed to who and described evidenced roles and the ownership/permission boundary. |
| Focus verify button, press Enter | Detail changed to verify. |
| Read preview `window.openai.widgetState` | Stored `{modelContent:{scenario:"release",selected:"verify"},privateContent:null}`. |
| Dispatch invalid saved scenario/selection | Existing verify detail remained unchanged; no invalid selection rendered. |
| Inspect console | Playwright reported zero errors and zero warnings at the time of inspection. |

Scenario checks asserted relevance sets and selected details. The release path `Acceptance → /se-verify → /se-when` was visually inspected; every scenario path string was not separately asserted.

## Layout and screenshots

- At browser viewports 736 × 1100 and 320 × 1100, the iframe reported widths of 704 and 273 pixels respectively. Document/body scroll widths matched those widths, and the overflow probe found no fragment element extending beyond the iframe's right edge.
- Visually inspected the light desktop screenshot at 768 × 900. All nine skills appeared in three groups of three with readable labels and selected detail.
- Visually inspected the dark mobile screenshot at 320 × 1100 after dark-color-scheme emulation. Skills stacked, all nine buttons remained present, and the selected detail wrapped. The full-page screenshot extends beyond the viewport height.
- Desktop screenshot, moved by parent after capture: `<historical-authoring-workdir>/visual-desktop.png`.
- Mobile screenshot, moved by parent after capture: `<historical-authoring-workdir>/visual-mobile-dark.png`.

## Source identity and limits

The last fragment edit changed relevance markers to distinguish active squares from inactive circles before generating the tested preview. No fragment edits were made after the runtime checks. A follow-up read-only check confirmed the complete current fragment is an exact substring of the HTML-decoded tested preview, so these checks apply to the current fragment bytes above. No semantic visual edits occurred after creation.

The local server was stopped after validation. Initial direct `file:` navigation was blocked; the successful runtime checks used the localhost URL. Actual Codex inline rendering, host-backed persistence across chats, screen-reader behavior, real touch input, and cross-browser behavior were not tested. The preview state test demonstrates its fallback state API, not production host persistence. Keyboard validation covered Enter activation of one focused skill button, not a complete accessibility audit. No external API or network-dependent visualization behavior was introduced.
