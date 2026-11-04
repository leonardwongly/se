"""Local HTML reference regressions; no network or third-party dependencies."""
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from validate import validate_html_links


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


if __name__ == '__main__':
    unittest.main()
