# Mandatory-baseline skill map: validation

Observed on 2026-10-31, Asia/Singapore, using the connected Playwright browser tools. This record supersedes the earlier optional-controls map evidence for the revised fragment.

## Tested source and scope

- Fragment: `docs/fragments/se-skills-map.html`
- SHA-256: `e73bfc916edba3ff4e94aa1c2e3eaee3f76316724e9ef904241766ec79471d88`; 9,815 bytes.
- Preview: `<historical-authoring-workdir>/visual-baseline-preview.html`.
- Tested URL: `http://127.0.0.1:8769/visual-baseline-preview.html`; locators and evaluations targeted the sandboxed iframe.
- After testing, the entire current fragment was confirmed to be an exact substring of the HTML-decoded preview. No fragment edits occurred after these tests.

The six question skills are labeled as needed. Zero-trust review and verification share a separate “Required for every code change” section covering new or modified code with depth scaled to risk. Concurrency is separately labeled optional. These are workflow requirements, not a claim that this map enforces runtime controls or adds approval requirements.

## Actual behavioral checks

All five scenario relevance sets were asserted against expected skill keys. Paths and selected details were captured and inspected:

| Scenario | Observed relevant skills | Observed path/result |
|---|---|---|
| Define a feature | what, why, who | Request → what → Acceptance brief; what detail selected. |
| Explain a design | why, where, how | where → how → why → Read-only explanation; how detail explicitly says explanation alone does not authorize edits. |
| Implement independent changes | what, where, how, when, zero-trust, verify, concurrent | what → where → how → when → concurrent → Security review + integrated verification; zero-trust detail selected. |
| Assess release readiness | what, who, when, zero-trust, verify | Security evidence → Verification evidence → when; detail separates readiness from deployment permission. |
| Review an agent tool boundary | where, zero-trust, verify | where → zero-trust → verify; zero-trust detail selected. |

- Nine skill buttons were counted. Clicking each produced the corresponding detail prefix; all nine assertions passed.
- A simulated `openai:set_globals` event containing existing saved-state keys `scenario: release, selected: zero-trust` restored the release selector and zero-trust detail.
- Focusing the verify button and pressing Enter selected verify and displayed its new mandatory-baseline detail.
- Preview state readback was `{modelContent:{scenario:"release",selected:"verify"},privateContent:null}`.
- A subsequent invalid scenario/selection event preserved the valid verify detail.
- Console inspection after the checks reported zero errors and zero warnings.

## Layout and visual inspection

- Light layout probes at browser widths 768, 736, and 320 pixels (height 1100) reported iframe widths/scroll widths of 736/736, 704/704, and 273/273. No fragment element extended beyond the right edge.
- Dark mode at 320 × 1100 retained nine buttons and no right-edge overflow; observed iframe `innerWidth` was 288 and document scroll width 273.
- Inspected light desktop screenshot at 768 × 1000: the required pair is clearly separate from optional concurrency; labels and details are readable.
- Inspected dark mobile full-page screenshot at 320 × 1100: groups stack, required-baseline text wraps, and all skills/detail remain visible in the page.
- Screenshots: `<historical-authoring-workdir>/visual-baseline-desktop.png` and `<historical-authoring-workdir>/visual-baseline-mobile-dark.png`.

## Security review and limitations

Static review of the fragment found no API calls, external resource imports, privileged actions, or host follow-up messaging. Dynamic text uses `textContent`; restored scenario/skill keys must exist in fixed local maps. State contains only the scenario and skill selection. The only host API use is the optional widget-state interface. These observations are scoped source inspection, not penetration testing or a proof of host isolation.

Actual Codex inline rendering and production host state persistence were not tested. State checks exercised the standalone preview's fallback API and a simulated globals event. Browser engine/version was not recorded; screen-reader behavior, full keyboard navigation, real touch input, and cross-browser behavior were not tested. The local preview server was stopped after validation. No implementation, deployment, or security-enforcement claim beyond this visualization is established by these checks.

## Project-grounding update: current source

On 2026-10-31, the fragment added a visible project-work anchor before the route: “root + revision · local rules + contracts · active paths · test/CI setup”. Project scenarios now begin with Project evidence. The explanation option explicitly describes a general design and starts from Question, avoiding unrelated repository access. Mandatory zero-trust/verification and optional concurrency sections remain unchanged.

- Current SHA-256: `9b1f6648c43b5514c609879db55a23919e29fae034a9c4d3a2d5666cc690f1e9`; 10,038 bytes. This supersedes the earlier digest above.
- Current tested preview: `<historical-authoring-workdir>/visual-grounded-preview.html`; URL `http://127.0.0.1:8769/visual-grounded-preview.html`.
- Read-only comparison confirmed the complete current fragment is exactly embedded in the HTML-decoded tested preview.
- Playwright smoke checks asserted that scope, implementation, release, and agent-boundary paths start with `Project evidence`; the general-design path starts with `Question` and ends with `Read-only explanation`.
- The implementation and release scenarios both retained zero-trust and verify relevance. The general-design scenario highlighted only why/how, without navigation, security review, or verification being triggered.
- All nine buttons remained present. Current scenario paths and highlight sets were captured. State keys, event handling, and click behavior were not modified; the earlier exhaustive selection/state/keyboard tests were not repeated for this text/data-only update.
- Light 768 × 1100, light 320 × 1100, and dark 320 × 1100 layout probes reported matching iframe/document widths of 736, 273, and 273 pixels with no right-edge overflow.
- Inspected `<historical-authoring-workdir>/visual-grounded-mobile-dark.png`: grounding anchor and extended route wrap legibly above the groups; mandatory baseline and optional concurrency remain distinct.
- Console inspection reported zero errors and warnings. The local server was stopped. All earlier host, accessibility, and cross-browser limitations remain.

The update introduced only static text and fixed scenario-data changes. It added no access, API, authority, or external interaction surface; the prior scoped security review still applies to the unchanged interaction implementation.

## Final route ordering: current source

On 2026-10-31, only the implementation scenario's route was adjusted to show security review before the implementation approach, followed by integrated verification:

`Project evidence → /se-what → /se-where → /se-zero-trust → /se-how → /se-when → /se-concurrent → Integrated /se-verify`

- Current SHA-256: `1a51a96d40fb9da42ae6e445c4b013c4423d26f404ef1f3f60d4f13ef3a6520c`; 10,032 bytes. This supersedes previous digests.
- Current preview: `<historical-authoring-workdir>/visual-security-order-preview.html`. Full fragment equality within the HTML-decoded preview was confirmed.
- Playwright selected the implementation scenario and asserted the complete route string above: PASS. Nine skill buttons remained present.
- At 320 × 1100 in dark mode, iframe and document scroll widths both measured 288 pixels; no fragment element extended beyond the right edge.
- Inspected `<historical-authoring-workdir>/visual-security-order-mobile-dark.png`; the revised route wraps legibly with zero-trust before how and integrated verify last.
- Console inspection reported zero errors or warnings. The preview server was stopped after checking.
- No other source behavior, state keys, labels, requirements, or security surfaces changed. The earlier bounded interaction/security findings and actual-Codex/cross-browser/accessibility limitations still apply; those unchanged checks were not rerun.
