# Custom guide and README media validation

Final local checks: 4 November 2026. Scope: the standalone guide and repository media, not skill installation, a production project, or a deployed website.

## Observed checks

- All twelve skill buttons selected the matching detail panel and invocation label.
- The 13-stage workflow retained revision A's failed check after revision B passed. Final wording limits the result to local scope.
- Actual playback moved the second worker token, paused without advancing for 1,900 ms (longer than a 1,750 ms stage), resumed, and stopped at stage 12. Replay restarted the sequence.
- Reduced-motion replay stayed paused; keyboard Step advanced the sequence. Final recheck at a 320 px viewport found no horizontal overflow (305 px client and scroll widths) and zero running animations.
- The final browser run reported zero console errors or warnings. The earlier missing favicon was corrected with a local data favicon.
- The compatibility URL `docs/skill-map.html` reached `index.html#skills`.
- Desktop workflow and skill-panel screenshots and a full mobile capture were visually inspected. The complete text sequence remains available without animation.
- An independent source review found a README diagram mismatch. It was corrected to make swarm work optional for repairs and include trust review of the final combined diff before verification.

## Media provenance

The PNGs are browser captures of the actual custom UI. The GIF was encoded with FFmpeg from 150 browser frames recorded at a target 6 fps; every workflow stage was observed during capture. It is 865 × 692 px, 27.83 seconds and 355,310 bytes, with looping disabled. It illustrates a fictional engineering change; it is not evidence of a live agent run or real verification result. Its persistent label makes that boundary visible inside the media.

README supplies a static workflow image outside the expandable animation, so readers can choose whether to show motion. The local guide adds Play/Pause, Step and Replay controls and reduced-motion support. The skill overview PNG is 865 × 648 px.

### Final source and media hashes

- `docs/index.html`: `67c0e9cfa779f746b2c47dd857877186462573d520f727c1b39c00a745b75a3b`
- `docs/assets/guide.css`: `c7809afac821762d67e6dd699484884899b7998bcecb3a2844bda3b78fdcb6d5`
- `docs/assets/guide.js`: `f484bc992d809893d753b400bca07a70ee6be255d65bbe78acc680c7bb7a94a5`
- `docs/images/workflow.png`: `80c10df47c4672909fd4c60e86101d4db879ea1fd58f34c12328c63d82af331c`
- `docs/images/skills-overview.png`: `ec765d22676a50b31af41683d5e3b90413aef3b0c43a67dd2032a5f075555648`
- `docs/images/workflow.gif`: `1a334cd5b3796c95fb311615c553762a23e750bd553806d0c099055215ed0fde`

## Reproduction and limits

Run `python3 -m http.server 8000 --bind 127.0.0.1 --directory docs` from the repository and open `http://127.0.0.1:8000/`. Use the playback controls and all twelve skill selectors; enable reduced motion to inspect the static step-through behavior. Run `node --check docs/assets/guide.js` for JavaScript syntax and `python3 scripts/validate.py` for package integrity and the retained synthetic behavior checks.

These are local browser checks, not a full screen-reader audit or cross-browser certification. Earlier animation and agent-exercise records describe older artifacts and remain historical. Publishing the source and README media does not deploy a public interactive website or establish production readiness.
