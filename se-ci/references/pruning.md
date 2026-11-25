# Rooting out useless tests

Removing a test removes a guarantee, so every removal needs evidence, a reviewer and the user's
approval.

## Evidence that a test adds no value

Propose removing or merging a test when at least one of these holds, and cite it:

- **Never fails.** It never failed across the observed history (state the number of runs), and it
  is not a required gate.
- **Duplicate.** Another test asserts the same behaviour; when one failed, the other failed for the
  same cause (cite the runs).
- **Tests implementation.** It asserts private helpers, call counts or internal structure rather
  than behaviour a user of the code can observe, and a behaviour test covers the same outcome.
- **Flaky without signal.** It fails without a code change and its failures never pointed at a real
  defect. Prefer fixing it when it covers a behaviour nothing else covers.

## Never remove

- A required gate, or a test a policy or contract names.
- The only test of a behaviour. Rewrite it as a behaviour test instead.
- A test whose failure history you can't see. Missing history is a gap, not evidence.

## Procedure

1. Write the proposal into `CI.md` under "Proposals waiting on approval", with one row per test:
   the test, the evidence, the behaviour that stays covered and by which test.
2. Put the removal in its own reviewable change (a separate commit or pull request), never mixed
   with other CI work, so it can be reviewed and reverted on its own.
3. Land it only after the user approves. In an unattended run, stop at the proposal.
4. After it lands, watch the full-suite runs on the default branch. A defect the removed test would
   have caught is recorded in the recurring failure causes bucket, and the test comes back.
