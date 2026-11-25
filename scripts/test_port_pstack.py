"""Port script and port-result regressions (specs/001-pstack-integration)."""
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import port_pstack as port  # noqa: E402
import validate  # noqa: E402

PORT_DATA = validate.ROOT / 'validation/pstack-port'
TITLES = {'prove-it-works': 'Prove It Works', 'fix-root-causes': 'Fix Root Causes'}


def rewrite(text, src='poteto-mode/SKILL.md', dst='se-playbook/SKILL.md', new_name='se-playbook'):
    report = port.Report()
    out = port.rewrite_markdown(text, src, dst, TITLES, report, new_name)
    return out, report.as_dict()


class RewriteTests(unittest.TestCase):
    def test_AC_4_3_prose_words_are_unchanged(self):
        text = ('This explains how and why to correct it; teach, reflect, recall, '
                'sharpen, the arena and a swarm stay ordinary words.\n')
        self.assertEqual(rewrite(text)[0], text)

    def test_AC_1_2_reference_forms_are_renamed(self):
        out, _ = rewrite('Run `/teach`, then **arena**, `how` and /pstack:poteto-mode.\n')
        self.assertEqual(out, 'Run `/se-explain`, then **se-contest**, `se-how` and /se-playbook.\n')

    def test_distinctive_bare_names_are_renamed(self):
        out, _ = rewrite('Read the poteto-mode Subagents section, then show-me-your-work.\n')
        self.assertEqual(out, 'Read the se-playbook Subagents section, then se-decision-log.\n')

    def test_AC_3_2_principle_reference_becomes_link(self):
        out, _ = rewrite('Apply **principle-prove-it-works** and the principle-fix-root-causes skill.\n')
        self.assertEqual(
            out,
            'Apply [**Prove It Works**](../se-principles/references/prove-it-works.md) and the '
            '[Fix Root Causes](../se-principles/references/fix-root-causes.md) principle.\n')

    def test_principle_inside_link_label_becomes_title(self):
        out, _ = rewrite('[principle-prove-it-works](../principle-prove-it-works/SKILL.md)\n')
        self.assertEqual(out, '[Prove It Works](../se-principles/references/prove-it-works.md)\n')

    def test_AC_5_4_links_follow_relocated_files(self):
        out, _ = rewrite('[x](../unslop/SKILL.md) [y](../principle-fix-root-causes/SKILL.md#rule)\n',
                         src='principle-prove-it-works/SKILL.md',
                         dst='se-principles/references/prove-it-works.md')
        self.assertEqual(out, '[x](../../se-prose/SKILL.md) [y](fix-root-causes.md#rule)\n')

    def test_sibling_links_stay_relative(self):
        out, _ = rewrite('[b](bug-fix.md) [s](../SKILL.md)\n',
                         src='poteto-mode/playbooks/feature.md',
                         dst='se-playbook/playbooks/feature.md')
        self.assertEqual(out, '[b](bug-fix.md) [s](../SKILL.md)\n')

    def test_external_and_dropped_references_are_reported(self):
        out, notes = rewrite('[guide](../../docs/guide/01-setup.md) [bot](../make-bot-ui/SKILL.md) '
                             'and `/make-bot-ui`\n', src='poteto-help/SKILL.md', dst='se-help/SKILL.md',
                             new_name='se-help')
        self.assertIn('[guide](../../docs/guide/01-setup.md)', out)
        self.assertNotIn('](../make-bot-ui', out)
        self.assertEqual(notes['external_link'][0]['detail'], '../../docs/guide/01-setup.md')
        self.assertEqual(len(notes['dropped_link']), 1)
        self.assertEqual(len(notes['dropped_name']), 1)

    def test_urls_are_left_alone(self):
        out, _ = rewrite('See https://github.com/cursor/plugins/tree/main/pstack and pstack skills.\n')
        self.assertEqual(out, 'See https://github.com/cursor/plugins/tree/main/pstack and SE skills.\n')

    def test_brand_needs_word_boundaries(self):
        text = 'pendingCheck("upstack-build") stays.\n'
        self.assertEqual(rewrite(text)[0], text)

    def test_AC_7_1_frontmatter_is_renamed_and_typed_only_flag_removed(self):
        text = ('---\nname: teach\ndescription: "Runs the `how` skill."\n'
                'disable-model-invocation: true\nicon: crown\n---\n# Teach\n')
        out, _ = rewrite(text, src='teach/SKILL.md', dst='se-explain/SKILL.md', new_name='se-explain')
        self.assertEqual(out, '---\nname: se-explain\ndescription: "Runs the `se-how` skill."\n---\n# Teach\n')

    def test_principle_frontmatter_becomes_rule_line(self):
        text = ('---\nname: principle-prove-it-works\ndescription: "Apply after a task."\n'
                'disable-model-invocation: true\n---\n\n# Prove It Works\n\nBody.\n')
        out, _ = rewrite(text, src='principle-prove-it-works/SKILL.md',
                         dst='se-principles/references/prove-it-works.md')
        self.assertEqual(out, '# Prove It Works\n\n> Apply after a task.\n\nBody.\n')

    def test_script_literals_are_renamed(self):
        text = '{"name": "@cursor-skill/poteto-mode-tools"}\n/agent/repos/plugins/pstack/skills/statechart/x\n'
        self.assertEqual(port.rewrite_script(text),
                         '{"name": "@se/playbook-tools"}\n/agent/repos/se/se-states/x\n')


def write_skill(root, folder, body='', description='A skill.', heading=None):
    path = root / 'skills' / folder / 'SKILL.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'---\nname: {folder}\ndescription: "{description}"\n'
                    f'disable-model-invocation: true\n---\n\n# {heading or folder.title()}\n\n{body}\n')
    return path


class PortTreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / 'pstack'
        self.dest = Path(self.temp.name) / 'se'
        self.dest.mkdir()
        for folder in list(port.NAMES) + sorted(port.DROPPED):
            write_skill(self.source, folder)
        for slugs in port.PRINCIPLE_GROUPS.values():
            for slug in slugs:
                write_skill(self.source, f'principle-{slug}', description=f'Apply when {slug}.',
                            heading=slug.replace('-', ' ').title())
        playbook = self.source / 'skills/poteto-mode/playbooks/bug-fix.md'
        playbook.parent.mkdir(parents=True)
        playbook.write_text('Run [tdd](../../tdd/SKILL.md) per **principle-fix-root-causes**.\n')
        script = self.source / 'skills/poteto-mode/scripts/package.json'
        script.parent.mkdir()
        script.write_text('{"name": "@cursor-skill/poteto-mode-tools"}\n')
        tool = self.source / 'skills/poteto-mode/scripts/tool'
        tool.write_text('#!/bin/sh\necho ok\n')
        tool.chmod(0o755)

    def test_port_places_files_and_skips_merged_and_dropped(self):
        report, edges = port.port(self.source, self.dest)
        self.assertEqual((self.dest / 'se-playbook/playbooks/bug-fix.md').read_text(),
                         'Run [tdd](../../se-test-first/SKILL.md) per '
                         '[**Fix Root Causes**](../../se-principles/references/fix-root-causes.md).\n')
        self.assertIn('"@se/playbook-tools"', (self.dest / 'se-playbook/scripts/package.json').read_text())
        self.assertTrue(os.stat(self.dest / 'se-playbook/scripts/tool').st_mode & stat.S_IXUSR)
        for absent in ('se-how', 'se-why', 'se-swarm', 'make-bot-ui', 'se-make-bot-ui'):
            self.assertFalse((self.dest / absent).exists(), absent)
        references = sorted(p.name for p in (self.dest / 'se-principles/references').iterdir())
        self.assertEqual(len(references), 24)
        index = (self.dest / 'se-principles/SKILL.md').read_text()
        self.assertEqual(index.count('](references/'), 24)
        self.assertIn('name: se-principles', index)
        self.assertIn(('se-playbook', 'se-test-first'), edges)
        self.assertIn(('se-playbook', 'se-principles#fix-root-causes'), edges)
        self.assertEqual(len(report.notes['not_copied']), 4)

    def test_existing_output_needs_force(self):
        port.port(self.source, self.dest)
        with self.assertRaises(port.PortError):
            port.port(self.source, self.dest)
        port.port(self.source, self.dest, force=True)

    def test_unknown_source_folder_is_rejected(self):
        write_skill(self.source, 'brand-new-skill')
        with self.assertRaises(port.PortError):
            port.port(self.source, self.dest)


class PortResultTests(unittest.TestCase):
    """Checks against the committed port output and its recorded source edges."""

    def setUp(self):
        self.edges = [tuple(edge) for edge in
                      json.loads((PORT_DATA / 'source-edges.json').read_text())['edges']]
        self.removed = json.loads((PORT_DATA / 'removed-edges.json').read_text())['removed']

    def test_AC_5_4_every_pstack_link_survives_or_is_recorded(self):
        actual = validate.skill_edges(validate.ROOT)
        removed = {(item['from'], item['to']) for item in self.removed}
        missing = [edge for edge in self.edges if edge not in actual and edge not in removed]
        self.assertEqual(missing, [])

    def test_removed_edges_are_real_and_explained(self):
        for item in self.removed:
            self.assertIn((item['from'], item['to']), self.edges, item)
            self.assertTrue(item['reason'].strip(), item)

    def test_edges_come_from_the_pinned_commit(self):
        data = json.loads((PORT_DATA / 'source-edges.json').read_text())
        self.assertEqual(data['source_commit'], port.PINNED_COMMIT)


if __name__ == '__main__':
    unittest.main()
