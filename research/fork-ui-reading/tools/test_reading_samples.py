#!/usr/bin/env python3
"""Host checks for reproducible, self-contained CrossPoint test EPUBs.

These checks prove the files are well-formed EPUB containers. They do not prove
that an X4 Pro renders them correctly.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path, PurePosixPath
import re
from tempfile import TemporaryDirectory
import unittest
from xml.etree import ElementTree as ET
import zipfile

GENERATOR = Path(__file__).with_name('make_reading_samples.py')
spec = importlib.util.spec_from_file_location('make_reading_samples', GENERATOR)
assert spec and spec.loader, f'cannot load {GENERATOR}'
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

OPF = '{http://www.idpf.org/2007/opf}'
XHTML = '{http://www.w3.org/1999/xhtml}'
EPUB_TYPE = '{http://www.idpf.org/2007/ops}type'
BOOKS = {'reading-prose.epub', 'reading-stress.epub', 'reading-legacy-ncx.epub'}
DATA_DESCRIPTOR_FLAG = 0x08


def opf_dir(book: zipfile.ZipFile) -> PurePosixPath:
    rootfile = ET.fromstring(book.read('META-INF/container.xml')).find(
        './/{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
    return PurePosixPath(rootfile.attrib['full-path']).parent


class EpubSamplesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = TemporaryDirectory()
        cls.output = Path(cls._tmp.name)
        module.build_samples(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def check_each(self, check):
        """Run check(name, book) per book; failures are reported by book name."""
        for path in sorted(self.output.glob('*.epub')):
            with self.subTest(book=path.name), zipfile.ZipFile(path) as book:
                check(path.name, book)

    def test_expected_books(self):
        self.assertEqual({f.name for f in self.output.glob('*.epub')}, BOOKS)

    def test_mimetype_entry(self):
        def check(_, book):
            info = book.infolist()[0]
            self.assertEqual(info.filename, 'mimetype')
            self.assertEqual(book.read(info), b'application/epub+zip')
            self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(info.extra, b'', 'mimetype must have no extra field')
            self.assertFalse(info.flag_bits & DATA_DESCRIPTOR_FLAG)
        self.check_each(check)

    def test_manifest_and_spine(self):
        def check(_, book):
            names = set(book.namelist())
            base = opf_dir(book)
            opf = ET.fromstring(book.read(str(base / 'content.opf')))
            manifest, spine = opf.find(OPF + 'manifest'), opf.find(OPF + 'spine')
            self.assertIsNotNone(manifest)
            self.assertIsNotNone(spine)
            items = {item.attrib['id']: item.attrib['href'] for item in manifest}
            for href in items.values():
                self.assertIn(str(base / href), names)
                ET.fromstring(book.read(str(base / href)))
            for ref in spine:
                self.assertIn(ref.attrib['idref'], items)
            self.assertFalse(any(n.lower().endswith(('.ttf', '.otf', '.woff', '.woff2', '.jpg', '.jpeg', '.png', '.gif', '.svg'))
                                 for n in names))
        self.check_each(check)

    def test_toc_kind(self):
        def check(name, book):
            names = set(book.namelist())
            opf = ET.fromstring(book.read('OEBPS/content.opf'))
            if name == 'reading-legacy-ncx.epub':
                self.assertEqual(opf.attrib['version'], '2.0')
                self.assertIn('OEBPS/toc.ncx', names)
                self.assertNotIn('OEBPS/nav.xhtml', names)
                self.assertEqual(opf.find(OPF + 'spine').attrib.get('toc'), 'ncx')
            else:
                self.assertEqual(opf.attrib['version'], '3.0')
                self.assertIn('OEBPS/nav.xhtml', names)
                nav = ET.fromstring(book.read('OEBPS/nav.xhtml')).find(f'.//{XHTML}nav')
                self.assertEqual(nav.attrib.get(EPUB_TYPE), 'toc')
        self.check_each(check)

    def test_noterefs_resolve(self):
        with zipfile.ZipFile(self.output / 'reading-stress.epub') as book:
            chapter = ET.fromstring(book.read('OEBPS/chapter-1.xhtml'))
            notes = ET.fromstring(book.read('OEBPS/notes.xhtml'))
            footnote_ids = {el.attrib['id'] for el in notes.iter(f'{XHTML}aside')
                            if el.attrib.get(EPUB_TYPE) == 'footnote'}
            refs = [a for a in chapter.iter(f'{XHTML}a') if a.attrib.get(EPUB_TYPE) == 'noteref']
            self.assertGreaterEqual(len(refs), 2)
            for ref in refs:
                target_file, _, target_id = ref.attrib['href'].partition('#')
                self.assertEqual(target_file, 'notes.xhtml')
                self.assertIn(target_id, footnote_ids)

    def test_prose_paragraph_markers_are_unique(self):
        with zipfile.ZipFile(self.output / 'reading-prose.epub') as book:
            text = b''.join(book.read(f'OEBPS/chapter-{n}.xhtml') for n in (1, 2, 3)).decode()
        markers = re.findall(r'\[(\d+\.\d\d)\]', text)
        expected = len(module.PROSE_HEADINGS) * module.PARAGRAPHS_PER_CHAPTER
        self.assertEqual(len(markers), expected)
        self.assertEqual(len(set(markers)), expected)

    def test_output_is_deterministic(self):
        with TemporaryDirectory() as other:
            module.build_samples(Path(other))
            for name in BOOKS:
                self.assertEqual((self.output / name).read_bytes(), (Path(other) / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
