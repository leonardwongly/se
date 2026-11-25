"""Local HTML reference regressions; no network or third-party dependencies."""
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from validate import (validate_baseline, validate_frontmatter, validate_html_links, validate_notice,
                      validate_recommended_instruction, validate_residue, validate_skill_references,
                      skill_edges)


class HTMLLinkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'repo'
        self.docs = self.root / 'docs'
        self.docs.mkdir(parents=True)
        for name in ('index.html', 'skill-map.html'):
            (self.docs / name).write_text('<!doctype html>', encoding='utf-8')
        (self.docs / 'assets').mkdir()
        (self.docs / 'assets/guide.css').write_text('body {}', encoding='utf-8')

    def write_html(self, text, name='index.html'):
        (self.docs / name).write_text(text, encoding='utf-8')

    def test_existing_relative_targets(self):
        (self.root / 'README.md').write_text('Guide', encoding='utf-8')
        self.write_html('<link href="assets/guide.css"><a href="../README.md">Read</a>')
        self.write_html('<a href="index.html#skills">Guide</a>', 'skill-map.html')
        validate_html_links(self.root)

    def test_query_fragment_and_percent_encoded_paths(self):
        for name in ('a b.css', 'a#b?.css', 'café.css', '%20.css', 'a+b.css'):
            (self.docs / name).touch()
        self.write_html('''
            <link href="a%20b.css?v=missing.css#missing-id">
            <link href="a%23b%3F.css?x=1&amp;y=2#section">
            <link href="caf%C3%A9.css"><link href="%2520.css">
            <link href="a+b.css">
        ''')
        validate_html_links(self.root)

    def test_missing_targets_in_both_entry_points(self):
        for name in ('index.html', 'skill-map.html'):
            for attribute in ('src', 'href'):
                with self.subTest(name=name, attribute=attribute):
                    self.write_html(f'<img {attribute}="missing%20file.png?v=1#part">', name)
                    with self.assertRaises(SystemExit) as caught:
                        validate_html_links(self.root)
                    message = str(caught.exception)
                    self.assertIn(f'docs/{name}:1:', message)
                    self.assertIn(f'{attribute}=\'missing%20file.png?v=1#part\'', message)
                    self.assertIn('missing local target', message)
                    self.write_html('', name)

    def test_escape_targets_even_when_they_exist(self):
        outside = self.root.parent / 'outside.css'
        outside.touch()
        prefix_neighbor = self.root.parent / 'repo-other'
        prefix_neighbor.mkdir()
        (prefix_neighbor / 'guide.css').touch()
        for target in ('../../outside.css', '%2e%2e/%2e%2e/outside.css',
                       '..%2F..%2Foutside.css', '../../repo-other/guide.css',
                       str(outside), '../../absent.css'):
            with self.subTest(target=target):
                self.write_html(f'<link href="{target}">')
                with self.assertRaisesRegex(SystemExit, 'target escapes repository'):
                    validate_html_links(self.root)

    def test_symlink_escape(self):
        outside = self.root.parent / 'outside.css'
        outside.touch()
        (self.docs / 'linked.css').symlink_to(outside)
        self.write_html('<link href="linked.css">')
        with self.assertRaisesRegex(SystemExit, 'target escapes repository'):
            validate_html_links(self.root)

    def test_external_and_data_references_do_not_access_network(self):
        self.write_html('''
            <a href="https://example.invalid/missing.html?q=1#part">External</a>
            <script src="//example.invalid/missing.js"></script>
            <a href="mailto:someone@example.invalid">Mail</a>
            <img src="data:image/png;base64,AAAA">
        ''')
        with patch.object(socket, 'socket', side_effect=AssertionError('network access')):
            validate_html_links(self.root)

    def test_same_document_references(self):
        self.write_html('<a href="#missing-id">Link</a><a href="?v=1#part">Query</a>'
                        '<a href="">Empty</a><img src><a href="  #part  ">Spaced</a>')
        validate_html_links(self.root)

    def test_base_href_rejected_in_both_entry_points(self):
        for name in ('index.html', 'skill-map.html'):
            for element in (
                '<base href="assets/">',
                '<base href="missing/">',
                '<base href="https://example.invalid/">',
                '<base href="//example.invalid/">',
                '<base href="">',
                '<base href="  ">',
                '<base href="#part">',
                '<base href>',
                '<BASE HREF=assets/>',
                '<BaSe HrEf="" />',
                '<base target="_blank" href="">',
                '<base href="" href="https://example.invalid/">',
            ):
                with self.subTest(name=name, element=element):
                    self.write_html('<!doctype html>\n' + element +
                                    '\n<link href="assets/guide.css">', name)
                    with patch.object(socket, 'socket', side_effect=AssertionError('network access')):
                        with self.assertRaises(SystemExit) as caught:
                            validate_html_links(self.root)
                    message = str(caught.exception)
                    self.assertIn(f'docs/{name}:2:', message)
                    self.assertIn('<base href=', message)
                    self.assertIn('browser URL resolution is not modeled', message)
                    self.write_html('', name)

    def test_base_without_href_and_non_markup_lookalikes_allowed(self):
        for name in ('index.html', 'skill-map.html'):
            self.write_html('''
                <base target="_blank"><BASE TARGET="_self" /><base>
                <!-- <base href="https://example.invalid/"> -->
                <script>const example = '<base href="">';</script>
                <style>/* <base href=""> */</style>
                &lt;base href=""&gt;
                <link href="assets/guide.css">
            ''', name)
        validate_html_links(self.root)

    def test_html_attribute_syntax_and_non_markup_text(self):
        (self.docs / 'a&b.css').touch()
        self.write_html('''
            <!-- <img src="missing.png"> -->
            <script>const example = '<img src="missing.png">';</script>
            <LINK HREF=assets/guide.css>
            <img src='assets/guide.css'/><link href="a&amp;b.css">
        ''')
        validate_html_links(self.root)
        self.write_html('<IMG SRC=missing.png />')
        with self.assertRaisesRegex(SystemExit, 'missing local target'):
            validate_html_links(self.root)

    def test_missing_entry_point_and_invalid_path_fail_usefully(self):
        for target in ('bad%00.css', 'bad%FF.css'):
            with self.subTest(target=target):
                self.write_html(f'<link href="{target}">')
                with self.assertRaisesRegex(SystemExit, 'docs/index.html:1:.*invalid local reference'):
                    validate_html_links(self.root)
        self.write_html('')
        (self.docs / 'skill-map.html').unlink()
        with self.assertRaisesRegex(SystemExit, 'docs/skill-map.html: missing HTML entry point'):
            validate_html_links(self.root)


class SkillPackageTests(unittest.TestCase):
    """Linkage, residue and frontmatter checks (specs/001-pstack-integration FR-4, FR-5, FR-7, FR-11)."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.expected = {'se-a', 'se-b'}
        for name in sorted(self.expected):
            self.write(f'{name}/SKILL.md', f'---\nname: {name}\ndescription: "Does {name}."\n---\n# {name}\n')
            self.write(f'{name}/agents/openai.yaml', f'interface:\n  display_name: "{name}"\n')

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_AC_5_2_known_references_pass(self):
        self.write('se-a/notes.md', 'Use se-b, then `/se-b` or **se-b**. Write `se-models.md` and se-b.\n')
        validate_skill_references(self.root, self.expected)

    def test_AC_5_3_unknown_skill_reference_fails_with_location(self):
        for text in ('Run `/se-missing` now.\n', 'Then se-missing.\n', 'Use **se-missing**\n'):
            with self.subTest(text=text):
                self.write('se-a/notes.md', 'ok\n' + text)
                with self.assertRaisesRegex(SystemExit, r"se-a/notes.md:2: reference to unknown skill 'se-missing'"):
                    validate_skill_references(self.root, self.expected)

    def test_paths_and_files_are_not_skill_references(self):
        self.write('se-a/notes.md', 'See ../se-b/SKILL.md, se-b/references/x.md and .se-tool-key.\n')
        validate_skill_references(self.root, self.expected)

    def test_AC_11_2_brand_residue_fails_in_any_file(self):
        for relative, text in (('se-a/notes.md', 'Ask poteto.\n'), ('se-a/tool.ts', '// pstack helper\n'),
                               ('se-a/notes.md', 'Read principle-prove-it-works.\n')):
            with self.subTest(text=text):
                self.write(relative, text)
                with self.assertRaisesRegex(SystemExit, f'{relative}:1: pstack or host-specific residue'):
                    validate_residue(self.root)
                (self.root / relative).unlink()

    def test_AC_11_2_old_names_and_host_features_fail_in_markdown(self):
        for text in ('Run `/teach` first.\n', 'Use the **arena** skill.\n', 'Then `how`.\n',
                     'Ask Bugbot.\n', 'Write ~/.cursor/rules/x.\n', 'Use the AskQuestion tool.\n'):
            with self.subTest(text=text):
                self.write('se-a/notes.md', text)
                with self.assertRaisesRegex(SystemExit, 'se-a/notes.md:1: pstack or host-specific residue'):
                    validate_residue(self.root)

    def test_AC_4_3_ordinary_words_are_not_residue(self):
        self.write('se-a/notes.md', 'Explain how and why to correct it; teach, reflect and recall.\n')
        self.write('se-a/tool.ts', 'const page = { endCursor: "next", name: "upstack-build" };\n')
        validate_residue(self.root)

    def test_AC_7_1_typed_only_flag_fails(self):
        self.write('se-a/SKILL.md', '---\nname: se-a\ndescription: "x"\ndisable-model-invocation: true\n---\n')
        with self.assertRaisesRegex(SystemExit, 'se-a: typed-only flag'):
            validate_frontmatter(self.root, self.expected)

    def test_AC_NFR3_1_long_description_fails(self):
        self.write('se-a/SKILL.md', f'---\nname: se-a\ndescription: "{"x" * 1025}"\n---\n')
        with self.assertRaisesRegex(SystemExit, 'se-a: description is 1025 characters'):
            validate_frontmatter(self.root, self.expected)
        self.write('se-a/SKILL.md', f'---\nname: se-a\ndescription: "{"x" * 1024}"\n---\n# se-a\n')
        validate_frontmatter(self.root, self.expected)

    def test_AC_4_1_title_must_match_the_se_display_name(self):
        validate_frontmatter(self.root, self.expected)
        for body, heading in (('\n# Unslop\n', 'Unslop'), ('\nNo title.\n', 'missing')):
            with self.subTest(heading=heading):
                self.write('se-a/SKILL.md', f'---\nname: se-a\ndescription: "x"\n---\n{body}')
                with self.assertRaisesRegex(SystemExit, f'se-a: title "{heading}" differs from its display name "se-a"'):
                    validate_frontmatter(self.root, self.expected)

    def test_AC_12_2_baseline_must_load_both_skills_by_name(self):
        head = '---\nname: se-a\ndescription: "x"\n---\n# se-a\n\n'
        good = ('## SE change baseline\n\n- **Review trust.** Load **se-zero-trust** and review the change with it.\n'
                '- **Verify.** Load **se-verify** and apply it.\n\n## Next\n\nLoad nothing here.\n')
        self.write('se-a/SKILL.md', head + good)
        validate_baseline(self.root, {'se-a'})
        for old, new, skill in (('Load **se-zero-trust** and review the change with it', 'Review trust with **se-zero-trust**', 'se-zero-trust'),
                                ('Load **se-verify** and apply it', 'Verify with **se-verify**', 'se-verify')):
            with self.subTest(skill=skill):
                self.write('se-a/SKILL.md', head + good.replace(old, new))
                with self.assertRaisesRegex(SystemExit, rf'se-a: the SE change baseline must load \*\*{skill}\*\* by name'):
                    validate_baseline(self.root, {'se-a'})
        self.write('se-a/SKILL.md', head + 'No baseline.\n## Next\n\nLoad **se-zero-trust** and load **se-verify**.\n')
        with self.assertRaisesRegex(SystemExit, 'se-a: no SE change baseline section'):
            validate_baseline(self.root, {'se-a'})

    def test_readme_recommends_the_tested_instruction(self):
        self.write('validation/pstack-selection/load-skill-instruction.md', 'Load the skill.\nThen follow it.\n')
        self.write('README.md', 'Add this:\n\n```text\nLoad the skill.\nThen follow it.\n```\n')
        validate_recommended_instruction(self.root)
        self.write('README.md', 'Add this:\n\n```text\nLoad the skill.\nThen maybe follow it.\n```\n')
        with self.assertRaisesRegex(SystemExit, 'README.md: the recommended project instruction differs'):
            validate_recommended_instruction(self.root)

    def test_AC_9_1_notice_needs_license_copyright_and_commit(self):
        with self.assertRaisesRegex(SystemExit, 'missing attribution'):
            validate_notice(self.root)
        self.write('THIRD_PARTY_NOTICES.md', 'MIT License\nCopyright (c) 2026 Lauren Tan\n')
        with self.assertRaisesRegex(SystemExit, 'c3464c11'):
            validate_notice(self.root)

    def test_edges_cover_tokens_and_links(self):
        self.write('se-a/notes.md', 'Use `/se-b`. [rule](../se-principles/references/x.md)\n')
        self.write('se-principles/references/x.md', 'See se-a.\n')
        edges = skill_edges(self.root, self.expected | {'se-principles'})
        self.assertIn(('se-a', 'se-b'), edges)
        self.assertIn(('se-a', 'se-principles#x'), edges)
        self.assertIn(('se-principles#x', 'se-a'), edges)


if __name__ == '__main__':
    unittest.main()
