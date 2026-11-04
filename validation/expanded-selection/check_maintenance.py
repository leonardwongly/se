#!/usr/bin/env python3
"""Independent public-CLI checks. Usage: python3 verify_team.py REPOSITORY.

The repository is read/copied, never edited. All fixture mutations are temporary.
No target implementation is imported or used to compute expected results.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile


SKILLS = tuple("se-" + name for name in (
    "what", "why", "who", "where", "how", "when", "zero-trust", "verify",
    "concurrent", "proof", "visualise", "swarm",
))
FILES = tuple(Path(skill) / name for skill in SKILLS
              for name in ("SKILL.md", "agents/openai.yaml"))
IGNORED = {".git", "__pycache__", ".venv"}


def snapshot(root):
    """Inventory bytes, permissions and link text without following symlinks."""
    result = {}
    def visit(path, relative):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            result[relative] = ("link", os.readlink(path), stat.S_IMODE(mode))
        elif stat.S_ISDIR(mode):
            result[relative] = ("dir", stat.S_IMODE(mode))
            for child in sorted(path.iterdir()):
                visit(child, relative + "/" + child.name)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", hashlib.sha256(path.read_bytes()).hexdigest(),
                                stat.S_IMODE(mode))
        else:
            result[relative] = ("special", stat.S_IMODE(mode))
    visit(root, ".")
    return result


def copy_repository(source, destination):
    shutil.copytree(source, destination, symlinks=True,
                    ignore=shutil.ignore_patterns(*IGNORED, "*.pyc", "*.pyo", ".DS_Store"))


def manifest(root):
    """Regenerate the public SHA-256 inventory, independent of validator code."""
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in IGNORED for part in relative.parts):
            continue
        if path.name == ".DS_Store" or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_file() and relative.as_posix() != "MANIFEST.sha256":
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative.as_posix()}\n")
    (root / "MANIFEST.sha256").write_text("".join(rows), encoding="utf-8")


def invoke(script, arguments, cwd):
    return subprocess.run([sys.executable, "-B", str(script), *map(str, arguments)],
                          cwd=cwd, capture_output=True, text=True, timeout=90,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def detail(process):
    return f"exit={process.returncode}; stdout={process.stdout[:1800]!r}; stderr={process.stderr[:1800]!r}"


def check_html(repo, markup, entry, expected_ok, expected_hint=None):
    with tempfile.TemporaryDirectory(prefix="se-oracle-html-") as directory:
        root = Path(directory) / "repository"
        copy_repository(repo, root)
        path = root / entry
        path.write_text(path.read_text(encoding="utf-8").replace("<head>", "<head>\n" + markup, 1),
                        encoding="utf-8")
        require(markup in path.read_text(encoding="utf-8"), "fixture injection failed")
        manifest(root)
        before = snapshot(root)
        process = invoke(root / "scripts/validate.py", [], root)
        require(snapshot(root) == before, "validator modified package bytes or paths")
        require((process.returncode == 0) == expected_ok, detail(process))
        if expected_hint:
            require(expected_hint.lower() in (process.stdout + process.stderr).lower(), detail(process))


def install(repo, destination):
    destination.mkdir(parents=True)
    for relative in FILES:
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((repo / relative).read_bytes())


def check_install(repo, setup=None, expected_ok=True, no_arguments=False, repeat=False):
    with tempfile.TemporaryDirectory(prefix="se-oracle-installed-") as directory:
        arena = Path(directory)
        # The checker itself also runs from a copy, avoiding writes to supplied repo.
        package = arena / "repository"
        copy_repository(repo, package)
        destination = arena / "installed skills with spaces"
        install(repo, destination)
        selected = setup(arena, destination) if setup else destination
        selected = selected if selected is not None else destination
        before = snapshot(arena)
        args = [] if no_arguments else ["--skills-dir", selected]
        process = invoke(package / "scripts/check_installed.py", args, arena)
        require(snapshot(arena) == before, "checker modified installed/repository/external bytes or paths")
        require((process.returncode == 0) == expected_ok, detail(process))
        try:
            decoded = json.loads(process.stdout)
        except (json.JSONDecodeError, ValueError) as error:
            raise AssertionError(f"stdout must be machine-readable JSON: {detail(process)}") from error
        require(isinstance(decoded, (dict, list)), "JSON result must be structured")
        if repeat:
            again = invoke(package / "scripts/check_installed.py", args, arena)
            require((again.returncode, again.stdout, again.stderr) ==
                    (process.returncode, process.stdout, process.stderr), "result was not deterministic")
            require(snapshot(arena) == before, "repeated checker modified fixture")


def missing(relative):
    def setup(arena, destination):
        (destination / relative).unlink()
    return setup


def modified(relative):
    def setup(arena, destination):
        target = destination / relative
        # Harmless executable-looking text; any execution would create an observable marker.
        target.write_bytes(target.read_bytes() + b"\n# changed bytes\n" +
                           f"touch '{arena / 'EXECUTED'}'\n".encode())
    return setup


def bytes_only(relative):
    def setup(arena, destination):
        target = destination / relative
        target.write_bytes(target.read_bytes() + b"\n")
    return setup


def linked(kind):
    def setup(arena, destination):
        relative = {"package": Path(SKILLS[0]), "agents": Path(SKILLS[0]) / "agents",
                    "file": FILES[0], "metadata": FILES[1]}.get(kind)
        if kind == "root":
            alias = arena / "linked-installation"
            alias.symlink_to(destination, target_is_directory=True)
            return alias
        if kind == "ancestor":
            alias = arena / "linked-parent"
            alias.symlink_to(arena, target_is_directory=True)
            return alias / destination.name
        original = destination / relative
        target = arena / ("external-" + kind)
        original.rename(target)
        original.symlink_to(target, target_is_directory=target.is_dir())
    return setup


def unrelated(arena, destination):
    package = destination / "unrelated-package"
    package.mkdir()
    (package / "SKILL.md").write_text("unrelated and intentionally not a skill\n", encoding="utf-8")
    (package / "unrelated-link").symlink_to(arena / "nonexistent")


def invalid(kind):
    def setup(arena, destination):
        if kind == "missing":
            return arena / "missing-directory"
        path = arena / "ordinary-file"
        path.write_bytes(b"not a directory")
        return path
    return setup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--baseline-base-only", action="store_true",
                        help="Run one negative base-href check to expose the baseline gap")
    args = parser.parse_args()
    repo = args.repository.resolve(strict=True)
    cases = []
    def run(name, function):
        try:
            function()
        except Exception as error:
            cases.append({"case": name, "pass": False, "error": f"{type(error).__name__}: {error}"})
        else:
            cases.append({"case": name, "pass": True})
    if args.baseline_base_only:
        run("base-href-empty-index", lambda: check_html(repo, '<base href="">',
                                                       "docs/index.html", False, "base"))
    else:
        for entry in ("docs/index.html", "docs/skill-map.html"):
            for label, markup in (
                ("local", '<base href="./">'),
                ("remote", '<base href="https://example.invalid/">'),
                ("empty", '<base href="">'),
                ("valueless", '<base href>'),
                ("mixed-case", '<BaSe HREF="./">'),
                ("duplicate-valueless", '<base target="_blank" href href="">'),
            ):
                run(f"{entry}:reject-base-{label}",
                    lambda m=markup, e=entry: check_html(repo, m, e, False, "base"))
            run(f"{entry}:allow-base-target", lambda e=entry: check_html(
                repo, '<base target="_blank">', e, True))
            run(f"{entry}:preserve-missing-link-rejection", lambda e=entry: check_html(
                repo, '<script src="nonexistent-oracle-file.js"></script>', e, False, "missing"))
            run(f"{entry}:preserve-escape-rejection", lambda e=entry: check_html(
                repo, '<a href="../../outside-oracle.html">outside</a>', e, False, "escape"))
        run("installation:exact-all-24-files-spaces-deterministic", lambda: check_install(repo, repeat=True))
        run("installation:ignore-unrelated-package", lambda: check_install(repo, unrelated))
        for relative in FILES:
            run(f"installation:missing:{relative}", lambda r=relative: check_install(repo, missing(r), False))
            run(f"installation:modified:{relative}", lambda r=relative: check_install(repo, modified(r), False))
        for relative in FILES[:2]:
            run(f"installation:trailing-newline:{relative}",
                lambda r=relative: check_install(repo, bytes_only(r), False))
        for kind in ("root", "package", "agents", "file", "metadata"):
            run(f"installation:reject-symlink:{kind}", lambda k=kind: check_install(repo, linked(k), False))
        run("installation:allow-ancestor-alias", lambda: check_install(repo, linked("ancestor"), repeat=True))
        for kind in ("missing", "file"):
            run(f"installation:invalid:{kind}", lambda k=kind: check_install(repo, invalid(k), False, repeat=True))
        run("installation:no-argument", lambda: check_install(repo, expected_ok=False, no_arguments=True))
    output = {"repository": str(repo), "python": sys.version.split()[0],
              "total": len(cases), "passed": sum(case["pass"] for case in cases), "cases": cases}
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0 if all(case["pass"] for case in cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
