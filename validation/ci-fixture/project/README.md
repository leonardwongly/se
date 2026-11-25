# Ledger

A small invoicing service.

- `POST /invoice` is handled by `app.api.handlers.handle_invoice`.
- Monthly reports run from the command line: `python -m app.cli [--csv] < rows.json`.

Run the tests with `python -m unittest discover -s tests -t . -v`.

This checkout has no remote. Its CI run history, pull requests and issues are exported under
`.ci-history/` (`runs.json`, `pulls.json`, `issues.json`).
