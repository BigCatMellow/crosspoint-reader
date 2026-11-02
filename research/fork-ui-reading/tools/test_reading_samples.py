#!/usr/bin/env python3
"""Host checks for reproducible, self-contained CrossPoint test EPUBs."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from xml.etree import ElementTree as ET
import zipfile

GENERATOR = Path(__file__).with_name('make_reading_samples.py')
spec = importlib.util.spec_from_file_location('make_reading_samples', GENERATOR)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

OPF = '{http://www.idpf.org/2007/opf}'

class EpubSamplesTest(unittest.TestCase):
    def test_epubs_are_valid_and_self_contained(self):
        with TemporaryDirectory() as tmp:
            output = Path(tmp)
            module.build_samples(output)
            self.assertEqual({f.name for f in output.glob('*.epub')},
                             {'reading-prose.epub', 'reading-stress.epub'})
            for path in output.glob('*.epub'):
                with self.subTest(book=path.name), zipfile.ZipFile(path) as book:
                    names = book.namelist()
                    self.assertEqual(names[0], 'mimetype')
                    self.assertEqual(book.read('mimetype'), b'application/epub+zip')
                    self.assertEqual(book.getinfo('mimetype').compress_type, zipfile.ZIP_STORED)
                    ET.fromstring(book.read('META-INF/container.xml'))
                    opf = ET.fromstring(book.read('OEBPS/content.opf'))
                    manifest = opf.find(OPF+'manifest')
                    spine = opf.find(OPF+'spine')
                    self.assertIsNotNone(manifest)
                    self.assertIsNotNone(spine)
                    item_map = {item.attrib['id']: item.attrib['href'] for item in manifest}
                    self.assertIn('nav', item_map)
                    for item in item_map.values():
                        self.assertIn('OEBPS/'+item, names)
                        ET.fromstring(book.read('OEBPS/'+item))
                    for ref in spine:
                        self.assertIn(ref.attrib['idref'], item_map)
                    self.assertFalse(any(n.endswith(('.ttf','.otf','.jpg','.png')) for n in names))

    def test_output_is_deterministic(self):
        with TemporaryDirectory() as a, TemporaryDirectory() as b:
            module.build_samples(Path(a))
            module.build_samples(Path(b))
            for name in ('reading-prose.epub', 'reading-stress.epub'):
                self.assertEqual((Path(a)/name).read_bytes(), (Path(b)/name).read_bytes())

if __name__ == '__main__':
    unittest.main()
