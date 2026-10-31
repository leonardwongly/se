# Mandatory baseline and project-grounding review

Read-only review of all nine current `outputs/se-skills/se-*/SKILL.md` files on 2026-10-31. Only this review artifact was written. No code, package skill, runtime, or deployment was changed. This is a textual consistency review; the examples below are synthetic response simulations, not tool-driven agent trials or proof of enforcement.

## Findings

### P2 — Unconditional grounding conflicts with generic explanations

Locations: `se-zero-trust/SKILL.md:12,16–18`; shared grounding at `se-how`, `se-why`, `se-what`, `se-when`, `se-where`, `se-who`, and `se-concurrent`, lines 13–19.

`se-zero-trust:12` correctly permits generic explanations without live access, but the next section unconditionally requires confirming a repository/root and inspecting a diff before conclusions. The shared paragraph also requires project identity, contracts, callers/configuration, and actual CI before any conclusions. A standalone conceptual “How does zero trust work?” or “Why validate at the server?” can therefore trigger unnecessary private-project discovery or an unnecessary scope clarification. Even a narrow ownership lookup can be overburdened with irrelevant CI discovery.

Smallest fix: qualify the grounding opening: “For project-specific questions and all code-change work, ground the answer in the actual project. For general concepts, use clearly illustrative examples without private-project access. Inspect only the project facts relevant to the requested conclusion.” Keep the existing identity, contract, runtime-wiring, and actual-command requirements for change work. No extra checklist is needed.

### P2 — Standalone zero-trust skill does not clearly mandate functional verification

Locations: `se-zero-trust/SKILL.md:26–47,49–50,93–108` compared with `se-verify:12–26,43–45,84–89` and `se-how:72–91`.

The zero-trust skill requires review and allowed/denied checks at affected boundaries. It does not clearly require ordinary functional verification on *every* new/modified-code task; that requirement appears explicitly only in the literal-text example. An authorized hardening change could satisfy the written security checks yet omit a project-required functional regression/build check. Unlike `se-verify`, the standalone skill also does not expressly tie those ordinary checks to project manifests/CI and the final combined source state. This is a gap when the other skills are unavailable, rather than a need to duplicate the whole verification skill.

Smallest fix: add one compact baseline paragraph: “Every code change also requires functional verification using applicable commands/checks discovered from this project's manifests, configuration, tests, and CI. Apply this responsibility directly if companion skills are unavailable. Record results against the final stable combined source/configuration state; recheck affected evidence after later edits. Missing required checks prevent an unconditional completion claim.” Existing safe-validation language can continue to govern probes and evidence depth.

## Checks that are already sound

- Source authority and runtime authority are separated: `se-zero-trust:19–20,71–91`, `se-verify:16–26`, and `se-who:36–47` prevent existing code, archived material, task approval, credentials, or CODEOWNERS alone from granting runtime/task authority.
- Project identity and active wiring are explicit: `se-where:30–35,45–47,60–74`; actual project commands are explicit in `se-verify:23–26` and `se-how:82–87`.
- Low-risk edits are not exempt: `se-zero-trust:45–54`, `se-how:89–91`, and `se-verify:43–45` allow grounded review plus a meaningful render/static check without fabricated tests or a full audit.
- Denial means no protected effects, not just a status code: `se-zero-trust:42–44,95–108`, `se-verify:54–63`, and `se-concurrent:101–104`. Legitimate denial audit records are not prohibited by “no protected side effects.”
- Combined-state evidence is explicit in `se-concurrent:92–105` and `se-verify:79–95`. Later changes invalidate affected evidence, rather than requiring every unrelated test to rerun.
- The readiness gates in `se-when:64–77` match `se-verify:114–134`. A missing integration environment remains BLOCKED; it cannot become NOT_APPLICABLE or unconditional PASS through a schedule recommendation.
- Read-only explanations and navigation are explicit in `se-how:23–28`, `se-where:94–97`, `se-zero-trust:11`, and `se-why:70–79`. Defining acceptance does not authorize edits (`se-what:77–80`).
- Repetition of the baseline is defensible for standalone skills. Consolidating it solely into an optional sibling would weaken the requirement. No further role split or ceremony is needed.

## Synthetic response simulations

These are expected response patterns under the intended final policy, using invented fixture facts. No repository inspection, command execution, runtime check, or real change described here occurred.

### 1. Literal UI label change, unchanged behavior and trust boundary

> Changed the fixture button label from “Submit” to “Save.” The reviewed diff and render path contain a literal string; interpolation, escaping, click behavior, and authorization remain unchanged. Zero-trust baseline: reviewed, with no affected boundary identified. The project's existing component render check confirms the new label and unchanged button action. Final combined fixture snapshot: `label-fixture-v2`; local scoped gate: PASS. No additional security tests were warranted.

Expected properties: baseline reviewed, not exempt; a meaningful project-derived check; exact snapshot in a real run; no blanket release claim.

### 2. Dependency update with missing integration environment

> Updated the fixture dependency and lockfile. Provenance, relevant configuration/permission changes, and the affected call path were reviewed. Local project checks pass on `dependency-fixture-v2`; the required provider integration check is BLOCKED because the configured integration service is unavailable. Overall gate: BLOCKED. The affected provider boundary remains unverified, so this is partial implementation, not completed verification. Next: restore the approved integration environment, run the repository's integration command with its valid and denied cases, inspect protected side effects, and bind those results to the same final source state.

Expected properties: local progress retained; no invented success, environment provisioning, or deployment; missing infrastructure remains BLOCKED.

### 3. Two candidate repositories, unclear target

> Both `/fixture/service-a` and `/fixture/service-b` match the requested component, and the conversation does not establish which is intended. I have made no changes. Which repository should receive the change? The bounded discovery notes identify the relevant candidate entry points; implementation and verification decisions remain pending the target selection.

Expected properties: resolve material project identity before mutation; do not assume generated cwd is target; bounded authorized candidate discovery may proceed.

### 4. Archived global-admin document versus maintained tenant-admin contract

> The maintained contract requires tenant-admin authority; the archived global-admin document records an earlier policy and does not replace that current contract. I will use the maintained contract as the expected behavior and trace the active enforcement path against it. For a change, verification must cover the intended tenant-admin action and denial for another tenant, including unchanged protected state. If active code still follows the archived policy, that is an implementation/contract discrepancy to report, not authority to change the policy.

Expected properties: distinguish intended contract from observed runtime behavior; do not elevate archival content; only clarify if current sources leave a genuine unresolved policy conflict.

### 5. General conceptual explanation of zero trust

> Zero trust means each protected operation must be authorized from verified identity and relevant context; being on an internal network or already logged in is not enough. For example, a server checks that the signed-in user may edit the specific tenant's record before writing it, even if the browser already hid the edit button. Verification should demonstrate both an allowed operation and a denied operation with no protected change. This is a conceptual example, not a finding about your project.

Expected properties: no private repository access or code mutation; no fabricated project findings; no full engineering audit or baseline execution claim for a conceptual question.

## Review snapshot digests (SHA-256)

```text
a1e569aec9c8f7a7dc946192088f1920c03c56e37cdea0f3c1dee19ec0467ae8  se-concurrent/SKILL.md
dc8962bb9e40e97bf76115de23693b6b870e14f19e0f2f5f6b5c87bdf57d6529  se-how/SKILL.md
fb5a4512b64d239f8df75a88eccd4f9d4fe735463d9a2e737f57681b7f99718b  se-verify/SKILL.md
29844c4603ebc4eec7177b10a8ec82470daec5d863fe5978232ecf6ac3a3f67b  se-what/SKILL.md
55fccd1f214bfbd63fb02107e7e31440cbc5335246061600c003e45d434ea332  se-when/SKILL.md
0d674ad2d56d42879314fd13312da8273b959b1825b5ef975ae03ad1e29d4779  se-where/SKILL.md
7058a22abbc74fa2782e030b3e2465b0c3ea665d3c5b60e9baea5777eb88f659  se-who/SKILL.md
809dc68387bbae7ab05ac2c622a29ab9c4529a4e149203233af2847601b05888  se-why/SKILL.md
92a1e0bfe4b155afe91ad6a89068e393dee9620379807422a1bb746c2929e5a7  se-zero-trust/SKILL.md
```

## Recheck after coordinator fixes

Re-read the changed grounding and baseline sections and checked the corresponding exact phrases across all nine files. Both P2 findings are resolved for this textual review:

- The seven coordinating/question skills now explicitly distinguish project-specific work from general conceptual examples (`:13–14`). `se-zero-trust:16,25–26` likewise qualifies project inspection and permits conceptual explanation without unrelated repository/private-source access.
- `se-zero-trust:47–50` now requires ordinary functional checks using the actual project's test/build/render commands as applicable, retains final source identity and results, and blocks completion when required checks are unavailable. This closes the standalone verification gap without duplicating the full verification gate implementation.
- `se-verify:54–57` and `se-zero-trust:107–108` explicitly permit redacted security logging when the project contract allows it, while prohibiting unauthorized protected effects.

No remaining material issue found within the requested baseline/grounding review scope. The five synthetic examples remain intended-behavior illustrations, not execution evidence. Full live skill adherence was not tested by this review.

Recheck digests:

```text
3c1fe996c6fbe08216970e2df569913a51c774527402c8b199c69f21356a8b85  se-concurrent/SKILL.md
2adbb13c30fa416eb94238bbc3cfd3fa9493fb63eef3c340df36a1aeafc8abfd  se-how/SKILL.md
cba26212492f47feef0524249b47e05b0ee8c83fde7f1ee41e64f74fe3622911  se-verify/SKILL.md
4a1e676b40d40c47345602a84ed2a2028958c8bc1b14699eaad5e853e4d18a4a  se-what/SKILL.md
cf505b8ccdd19d53e6f9758d6f254e0f5fcac56ef14195ed682cc7a73ef46d94  se-when/SKILL.md
1e7b449143dd30089c949364dac9834dff831930799dcaf83bbce6d7031507f2  se-where/SKILL.md
77d5ed70396af2048ae2f0107a2470f25a313478bbac62b1a5c2dae77453b040  se-who/SKILL.md
9b3d4c5579963f5ce777488cd60565cee62346e08cbd4bb5950b532942898238  se-why/SKILL.md
f9cfa2302923509f038c300d8a761ab07f4a85e4236c848fc949ff47af50df7c  se-zero-trust/SKILL.md
```
