"""Run se-ci on the CI fixture with a headless agent and grade each run; Python >= 3.10.

    python3 -B run_eval.py --agent claude|codex --out <dir> [--runs 1,2,3] [--model <name>]

Writes the working project, each run's transcript and reply, and the grader output under
<out>/<agent>/. The project copy never contains this folder's README, grader or reference answer.
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
GRADER = HERE / 'grade_ci.py'
SKILL_DIRS = {'claude': '.claude/skills', 'codex': '.agents/skills'}
PROMPTS = {
    1: ('Use the se-ci skill ({skill}) to optimise this project\'s CI. This is its first run here. '
        'The project has no remote: its CI run history, pull requests and issues are exported under .ci-history/. '
        'Work without asking me questions, and record anything that needs my approval in CI.md. '
        'When you finish, summarise what you changed.'),
    2: ('A new commit changed app/billing (see git log). Run the se-ci skill ({skill}) again for this change: '
        'update the CI record and tell me which tests CI should run for this commit. Work without asking me questions. '
        'End your reply with exactly one line of the form `TESTS: <comma-separated test modules such as tests.billing, or ALL>`.'),
    3: ('A new commit changed app/config.py. Using the se-ci skill ({skill}), which tests should CI run for this commit? '
        'Update the CI record if needed. Work without asking me questions. '
        'End your reply with exactly one line of the form `TESTS: <comma-separated test modules such as tests.billing, or ALL>`.'),
}
CHANGES = {
    2: ('app/billing/invoice.py', '\n\ndef volume_discount(lines, threshold=10, rate=0.05):\n'
        '    """Discount for orders of at least `threshold` units."""\n'
        '    units = sum(quantity for quantity, _ in lines)\n'
        '    return rate if units >= threshold else 0.0\n', 'Add volume discount helper'),
    3: ('app/config.py', '\nDEFAULT_LOCALE = "en-SG"\n', 'Add default locale setting'),
}
CLAUDE_TOOLS = ('Read Write Edit Glob Grep Skill Agent Task TodoWrite '
                'Bash(python3:*) Bash(python:*) Bash(git:*) Bash(ls:*) Bash(cat:*) Bash(wc:*) Bash(head:*) '
                'Bash(tail:*) Bash(find:*) Bash(grep:*) Bash(actionlint:*) Bash(mkdir:*) Bash(sort:*) Bash(jq:*)')


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


def git(project, *args):
    return subprocess.run(['git', '-C', str(project), '-c', 'user.name=fixture',
                           '-c', 'user.email=fixture@example.invalid', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def prepare(project, agent):
    shutil.copytree(HERE / 'project', project)
    skills = project / SKILL_DIRS[agent]
    skills.mkdir(parents=True)
    for folder in sorted(REPO.glob('se-*')):
        if (folder / 'SKILL.md').is_file():
            shutil.copytree(folder, skills / folder.name)
    git(project, 'init', '-q', '-b', 'main')
    (project / '.git/info/exclude').write_text('.claude/\n.agents/\n')
    git(project, 'add', '-A')
    git(project, 'commit', '-q', '-m', 'Initial import')


def run_agent(agent, project, prompt, transcript, model):
    env = None
    if agent == 'claude':
        command = ['claude', '-p', prompt, '--output-format', 'json', '--permission-mode', 'acceptEdits',
                   '--setting-sources', 'project,local', '--append-system-prompt',
                   UNATTENDED + ' Do the requested work directly in this copy, and record anything that '
                   'needs approval in CI.md, as the task asks.',
                   '--allowedTools', *CLAUDE_TOOLS.split()]
        if model:
            command += ['--model', model]
        env = clean_env()
    else:
        command = ['codex', 'exec', '--ephemeral', '--json', '--sandbox', 'workspace-write',
                   '-C', str(project), prompt]
        if model:
            command[2:2] = ['-m', model]
    started = time.monotonic()
    result = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=3600, env=env)
    elapsed = round(time.monotonic() - started, 1)
    transcript.write_text(result.stdout + ('\n--- stderr ---\n' + result.stderr if result.stderr else ''))
    return result, elapsed


def reply_text(agent, stdout):
    if agent == 'claude':
        try:
            return json.loads(stdout).get('result', '')
        except json.JSONDecodeError:
            return stdout
    messages = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get('item') or event.get('msg') or {}
        if item.get('type') in ('agent_message', 'assistant_message') and item.get('text'):
            messages.append(item['text'])
    return messages[-1] if messages else ''


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--agent', choices=sorted(SKILL_DIRS), required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--runs', default='1,2,3')
    parser.add_argument('--model')
    args = parser.parse_args(argv)
    base = args.out / args.agent
    project = base / 'project'
    if base.exists():
        print(f'FAIL: {base} exists; choose a fresh --out', file=sys.stderr)
        return 2
    base.mkdir(parents=True)
    prepare(project, args.agent)
    skill = f'{SKILL_DIRS[args.agent]}/se-ci/SKILL.md'
    summary = []
    for run in (int(item) for item in args.runs.split(',')):
        if run in CHANGES:
            git(project, 'add', '-A')
            if git(project, 'status', '--porcelain'):
                git(project, 'commit', '-q', '-m', f'se-ci run {run - 1} output')
            path, addition, message = CHANGES[run]
            with open(project / path, 'a', encoding='utf-8') as handle:
                handle.write(addition)
            git(project, 'add', path)
            git(project, 'commit', '-q', '-m', message)
        prompt = PROMPTS[run].format(skill=skill)
        result, elapsed = run_agent(args.agent, project, prompt, base / f'run{run}-transcript.jsonl', args.model)
        reply = reply_text(args.agent, result.stdout)
        (base / f'run{run}-reply.txt').write_text(reply)
        grade = subprocess.run([sys.executable, '-B', str(GRADER), f'run{run}', str(project),
                                '--original', str(HERE / 'project'), '--answer', str(base / f'run{run}-reply.txt')],
                               capture_output=True, text=True)
        (base / f'run{run}-grade.txt').write_text(grade.stdout + grade.stderr)
        last = grade.stdout.strip().splitlines()[-1] if grade.stdout.strip() else 'no grader output'
        summary.append({'run': run, 'agent_exit': result.returncode, 'seconds': elapsed, 'grade': last,
                        'grade_exit': grade.returncode})
        print(json.dumps(summary[-1]))
    (base / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return 0 if all(item['grade_exit'] == 0 for item in summary) else 1


if __name__ == '__main__':
    sys.exit(main())
