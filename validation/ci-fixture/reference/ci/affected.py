"""Print the flows a change affects, as `flows=<comma list>` for $GITHUB_OUTPUT.

    python ci/affected.py --base <sha>      # pull request: diff against the base
    python ci/affected.py                   # no base (push, schedule): every flow
"""
import argparse
import subprocess

FLOWS = ("billing", "api", "reports")
# Path prefix -> flows it affects. Shared foundations affect every flow.
SHARED = ("app/config.py", "app/__init__.py", "requirements.txt", ".github/", "ci/", "tests/__init__.py")
MAP = {
    "app/billing/": ("billing", "api"),
    "tests/billing/": ("billing",),
    "app/api/": ("api",),
    "tests/api/": ("api",),
    "app/security.py": ("api",),
    "tests/security/": (),
    "app/reports/": ("reports",),
    "app/cli.py": ("reports",),
    "tests/reports/": ("reports",),
}


def affected(paths):
    flows = set()
    for path in paths:
        if path.startswith(SHARED):
            return set(FLOWS)
        match = [flows_ for prefix, flows_ in MAP.items() if path.startswith(prefix)]
        if not match:
            return set(FLOWS)  # unmapped path: impact unknown, run everything
        flows.update(*match)
    return flows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="")
    args = parser.parse_args()
    if not args.base:
        selected = set(FLOWS)
    else:
        diff = subprocess.run(["git", "diff", "--name-only", f"{args.base}...HEAD"],
                              capture_output=True, text=True, check=True).stdout.split()
        selected = affected(diff)
    print("flows=" + ",".join(flow for flow in FLOWS if flow in selected))


if __name__ == "__main__":
    main()
