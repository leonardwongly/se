# pstack port data

Evidence for [spec 001](../../specs/001-pstack-integration/spec.md), from pstack commit
`c3464c11c60b1352d5e8f5f0428a3a6943837568`.

- `source-edges.json`: every reference from one pstack skill to another, written by
  `scripts/port_pstack.py --edges` and expressed with the SE names (`se-principles#<slug>` for a
  principle, `dropped:<name>` for a skill that was not ported).
- `removed-edges.json`: source references with no SE counterpart, each with its reason.

`scripts/test_port_pstack.py` fails if a source reference is neither present in the SE package nor
listed here.
