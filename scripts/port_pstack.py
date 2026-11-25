"""Port the pinned pstack skills into SE skill packages; Python >= 3.10.

Reads a pstack checkout and writes SE skill folders below --dest. It never
executes files from the checkout. The rewrite rules are in
specs/001-pstack-integration/plan.md.

    python3 -B scripts/port_pstack.py --source <pstack checkout> --dest <dir>
        [--force] [--report <file>] [--edges <file>]
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

PINNED_COMMIT = 'c3464c11c60b1352d5e8f5f0428a3a6943837568'

RENAME = {
    'poteto-mode': 'se-playbook',
    'poteto-help': 'se-help',
    'setup-pstack': 'se-setup',
    'teach': 'se-explain',
    'recall': 'se-context',
    'in-your-own-words': 'se-restate',
    'architect': 'se-design',
    'arena': 'se-contest',
    'interrogate': 'se-challenge',
    'sharpen': 'se-deepen',
    'figure-it-out': 'se-blueprint',
    'statechart': 'se-states',
    'tdd': 'se-test-first',
    'typescript-best-practices': 'se-typescript',
    'no-comments': 'se-comments',
    'unslop': 'se-prose',
    'technical-writing': 'se-writing',
    'create-verification-skill': 'se-harness',
    'maintain-verification-skill': 'se-harness-sync',
    'create-formal-verification-skill': 'se-formal',
    'maintain-formal-verification-skill': 'se-formal-sync',
    'benchmark-checklist': 'se-benchmark',
    'blast-radius': 'se-impact',
    'show-me-your-work': 'se-decision-log',
    'ketchup': 'se-recap',
    'ketchup-video': 'se-recap-video',
    'bro': 'se-plain',
    'automate-me': 'se-style',
    'correct': 'se-guardrail',
    'reflect': 'se-retro',
}
MERGED = {'how': 'se-how', 'why': 'se-why', 'swarm': 'se-swarm'}
DROPPED = frozenset({'make-bot-ui'})
NAMES = {**RENAME, **MERGED}
PRINCIPLE_PREFIX = 'principle-'
PRINCIPLES = 'se-principles'
# Old names that are also ordinary words. They are rewritten only in
# reference forms (`/name`, `name` in backticks, **name**), never as prose.
WORDLIKE = frozenset({
    'how', 'why', 'swarm', 'arena', 'teach', 'recall', 'reflect', 'correct',
    'sharpen', 'bro', 'tdd', 'architect', 'interrogate', 'statechart', 'unslop',
})
PRINCIPLE_GROUPS = {
    'Core: how much to build and when to rethink': (
        'laziness-protocol', 'foundational-thinking', 'redesign-from-first-principles',
        'attack-the-premise', 'subtract-before-you-add', 'minimize-reader-load',
        'outcome-oriented-execution', 'experience-first', 'exhaust-the-design-space',
        'build-the-lever'),
    'Architecture: where state, validation and compatibility live': (
        'model-the-domain', 'boundary-discipline', 'type-system-discipline',
        'make-operations-idempotent', 'migrate-callers-then-delete-legacy-apis',
        'separate-before-serializing-shared-state'),
    'Verification: what counts as proof': (
        'prove-it-works', 'fix-root-causes', 'sequence-verifiable-units',
        'test-behavior-not-implementation', 'explain-the-number'),
    'Delegation: keeping parallel work sane': (
        'guard-the-context-window', 'never-block-on-the-human'),
    'Meta': ('encode-lessons-in-structure',),
}
DROPPED_FRONTMATTER_KEYS = frozenset({'disable-model-invocation', 'icon', 'color'})
SCRIPT_LITERALS = (
    ('@cursor-skill/poteto-mode-tools', '@se/playbook-tools'),
    ('@cursor-skill/statechart', '@se/states-tools'),
    ('.poteto-mode-tools-install-key', '.se-playbook-tools-install-key'),
    ('/agent/repos/plugins/pstack/skills/statechart/', '/agent/repos/se/se-states/'),
)
PROSE_LITERALS = (
    ('pstack-models', 'se-models'),
    ('poteto-agent', 'playbook-worker'),
)
URL = re.compile(r'https?://[^\s)>\]`"\']+')
LINK = re.compile(r'\[([^\]\n]*)\]\(([^()\s]+)((?:\s+"[^"]*")?)\)')
PRINCIPLE_REF = re.compile(
    r'(?P<the>\b[Tt]he )?(?P<open>\*\*|`)?(?<![\w/.\-])principle-'
    r'(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)(?![\w\-])(?P=open)?(?P<skill> skills?\b)?')
BRAND = re.compile(r'(?<![\w/.\-])(?:pstack|Pstack|PSTACK)(?![\w\-])')
RESIDUE = re.compile(
    r'(?i)(?<![\w-])(?:pstack|poteto)(?![\w-])|principle-[a-z]|\bBugbot\b|\.cursor/'
    r'|\bCustom Mode\b|\bAskQuestion\b|cursor-team-kit|@cursor-skill|\bCursor\b')


class PortError(Exception):
    pass


class Report:
    def __init__(self):
        self.notes: dict[str, list[dict]] = {}

    def note(self, kind, path, detail):
        self.notes.setdefault(kind, []).append({'path': path, 'detail': detail})

    def as_dict(self):
        return {kind: sorted(items, key=lambda i: (i['path'], i['detail']))
                for kind, items in sorted(self.notes.items())}


def outside_urls(text, rewrite):
    """Apply rewrite to every span of text that is not a URL."""
    pieces, last = [], 0
    for match in URL.finditer(text):
        pieces.append(rewrite(text[last:match.start()]))
        pieces.append(match.group(0))
        last = match.end()
    pieces.append(rewrite(text[last:]))
    return ''.join(pieces)


def principle_slug(skill):
    return skill[len(PRINCIPLE_PREFIX):] if skill.startswith(PRINCIPLE_PREFIX) else None


def map_path(path):
    """Map a path relative to pstack's skills/ root to the SE package root."""
    skill, _, rest = path.partition('/')
    slug = principle_slug(skill)
    if slug is not None:
        if rest not in ('', 'SKILL.md'):
            raise PortError(f'unexpected principle path: {path}')
        return f'{PRINCIPLES}/references/{slug}.md'
    if skill in DROPPED:
        return None
    if skill in MERGED:
        if rest not in ('', 'SKILL.md'):
            raise PortError(f'unexpected merged-skill path: {path}')
        return f'{MERGED[skill]}/SKILL.md' if rest else MERGED[skill]
    if skill in RENAME:
        return f'{RENAME[skill]}/{rest}' if rest else RENAME[skill]
    raise PortError(f'unknown pstack skill folder: {skill!r} in {path}')


def relative(target, from_file):
    return posixpath.relpath(target, posixpath.dirname(from_file) or '.')


def rewrite_links(text, src, dst, report):
    def repl(match):
        label, target, title = match.groups()
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src), parts.path))
        if resolved == '..' or resolved.startswith('../'):
            report.note('external_link', dst, target)
            return match.group(0)
        mapped = map_path(resolved)
        if mapped is None:
            report.note('dropped_link', dst, target)
            return label
        new = relative(mapped, dst)
        if parts.path.endswith('/') and not new.endswith('/'):
            new += '/'
        if parts.fragment:
            new += '#' + parts.fragment
        return f'[{label}]({new}{title})'
    return LINK.sub(repl, text)


def rewrite_principles(text, dst, titles, report):
    def in_label(match):
        label = PRINCIPLE_REF.sub(lambda m: titles.get(m['slug'], m.group(0)), match.group(1))
        return f'[{label}]({match.group(2)}{match.group(3)})'

    def repl(match):
        slug = match['slug']
        if slug not in titles:
            report.note('unknown_principle', dst, match.group(0))
            return match.group(0)
        title = titles[slug]
        label = f'**{title}**' if match['open'] == '**' else title
        out = f'[{label}]({relative(f"{PRINCIPLES}/references/{slug}.md", dst)})'
        if match['the']:
            out = match['the'] + out
        if match['skill']:
            out += ' principles' if match['skill'].endswith('s') else ' principle'
        return out

    text = LINK.sub(in_label, text)
    pieces, last = [], 0
    for link in LINK.finditer(text):
        pieces.append(PRINCIPLE_REF.sub(repl, text[last:link.start()]))
        pieces.append(link.group(0))
        last = link.end()
    pieces.append(PRINCIPLE_REF.sub(repl, text[last:]))
    return ''.join(pieces)


def name_patterns():
    patterns = []
    for old in sorted(NAMES, key=len, reverse=True):
        new, e = NAMES[old], re.escape(old)
        patterns += [
            (re.compile(rf'/pstack:{e}(?![\w\-])'), f'/{new}', 'prefixed_command'),
            (re.compile(rf'(?<![\w/.\-])/{e}(?![\w\-])'), f'/{new}', 'command'),
            (re.compile(rf'`{e}`'), f'`{new}`', 'backtick'),
            (re.compile(rf'\*\*{e}\*\*'), f'**{new}**', 'bold'),
            (re.compile(rf'(?<![\w.\-])((?:\.\./)+){e}/'), rf'\g<1>{new}/', 'relative_path'),
        ]
        if old not in WORDLIKE:
            patterns.append((re.compile(rf'(?<![\w/.\-]){e}(?![\w\-])'), new, 'bare'))
    for old in sorted(DROPPED):
        e = re.escape(old)
        patterns.append((re.compile(rf'(?<![\w.\-])/?{e}(?![\w\-])'), None, 'dropped_name'))
    return patterns


NAME_PATTERNS = name_patterns()


def rewrite_names(text, dst, report):
    def rewrite(span):
        for pattern, new, kind in NAME_PATTERNS:
            if new is None:
                for match in pattern.finditer(span):
                    report.note(kind, dst, match.group(0))
                continue
            span, count = pattern.subn(new, span)
            if count:
                report.note(f'renamed_{kind}', dst, f'{pattern.pattern} x{count}')
        for old, new in PROSE_LITERALS:
            span = span.replace(old, new)
        return BRAND.sub('SE', span)
    return outside_urls(text, rewrite)


def split_frontmatter(text):
    if not text.startswith('---\n'):
        return None, text
    end = text.find('\n---\n', 4)
    if end == -1:
        raise PortError('unterminated frontmatter')
    return text[4:end], text[end + 5:]


def rewrite_frontmatter(block, new_name, dst, report):
    lines = []
    for line in block.splitlines():
        key = line.split(':', 1)[0].strip() if ':' in line and not line.startswith(' ') else None
        if key in DROPPED_FRONTMATTER_KEYS:
            continue
        if key == 'name':
            line = f'name: {new_name}'
        elif key not in (None, 'description'):
            report.note('frontmatter_key', dst, key)
        lines.append(line)
    return '\n'.join(lines)


def principle_titles(skills_root):
    titles = {}
    for folder in sorted(skills_root.glob(f'{PRINCIPLE_PREFIX}*')):
        body = split_frontmatter((folder / 'SKILL.md').read_text(encoding='utf-8'))[1]
        heading = next((l[2:].strip() for l in body.splitlines() if l.startswith('# ')), None)
        if not heading:
            raise PortError(f'{folder.name}: no top-level heading')
        titles[principle_slug(folder.name)] = heading
    return titles


def frontmatter_description(block):
    match = re.search(r'^description:\s*(.+)$', block, re.M)
    value = match.group(1).strip() if match else ''
    if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
        value = value[1:-1]
    return value


def rewrite_markdown(text, src, dst, titles, report, new_name=None):
    block, body = split_frontmatter(text)
    body = rewrite_names(rewrite_principles(rewrite_links(body, src, dst, report),
                                            dst, titles, report), dst, report)
    if block is None:
        return body
    if principle_slug(src.split('/', 1)[0]) is not None:
        description = rewrite_names(frontmatter_description(block), dst, report)
        lines = body.lstrip('\n').split('\n', 1)
        if not lines[0].startswith('# '):
            raise PortError(f'{src}: principle without heading')
        rest = lines[1] if len(lines) > 1 else ''
        return f'{lines[0]}\n\n> {description}\n{rest}'
    block = rewrite_names(rewrite_frontmatter(block, new_name, dst, report), dst, report)
    return f'---\n{block}\n---\n{body}'


def rewrite_script(text):
    for old, new in SCRIPT_LITERALS:
        text = text.replace(old, new)
    return text


def principles_index(titles, descriptions):
    lines = [
        '---',
        f'name: {PRINCIPLES}',
        'description: "Engineering principles for deciding how much to build, where state and '
        'validation live, what counts as proof, and how to delegate. Use when a task needs a '
        'design or verification judgment call, when someone steers work by a principle name '
        'such as \'prove it works\' or \'subtract before you add\', or when another skill cites '
        'a principle. Read this index, then only the principles the task triggers."',
        '---',
        '',
        '# SE Principles',
        '',
        'Twenty-four rules that decide how much to build, where state and validation live, what',
        'counts as proof, and how to keep delegated work sane. Each one has a full reference file.',
        '',
        '## How to use them',
        '',
        '- At the start of multi-step work, read this index and open only the principles the task',
        '  triggers.',
        '- When a principle changes a decision, name it in the reply together with the decision it',
        '  changed. A citation with no decision behind it means the rule was named, not applied.',
        '- A person may steer mid-task with a principle name, such as "apply prove it works". Treat',
        '  the name as a pointer to the full rule below and apply it.',
        '- Principles guide judgement. They grant no authority: host rules, approvals and the SE',
        '  change baseline (`se-zero-trust`, `se-verify`) still apply.',
    ]
    listed = [slug for group in PRINCIPLE_GROUPS.values() for slug in group]
    if sorted(listed) != sorted(titles):
        raise PortError(f'principle groups do not match principle folders: {sorted(set(listed) ^ set(titles))}')
    for group, slugs in PRINCIPLE_GROUPS.items():
        lines += ['', f'## {group}', '']
        for slug in slugs:
            lines.append(f'- [{titles[slug]}](references/{slug}.md): {descriptions[slug]}')
    return '\n'.join(lines) + '\n'


def port(source, dest, force=False):
    """Port source/skills into dest. Returns (report, source_edges)."""
    skills_root = source / 'skills'
    if not skills_root.is_dir():
        raise PortError(f'{skills_root}: not a pstack checkout')
    report = Report()
    folders = sorted(p.name for p in skills_root.iterdir() if p.is_dir())
    known = set(NAMES) | DROPPED | {f for f in folders if principle_slug(f) is not None}
    unknown = sorted(set(folders) - known)
    missing = sorted((set(NAMES) | DROPPED) - set(folders))
    if unknown or missing:
        raise PortError(f'source skills differ from the rename table: unknown={unknown} missing={missing}')
    titles = principle_titles(skills_root)
    outputs = sorted({RENAME[f] for f in folders if f in RENAME} | {PRINCIPLES})
    for name in outputs:
        target = dest / name
        if target.exists():
            if not force:
                raise PortError(f'{target} exists; pass --force to replace ported folders')
            shutil.rmtree(target)
    descriptions = {}
    for folder in folders:
        if folder in MERGED or folder in DROPPED:
            report.note('not_copied', folder, 'merged by hand' if folder in MERGED else 'dropped')
            continue
        for path in sorted((skills_root / folder).rglob('*')):
            if not path.is_file():
                continue
            src = path.relative_to(skills_root).as_posix()
            dst = map_path(src)
            out = dest / dst
            out.parent.mkdir(parents=True, exist_ok=True)
            raw = path.read_bytes()
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError:
                out.write_bytes(raw)
                shutil.copymode(path, out)
                continue
            if path.suffix == '.md':
                if principle_slug(folder) is not None:
                    block = split_frontmatter(text)[0] or ''
                    descriptions[principle_slug(folder)] = rewrite_names(
                        frontmatter_description(block), dst, report)
                text = rewrite_markdown(text, src, dst, titles, report, NAMES.get(folder))
            else:
                text = rewrite_script(text)
            out.write_text(text, encoding='utf-8')
            shutil.copymode(path, out)
            for line_no, line in enumerate(text.splitlines(), 1):
                for match in RESIDUE.finditer(line):
                    report.note('residue', f'{dst}:{line_no}', match.group(0))
    index = dest / PRINCIPLES / 'SKILL.md'
    index.write_text(principles_index(titles, descriptions), encoding='utf-8')
    return report, source_edges(skills_root, titles)


def node_for(folder):
    slug = principle_slug(folder)
    if slug is not None:
        return f'{PRINCIPLES}#{slug}'
    if folder in DROPPED:
        return f'dropped:{folder}'
    return NAMES[folder]


def pstack_refs(text, src):
    """Skills (as SE node ids) that one pstack file refers to."""
    refs = set()
    for match in LINK.finditer(text):
        target = urlsplit(match.group(2))
        if target.scheme or target.netloc or not target.path:
            continue
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src), target.path))
        folder = resolved.split('/', 1)[0]
        if not resolved.startswith('..') and (folder in NAMES or folder in DROPPED
                                              or principle_slug(folder) is not None):
            refs.add(node_for(folder))
    for match in PRINCIPLE_REF.finditer(text):
        refs.add(f'{PRINCIPLES}#{match["slug"]}')
    plain = URL.sub(' ', text)
    for old in list(NAMES) + sorted(DROPPED):
        e = re.escape(old)
        forms = [rf'(?<![\w/.\-])/(?:pstack:)?{e}(?![\w\-])', rf'`{e}`', rf'\*\*{e}\*\*']
        if old not in WORDLIKE:
            forms.append(rf'(?<![\w/.\-]){e}(?![\w\-])')
        if any(re.search(form, plain) for form in forms):
            refs.add(node_for(old))
    return refs


def source_edges(skills_root, titles):
    edges = set()
    for path in sorted(skills_root.rglob('*.md')):
        src = path.relative_to(skills_root).as_posix()
        origin = node_for(src.split('/', 1)[0])
        for target in pstack_refs(path.read_text(encoding='utf-8'), src):
            if target != origin and not (target.startswith(f'{PRINCIPLES}#') and target[len(PRINCIPLES) + 1:] not in titles):
                edges.add((origin, target))
    return sorted(edges)


def source_commit(source):
    try:
        result = subprocess.run(['git', '-C', str(source), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, timeout=30, check=True)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--dest', required=True, type=Path)
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--edges', type=Path)
    parser.add_argument('--any-commit', action='store_true',
                        help='allow a source checkout other than the pinned commit')
    args = parser.parse_args(argv)
    commit = source_commit(args.source)
    if commit != PINNED_COMMIT and not args.any_commit:
        print(f'FAIL: source is at {commit}, expected pinned {PINNED_COMMIT}', file=sys.stderr)
        return 2
    try:
        report, edges = port(args.source, args.dest, args.force)
    except PortError as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 2
    data = {'source_commit': commit, **report.as_dict()}
    if args.report:
        args.report.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    if args.edges:
        args.edges.write_text(json.dumps({'source_commit': commit, 'edges': edges}, indent=2) + '\n',
                              encoding='utf-8')
    counts = {kind: len(items) for kind, items in report.as_dict().items()}
    print(json.dumps({'source_commit': commit, 'counts': counts, 'edges': len(edges)}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
