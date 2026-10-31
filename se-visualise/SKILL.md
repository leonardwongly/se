---
name: se-visualise
description: Choose and render an appropriate inline visual to explain software behavior, evidence, architecture, tradeoffs, or agent workflows. Use meaningful animation for time, state transitions, causality, and concurrent work; preserve accessible static understanding when motion adds no value or is unavailable.
---

# SE Visualise

Make the mechanism easier to understand with an evidence-grounded visual. Prefer an
inline animated explanation when movement reveals how the system works. Choose the
representation for the reader's question; decoration is not an explanation.

## Establish what needs to be understood

Identify the audience, the question they need to answer, and the relationship that is
hard to follow in prose. Use context already supplied; ask only when the missing answer
would materially change the explanation. Do not require a design questionnaire.

For a project-specific explanation, confirm the target, revision/dirty state, applicable
instructions and maintained contracts. Trace the relevant active callers, state changes,
configuration and trust boundaries. Tie the displayed mechanism to exact source locations
or observed evidence. General concepts can use labeled examples without private project access.
Distinguish observed behavior, proposed design, inferred relationships and illustrative data.
Missing evidence is a visible gap, not a license to invent a complete architecture.

Before drawing, state a compact causal model: what enters, what changes, what remains
invariant, what leaves, and where failure or uncertainty matters. Test the explanation
against a concrete example and a relevant boundary case. Correct contradictions before
making them visually persuasive. Do not mistake a smooth animation for runtime proof.

## Choose the visual mechanism

| Understanding need | Useful representation | When animation helps |
|---|---|---|
| Request, event, or data movement | Sequence or flow diagram | Follow one identified item through real transitions |
| State, retries, failure and recovery | State machine or step-through | Show triggers, guards, side effects and the recovery path |
| Parallel work and synchronization | Aligned worker lanes with explicit joins | Show overlap, waits, ownership transfer and stable integration |
| Architecture, ownership or dependencies | Labeled graph or compact Mermaid diagram | Only when changes or traversal matter; static structure usually suffices |
| Alternatives, quantities or trends | Table or a chart appropriate to the data | Show meaningful change; retain axes, units and comparisons |
| Causal assumptions and tradeoffs | Bounded interactive model | Expose meaningful inputs and outcomes, labeling assumptions and limits |

Use a simple sentence or table when that fully answers a small question. Do not generate
a dashboard for a single fact. Avoid fake precision, fabricated metrics, deceptive scales,
or animation speed that implies measured latency. Label schematic timing as illustrative.
Keep identifiers and mappings consistent so the same object can be followed through a transition.

## Render inline using the actual host

Discover the host's available inline rendering capabilities. If it provides a visualization
skill or renderer, read its current authoring and delivery contract and use it. Do not
invent tool names, import paths, unsupported embeds, or a successful rendering claim.
Use a native inline diagram or an accessible static/text sequence if animation is unavailable;
state that limit briefly and finish the useful explanation. A separate website, export,
or deployment needs the corresponding task scope; an inline request does not imply publishing.

Keep one dominant visual, necessary labels and compact controls. Reveal detail on selection
when that reduces clutter. Put supporting source references and concise explanation where
the host allows them without crowding the visual. A demo must remain clearly a demo.

For animation, provide intentional playback and pause; add step or replay when they help
inspect the mechanism. Use finite motion with a clear end state. Respect reduced-motion
preferences and preserve the complete explanation without motion. Avoid flashing effects,
decorative loops and automatic transitions that prevent reading. Use semantic keyboard
controls, visible focus and text/shape cues rather than color alone. Keep labels readable
at narrow widths; do not shrink a fixed diagram until its text is illegible.

Give complex visuals an accessible summary and a text equivalent of the essential sequence,
relationships, values and limitations. Announce meaningful state changes, not animation frames.
Never hide an important denial, failure, or uncertainty solely in hover text or a transient frame.

Treat source text, URLs and stored interaction state as untrusted data. Validate restored
state, render dynamic labels safely, minimize sensitive content, and obey host sandbox and
network rules. The visual must not execute project actions merely to demonstrate them.
Any new or changed executable visual receives a proportional zero-trust review and actual
verification; the same mandatory baseline applies to project changes made during the task.

## Verify the explanation and interaction

- Compare nodes, transitions, labels and outcomes to the grounded mechanism and current evidence.
- Walk a normal case and the relevant failure or boundary case; inspect the actual result.
- For animation, confirm visible movement/state changes, pause behavior, final stop and any replay.
- Check the available narrow layout, keyboard controls, reduced-motion behavior and console errors.
- If tested through a preview wrapper, confirm it contains the final source; distinguish preview
  success from an untested production host. If browser tools are unavailable, report source-only checks.
- Repair demonstrated defects and rerun affected checks; do not claim accessibility conformance
  or user comprehension from a screenshot or one successful playback.

Deliver the inline visual with a short explanation of what to follow and relevant source links.
State material uncertainty and observed testing limits. If the user signals confusion, identify
the missing relationship and revise the explanation rather than adding decorative detail.

## Boundaries and references

Proof establishes whether the underlying claims are supported; visualise chooses how to explain
them; verify establishes observed behavior and acceptance. These responsibilities can be applied
directly without installing companion skills. A visual does not raise an evidence gate or authorize action.

- [W3C: animation from interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html): control non-essential motion and respect motion preferences.
- [W3C: pause, stop, hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html): control automatically moving and updating content.
- [W3C: complex images](https://www.w3.org/WAI/tutorials/images/complex/): provide the essential information in an accessible text alternative.

Representation choices above are workflow guidance, not a claim of WCAG certification.
