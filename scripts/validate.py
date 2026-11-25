"""Portable package integrity and synthetic behavior checks; Python >= 3.10."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib
import json
import os
import re
import subprocess
import sys

from port_pstack import DROPPED as PSTACK_DROPPED, NAMES as PSTACK_NAMES, PINNED_COMMIT as PSTACK_COMMIT

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {f'se-{name}' for name in (
    'what', 'why', 'who', 'where', 'how', 'when', 'zero-trust', 'verify', 'concurrent',
    'proof', 'visualise', 'swarm',
    # Ported from pstack: specs/001-pstack-integration.
    'playbook', 'help', 'setup', 'principles', 'explain', 'context', 'restate', 'design',
    'contest', 'challenge', 'deepen', 'blueprint', 'states', 'test-first', 'typescript',
    'comments', 'prose', 'writing', 'harness', 'harness-sync', 'formal', 'formal-sync',
    'benchmark', 'impact', 'decision-log', 'recap', 'recap-video', 'plain', 'style',
    'guardrail', 'retro',
    # CI optimisation: specs/002-ci-optimization.
    'ci',
)}
DESCRIPTION_LIMIT = 1024
NOTICE = 'THIRD_PARTY_NOTICES.md'
_NAME = r'se-[a-z0-9]+(?:-[a-z0-9]+)*'
_END = r'(?![\w\-/]|\.\w)'
SKILL_COMMAND = re.compile(rf'(?<![\w/.\-])/({_NAME}){_END}')
SKILL_TOKEN = re.compile(rf'(?<![\w/.\-@])({_NAME}){_END}')
BRAND_RESIDUE = re.compile(
    r'(?i)(?<![\w-])(?:pstack|poteto)(?![\w-])|principle-[a-z]|@cursor-skill')
HOST_RESIDUE = re.compile(
    r'\b[Bb]ug[Bb]ot\b|\.cursor/|\bCustom Mode\b|\bAskQuestion\b|cursor-team-kit|\bCursor\b')
OLD_NAME_RESIDUE = re.compile('|'.join(
    rf'(?<![\w/.\-])/{re.escape(old)}(?![\w\-])|`/?{re.escape(old)}`|\*\*{re.escape(old)}\*\*'
    for old in sorted(set(PSTACK_NAMES) | set(PSTACK_DROPPED), key=len, reverse=True)))
MARKDOWN_LINK = re.compile(r'\]\(([^)]+)\)')


def require(condition, message):
    if not condition:
        raise SystemExit(f'FAIL: {message}')


def package_files():
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(part in {'.git', '__pycache__', '.venv'} for part in relative.parts):
            continue
        if path.name == '.DS_Store' or path.suffix in {'.pyc', '.pyo'}:
            continue
        require(not path.is_symlink(), f'symlink outside package contract: {relative}')
        if path.is_file() and relative.as_posix() != 'MANIFEST.sha256':
            yield relative.as_posix(), path


def run(args, cwd=ROOT):
    result = subprocess.run([sys.executable, '-B', *args], cwd=cwd,
                            capture_output=True, text=True, timeout=60,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    return result, result.stdout + result.stderr


def require_tests(result, output, count, label):
    ran = re.search(r'^Ran (\d+) tests? in ', output, re.M)
    require(result.returncode == 0 and ran is not None and
            int(ran.group(1)) == count and re.search(r'^OK$', output, re.M),
            f'{label}: expected {count} passing tests without skips\n{output}')


class HTMLReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.base_hrefs = []

    def handle_starttag(self, tag, attrs):
        for attribute, target in attrs:
            if tag == 'base' and attribute == 'href':
                self.base_hrefs.append((self.getpos()[0], target))
            if attribute in {'src', 'href'} and target is not None:
                self.references.append((self.getpos()[0], attribute, target))


def validate_html_links(root=ROOT):
    root = root.resolve()
    for name in ('docs/index.html', 'docs/skill-map.html'):
        source = root / name
        require(source.is_file(), f'{name}: missing HTML entry point')
        parser = HTMLReferences()
        parser.feed(source.read_text(encoding='utf-8'))
        parser.close()
        for line, target in parser.base_hrefs:
            require(False, f'{name}:{line}: <base href={target!r}> is unsupported: '
                    'browser URL resolution is not modeled by this static checker')
        for line, attribute, target in parser.references:
            context = f'{name}:{line}: {attribute}={target!r}'
            try:
                url = urlsplit(target.strip())
                if url.scheme or url.netloc or not url.path:
                    continue
                # Split before decoding so encoded ? and # remain filename characters.
                resolved = (source.parent / unquote(url.path, errors='strict')).resolve()
                require(resolved.is_relative_to(root), f'{context}: target escapes repository')
                require(resolved.exists(), f'{context}: missing local target')
            except (ValueError, OSError, RuntimeError) as error:
                require(False, f'{context}: invalid local reference ({error})')


def validate_markdown_links(source, root=ROOT):
    """Check the existing bounded inline-link syntax, not a full Markdown grammar."""
    root = root.resolve()
    source = source.resolve()
    name = source.relative_to(root).as_posix()
    for target in re.findall(r'\]\(([^)]+)\)', source.read_text(encoding='utf-8')):
        context = f'{name}: invalid link {target!r}'
        try:
            url = urlsplit(target.strip())
            if url.scheme or url.netloc or not url.path:
                continue
            # URL delimiters are removed before one strict filename decode.
            resolved = (source.parent / unquote(url.path, errors='strict')).resolve()
            require(resolved.is_relative_to(root), f'{context}: target escapes repository')
            require(resolved.exists(), f'{context}: missing local target')
        except (ValueError, OSError, RuntimeError) as error:
            require(False, f'{context}: invalid local reference ({error})')


def skill_text_files(root=ROOT):
    """Yield (relative path, text) for every UTF-8 file inside an se-* skill folder."""
    for folder in sorted(root.glob('se-*')):
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob('*')):
            if not path.is_file() or path.name == '.DS_Store' or 'node_modules' in path.parts:
                continue
            try:
                text = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            yield path.relative_to(root).as_posix(), text


def validate_frontmatter(root=ROOT, expected=EXPECTED):
    actual = {path.parent.name for path in root.glob('*/SKILL.md')}
    require(actual == expected, f'expected {len(expected)} skills, found {sorted(actual)}')
    for name in sorted(expected):
        text = (root / name / 'SKILL.md').read_text(encoding='utf-8')
        frontmatter = text.split('---', 2)
        require(text.startswith('---\n') and len(frontmatter) == 3, f'{name}: frontmatter')
        require(re.search(rf'^name: {re.escape(name)}$', frontmatter[1], re.M), f'{name}: name')
        description = re.search(r'^description: (\S.+)$', frontmatter[1], re.M)
        require(description, f'{name}: description')
        value = description.group(1).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
            value = value[1:-1]
        require(len(value) <= DESCRIPTION_LIMIT,
                f'{name}: description is {len(value)} characters; limit {DESCRIPTION_LIMIT}')
        require(not re.search(r'^disable-model-invocation:', frontmatter[1], re.M),
                f'{name}: typed-only flag; every skill must be selectable automatically')
        require((root / name / 'agents/openai.yaml').is_file(), f'{name}: UI metadata')
        display = re.search(r'^\s*display_name:\s*"([^"]+)"',
                            (root / name / 'agents/openai.yaml').read_text(encoding='utf-8'), re.M)
        require(display, f'{name}: UI display name')
        title = re.search(r'^# (.+)$', frontmatter[2], re.M)
        heading = title.group(1).strip() if title else 'missing'
        require(heading == display.group(1),
                f'{name}: title "{heading}" differs from its display name "{display.group(1)}"')


BASELINE_SKILLS = frozenset({
    'se-blueprint', 'se-ci', 'se-comments', 'se-contest', 'se-design', 'se-formal', 'se-formal-sync',
    'se-guardrail', 'se-harness', 'se-harness-sync', 'se-playbook', 'se-retro', 'se-setup', 'se-style',
    'se-test-first', 'se-typescript'})


def validate_baseline(root=ROOT, skills=BASELINE_SKILLS):
    """Skills that change code load se-zero-trust and se-verify by name (spec 001 AC-12.1, AC-12.2)."""
    for name in sorted(skills):
        text = (root / name / 'SKILL.md').read_text(encoding='utf-8')
        section = re.search(r'^## SE change baseline\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        require(section, f'{name}: no SE change baseline section')
        for skill in ('se-zero-trust', 'se-verify'):
            require(re.search(rf'\b[Ll]oad \*\*{skill}\*\*', section.group(1)),
                    f'{name}: the SE change baseline must load **{skill}** by name')


TESTED_INSTRUCTION = 'validation/pstack-selection/load-skill-instruction.md'


def validate_recommended_instruction(root=ROOT):
    """The README recommends exactly the project instruction the selection evaluation tested."""
    tested = (root / TESTED_INSTRUCTION).read_text(encoding='utf-8')
    readme = (root / 'README.md').read_text(encoding='utf-8')
    require(f'```text\n{tested}```' in readme,
            f'README.md: the recommended project instruction differs from {TESTED_INSTRUCTION}')


def validate_skill_references(root=ROOT, expected=EXPECTED):
    """Every skill-shaped reference inside a skill folder names a package skill."""
    for name, text in skill_text_files(root):
        if not name.endswith('.md'):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for pattern in (SKILL_COMMAND, SKILL_TOKEN):
                for match in pattern.finditer(line):
                    require(match.group(1) in expected,
                            f'{name}:{line_no}: reference to unknown skill {match.group(1)!r}')


def validate_residue(root=ROOT):
    """No pstack naming, old pstack skill names or Cursor-only features in skill folders."""
    for name, text in skill_text_files(root):
        patterns = [BRAND_RESIDUE]
        if name.endswith('.md'):
            patterns += [OLD_NAME_RESIDUE, HOST_RESIDUE]
        for line_no, line in enumerate(text.splitlines(), 1):
            for pattern in patterns:
                match = pattern.search(line)
                require(match is None,
                        f'{name}:{line_no}: pstack or host-specific residue {match and match.group(0)!r}')


def validate_notice(root=ROOT):
    path = root / NOTICE
    require(path.is_file(), f'{NOTICE}: missing attribution for ported pstack material')
    text = path.read_text(encoding='utf-8')
    for needed in ('MIT License', 'Copyright (c) 2026 Lauren Tan', PSTACK_COMMIT):
        require(needed in text, f'{NOTICE}: missing {needed!r}')


def skill_node(name):
    """Graph node for a file inside the package: a skill, or one principle reference."""
    parts = name.split('/')
    if parts[0] == 'se-principles' and len(parts) == 3 and parts[1] == 'references':
        return f'se-principles#{parts[2].removesuffix(".md")}'
    return parts[0]


def skill_edges(root=ROOT, expected=EXPECTED):
    """(from, to) references between package skills and principle references."""
    edges = set()
    for name, text in skill_text_files(root):
        if not name.endswith('.md'):
            continue
        origin = skill_node(name)
        targets = {m.group(1) for p in (SKILL_COMMAND, SKILL_TOKEN) for m in p.finditer(text)}
        targets &= expected
        for target in MARKDOWN_LINK.findall(text):
            url = urlsplit(target.strip())
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(name), unquote(url.path)))
            if not resolved.startswith('..') and resolved.split('/', 1)[0] in expected:
                targets.add(skill_node(resolved.replace(os.sep, '/')))
        edges.update((origin, target) for target in targets if target != origin)
    return edges


def main():
    validate_frontmatter()

    files = dict(package_files())
    manifest = {}
    for line in (ROOT / 'MANIFEST.sha256').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(name not in manifest and re.fullmatch(r'[0-9a-f]{64}', digest), 'invalid manifest entry')
        manifest[name] = digest
    require(files.keys() == manifest.keys(), 'manifest file inventory differs from package')
    for name, path in files.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == manifest[name], f'digest mismatch: {name}')
        if path.suffix == '.md':
            validate_markdown_links(path)
    validate_html_links()
    validate_skill_references()
    validate_residue()
    validate_notice()
    validate_baseline()
    validate_recommended_instruction()
    print(f'PASS: {len(EXPECTED)} skill packages, required fields, local Markdown/HTML links, '
          'skill references, no pstack or host-specific residue, attribution, change baseline, recommended '
          'instruction, complete hash manifest')

    fixture = ROOT / 'validation/code-baseline'
    for name, project_count, independent_count in (('new', 10, 7), ('update', 8, 8)):
        result, output = run(['-m', 'unittest', 'discover', '-s', 'tests', '-v'], fixture / name)
        require_tests(result, output, project_count, f'{name} project checks')
        print(f'PASS: {name} project checks')
        result, output = run([str(fixture / 'grade_fixture.py'), name, str(fixture / name)])
        require_tests(result, output, independent_count, f'{name} independent checks')
        print(f'PASS: {name} independent checks')
    result, output = run([str(fixture / 'grade_fixture.py'), 'update', str(fixture / 'original-update')])
    require(result.returncode == 1 and
            'FAIL: test_spoofed_tenant_hint_denied' in output and
            'AssertionError: PermissionError not raised' in output,
            f'negative control did not detect tenant bypass\n{output}')
    print('PASS: original defective implementation rejected for tenant bypass')

    expansion = ROOT / 'validation/expansion'
    result, output = run([str(expansion / 'proof/check_archive.py')])
    require(result.returncode == 1, f'proof exercise must retain observed defects\n{output}')
    observations = json.loads(output)
    bypass = next(case for case in observations['cases']
                  if case['case'] == 'admin cross tenant with target hint')
    require(observations['passed'] == 6 and observations['total'] == 10 and
            not bypass['contract_pass'] and bypass['changed_accounts'] == ['E'] and
            bypass['events_changed'], 'proof exercise did not reproduce unauthorized effects')
    print('PASS: proof exercise reproduces tenant bypass despite original green suite')

    result, output = run(['-m', 'unittest', 'discover', '-s', 'tests', '-v'], expansion / 'swarm/project')
    require_tests(result, output, 10, 'swarm integrated project checks')
    result, output = run([str(fixture / 'grade_fixture.py'), 'update', str(expansion / 'swarm/project')])
    require_tests(result, output, 8, 'swarm independent checks')
    print('PASS: swarm project and independent checks')

    result, output = run([str(ROOT / 'validation/ci-fixture/grade_ci.py'), 'self-test'])
    require(result.returncode == 0 and 'Ran 7 checks: 7 passed, 0 failed' in output,
            f'CI fixture grader self-test failed\n{output}')
    print('PASS: CI fixture grader rejects the untouched fixture and accepts the reference answer')


if __name__ == '__main__':
    main()
