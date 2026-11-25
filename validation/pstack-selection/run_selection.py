"""Automatic-selection evaluation for the SE family (spec 001 FR-13); Python >= 3.10.

    python3 -B run_selection.py --out <dir> [--agent codex|claude] [--skills global|project]
        [--ids how-1,why-2] [--model <name>] [--instructions <file>]

Each prompt in prompts.json runs in a fresh headless session (`codex exec --ephemeral`, or
`claude -p`, with the user settings source when the skills are global), in its own copy
of the CI fixture project. `--instructions` writes a file into each copy as the project's
instruction file (`CLAUDE.md` or `AGENTS.md`), to test project-level routing guidance. With `--skills global` (the default) the session uses the SE package
installed in the host's user skill folder; with `--skills project` the package is copied into the
workspace as project skills. No prompt names a skill. A prompt passes when the session reads the SKILL.md of one of its expected skills.
Results go to <out>/results.json; transcripts to <out>/<id>.jsonl.

Run it where the host sees only the SE package: user-level copies of older SE skills or of the
original pstack skills, and global routing instructions, change what this measures. Record the
environment with the results.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FIXTURE = REPO / 'validation/ci-fixture/project'
SKILL_READ = re.compile(r'([\w.-]+)/SKILL\.md')
INSTRUCTION_FILES = {'claude': 'CLAUDE.md', 'codex': 'AGENTS.md'}


# A headless `claude` started from inside a Claude Code session inherits that session's variables
# (CLAUDE_CODE_SIMPLE, ANTHROPIC_BASE_URL and host-auth flags), which switch it to bare mode or route it
# through the host. Start it with only the basics, so it uses the CLI's own login and normal discovery.
CLEAN_ENV_KEYS = ('HOME', 'PATH', 'USER', 'LOGNAME', 'SHELL', 'LANG', 'TERM', 'TMPDIR')
UNATTENDED = ('This is an unattended evaluation run in a disposable copy of a fixture project. '
              'Nobody can answer questions or approve a plan during this run.')


def clean_env():
    import os
    env = {key: os.environ[key] for key in CLEAN_ENV_KEYS if key in os.environ}
    env.setdefault('LANG', 'en_US.UTF-8')
    return env


def workspace(base, item, project_skills, instructions=None, agent='codex'):
    project = base / item['id']
    shutil.copytree(FIXTURE, project)
    if instructions:
        (project / INSTRUCTION_FILES[agent]).write_text(instructions)
    if project_skills:
        skills = project / '.agents/skills'
        skills.mkdir(parents=True)
        for folder in sorted(REPO.glob('se-*')):
            if (folder / 'SKILL.md').is_file():
                shutil.copytree(folder, skills / folder.name)
    subprocess.run(['git', 'init', '-q', '-b', 'main'], cwd=project, check=True)
    (project / '.git/info/exclude').write_text('.agents/\n')
    subprocess.run(['git', 'add', '-A'], cwd=project, check=True)
    subprocess.run(['git', '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid',
                    'commit', '-q', '-m', 'Initial import'], cwd=project, check=True)
    return project


def skills_read(stdout):
    """Skill names the session loaded, in order: SKILL.md reads and Skill tool calls."""
    read = []

    def add(names):
        for name in names:
            if name not in read:
                read.append(name)

    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get('item') or {}
        if item.get('type') == 'command_execution':  # Codex
            add(SKILL_READ.findall(str(item.get('command', ''))))
        message = event.get('message') if event.get('type') == 'assistant' else None
        for block in (message or {}).get('content', []) if isinstance(message, dict) else []:
            if block.get('type') != 'tool_use':  # Claude Code
                continue
            data = block.get('input') or {}
            if block.get('name') == 'Skill' and data.get('skill'):
                add([str(data['skill']).split(':')[-1]])
            add(SKILL_READ.findall(str(data.get('file_path', '')) + ' ' + str(data.get('command', ''))))
    return read


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--agent', choices=('codex', 'claude'), default='codex')
    parser.add_argument('--skills', choices=('global', 'project'), default='global')
    parser.add_argument('--ids')
    parser.add_argument('--model')
    parser.add_argument('--instructions', type=Path,
                        help='file written into each workspace as CLAUDE.md (claude) or AGENTS.md (codex)')
    args = parser.parse_args(argv)
    instructions = args.instructions.read_text() if args.instructions else None
    prompts = json.loads((HERE / 'prompts.json').read_text())
    if args.ids:
        wanted = set(args.ids.split(','))
        prompts = [item for item in prompts if item['id'] in wanted]
    args.out.mkdir(parents=True, exist_ok=True)
    results = []
    for item in prompts:
        project = workspace(args.out / 'work', item, args.skills == 'project', instructions, args.agent)
        if args.agent == 'codex':
            command = ['codex', 'exec', '--ephemeral', '--json', '--sandbox',
                       'workspace-write' if item['write'] else 'read-only', '-C', str(project), item['prompt']]
            if args.model:
                command[2:2] = ['-m', args.model]
        else:
            tools = 'Read Glob Grep Skill Agent Bash(python3:*) Bash(git:*) Bash(ls:*) Bash(cat:*)'
            command = ['claude', '-p', item['prompt'], '--output-format', 'stream-json', '--verbose',
                       # User-level skills load only with the `user` source, which also brings user settings.
                       '--setting-sources', 'user,project,local' if args.skills == 'global' else 'project,local',
                       '--append-system-prompt', UNATTENDED,
                       '--allowedTools', *tools.split()]
            if item['write']:
                command += ['--permission-mode', 'acceptEdits']
            if args.model:
                command += ['--model', args.model]
        env = clean_env() if args.agent == 'claude' else None
        result = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=1800, env=env)
        (args.out / f'{item["id"]}.jsonl').write_text(result.stdout)
        read = skills_read(result.stdout)
        passed = any(name in read for name in item['expect'])
        results.append({'id': item['id'], 'area': item['area'], 'expect': item['expect'], 'read': read,
                        'pass': passed, 'exit': result.returncode,
                        'instructions': args.instructions.name if args.instructions else None})
        print(json.dumps(results[-1]))
    (args.out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    passed = sum(item['pass'] for item in results)
    print(f'{passed}/{len(results)} prompts read an expected skill')
    return 0 if passed == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
