"""Behavioral Markdown URL checks using disposable local fixtures."""
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from validate import validate_markdown_links


class MarkdownLinkTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / 'repo'
        self.docs = self.root / 'docs'
        self.docs.mkdir(parents=True)
        self.source = self.docs / 'guide.md'
        (self.docs / 'guide.css').write_bytes(b'local asset')
        (self.root / 'README.md').write_text('Root', encoding='utf-8')

    def check(self, *targets):
        self.source.write_text('\n'.join(f'[Link]({target})' for target in targets),
                               encoding='utf-8')
        validate_markdown_links(self.source, self.root)

    def test_valid_queries_and_encoded_filenames(self):
        for name in ('a b.css', 'a#b?.css', 'café.css', '%20.css', 'a+b.css'):
            (self.docs / name).write_bytes(b'asset')
        self.check('guide.css?rev=1#part', '../README.md#part',
                   'guide.css?redirect=https://example.invalid/',
                   'a%20b.css?rev=1', 'a%23b%3F.css?q=1#part',
                   'caf%C3%A9.css', '%2520.css', 'a+b.css')

    def test_url_text_in_query_cannot_bypass_escape_check(self):
        outside = self.base / 'outside.css'
        outside.write_bytes(b'outside sentinel')
        with self.assertRaisesRegex(SystemExit, 'target escapes repository'):
            self.check('../../outside.css?redirect=https://example.invalid/')
        self.assertEqual(outside.read_bytes(), b'outside sentinel')

    def test_url_text_in_query_or_fragment_cannot_hide_missing_target(self):
        for target in ('missing.css?redirect=https://example.invalid/',
                       'missing.css#https://example.invalid/', 'missing%20file.css?v=1'):
            with self.subTest(target=target):
                with self.assertRaisesRegex(SystemExit, 'guide.md: invalid link .*missing local target'):
                    self.check(target)
        self.assertFalse((self.docs / 'missing.css').exists())

    def test_percent_traversal_and_prefix_neighbor_are_rejected(self):
        outside = self.base / 'outside.css'
        outside.write_bytes(b'sentinel')
        neighbor = self.base / 'repo-other'
        neighbor.mkdir()
        (neighbor / 'asset.css').write_bytes(b'neighbor')
        for target in ('%2e%2e/%2e%2e/outside.css', '..%2F..%2Foutside.css',
                       '../../repo-other/asset.css', str(outside)):
            with self.subTest(target=target):
                with self.assertRaisesRegex(SystemExit, 'target escapes repository'):
                    self.check(target)
        self.assertEqual(outside.read_bytes(), b'sentinel')

    def test_containment_precedes_existence(self):
        with patch.object(Path, 'exists', side_effect=AssertionError('exists reached')):
            with self.assertRaisesRegex(SystemExit, 'target escapes repository'):
                self.check('../../absent.css?redirect=https://example.invalid/')

    def test_symlink_file_and_directory_escapes_are_rejected(self):
        external = self.base / 'outside'
        external.mkdir()
        target = external / 'asset.css'
        target.write_bytes(b'outside bytes')
        (self.docs / 'linked.css').symlink_to(target)
        (self.docs / 'linked-dir').symlink_to(external, target_is_directory=True)
        for link in ('linked.css', 'linked-dir/asset.css?query=1'):
            with self.subTest(link=link):
                with self.assertRaisesRegex(SystemExit, 'target escapes repository'):
                    self.check(link)
        self.assertEqual(target.read_bytes(), b'outside bytes')

    def test_external_and_pathless_references_are_skipped_without_network(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network access')):
            self.check('https://example.invalid/missing.css', '//example.invalid/missing.css',
                       'mailto:someone@example.invalid', 'data:text/plain,example',
                       '#missing-fragment', '?q=1#part', '  #part  ')

    def test_malformed_urls_and_decoded_paths_fail_usefully(self):
        for target in ('//[invalid', 'bad%FF.css', 'bad%00.css'):
            with self.subTest(target=target):
                with self.assertRaisesRegex(SystemExit, 'docs/guide.md: invalid link .*invalid local reference'):
                    self.check(target)

    def test_images_use_same_local_reference_boundary(self):
        self.source.write_text('![image](missing.png?redirect=https://example.invalid/)',
                               encoding='utf-8')
        with self.assertRaisesRegex(SystemExit, 'missing local target'):
            validate_markdown_links(self.source, self.root)


if __name__ == '__main__':
    unittest.main()
