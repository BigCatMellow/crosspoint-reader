#!/usr/bin/env python3
"""Build original, font-neutral EPUB 3 samples for CrossPoint X4 Pro comparisons.

No dependencies outside the Python standard library. No embedded fonts or images.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

DATE = (2024, 1, 1, 0, 0, 0)
NS = 'http://www.w3.org/1999/xhtml'

PROSE = [
    'The first page of a book should feel like an open door rather than a control panel. A reader notices the rhythm of a paragraph before noticing the software that made it. Lines of similar length are easier to follow than a column of scattered words, but a little variation gives prose its natural pace.',
    'At the window, the light changed slowly. Nothing on the desk moved except the shadow of a cup, which had stretched across a folded letter. The room had no clock. Its occupant preferred to judge the hour by the warmth of the glass and the sound of footsteps crossing the hall.',
    'A short sentence can create a pause. A longer sentence, unfolding clause by clause, gives the eye more work to do and makes irregular spaces between words much more visible. When a paragraph contains both, the line-breaking engine has to make sensible choices without drawing attention to itself.',
    'The person reading this passage is not expected to admire a font. The aim is simpler: letters should remain distinct, words should appear evenly spaced, and the end of one line should lead effortlessly to the start of the next. Good typography becomes most successful when it disappears.',
    'Near the garden gate, an old notebook lay open to a page of measurements. They were ordinary numbers, written with care: 18, 24, 36, and 48. Beside them stood a note about the weather, and a reminder to return before sunset. The smallest details were often the easiest to overlook.',
    'Another paragraph begins with no ornament and no special instruction. The setting should come from the reading software rather than from a publisher forcing its preferred typeface, margin, or line height. That is the purpose of this controlled sample: to compare the same words while changing one reader setting at a time.',
]

STRESS_PARAGRAPHS = [
    'Distinguish I, l, 1, |, O, 0, rn, m, vv, w, c, e, a, o, 8, B, S, 5, and the pairs cl / d. In small type, open counters and clear punctuation matter more than decoration.',
    'Compare quotation marks: “double,” ‘single,’ straight "double", and apostrophe’s shape. Also compare en dash – with em dash — and minus sign −. The ellipsis … should not be mistaken for three separate full stops...',
    'Accents and language: café, naïve, façade, piñata, jalapeño, Straße, smörgåsbord, Łódź, Ελληνικά, кириллица. Missing glyphs should be visible as missing, not silently substituted with the wrong letter.',
    'Spacing and wrapping: extraordinary, intercontinental, counterrevolutionary, incomprehensibility, electroencephalographically, and antidisestablishmentarianism. Keep each word together unless a valid break occurs.',
    'Numbers and punctuation: 0123456789, 1,234.56, (12:30), [42], {7}, #5, 50%, $19.95, €42, +4.0, 3/8, 2026–2027, and sentence endings?!',
]

def wrap_xhtml(title: str, body: str) -> bytes:
    content = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="{NS}" xml:lang="en"><head><title>{html.escape(title)}</title>
<meta charset="utf-8" /></head><body>{body}</body></html>'''
    ET.fromstring(content.encode('utf-8'))
    return content.encode('utf-8')

def write_epub(path: Path, title: str, identifier: str, chapters: list[tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entries: list[tuple[str, bytes]] = []
    container = b'''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>
<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
</rootfiles></container>'''
    entries.append(('META-INF/container.xml', container))
    manifest = []
    spine = []
    nav_list = []
    for number, (chapter_title, body) in enumerate(chapters, 1):
        filename = f'chapter-{number}.xhtml'
        ident = f'ch{number}'
        entries.append((f'OEBPS/{filename}', wrap_xhtml(chapter_title, body)))
        manifest.append(f'<item id="{ident}" href="{filename}" media-type="application/xhtml+xml" />')
        spine.append(f'<itemref idref="{ident}" />')
        nav_list.append(f'<li><a href="{filename}">{html.escape(chapter_title)}</a></li>')
    nav = wrap_xhtml('Contents', f'<nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc"><h1>Contents</h1><ol>{"".join(nav_list)}</ol></nav>')
    entries.append(('OEBPS/nav.xhtml', nav))
    package = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:{identifier}</dc:identifier><dc:title>{html.escape(title)}</dc:title>
<dc:language>en</dc:language><dc:creator>CrossPoint Reading Research</dc:creator>
<meta property="dcterms:modified">2026-11-02T00:00:00Z</meta>
</metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>'''
    entries.append(('OEBPS/content.opf', package.encode('utf-8')))
    for name, value in entries:
        ET.fromstring(value)
    with zipfile.ZipFile(path, 'w') as archive:
        mimetype = zipfile.ZipInfo('mimetype', date_time=DATE)
        mimetype.compress_type = zipfile.ZIP_STORED
        archive.writestr(mimetype, b'application/epub+zip')
        for name, value in entries:
            info = zipfile.ZipInfo(name, date_time=DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, value)

def build_samples(output: Path) -> None:
    prose_chapters = []
    for idx, heading in enumerate(('A Quiet Page', 'A Longer Passage', 'The Last Page'), 1):
        paragraphs = [f'<p>{html.escape(PROSE[(idx + n) % len(PROSE)])}</p>' for n in range(16)]
        prose_chapters.append((heading, f'<h1>{heading}</h1>' + ''.join(paragraphs)))
    write_epub(output / 'reading-prose.epub', 'Reading Test — Ordinary Prose',
               'a5527c52-67ee-4339-a6ce-50bdd879a009', prose_chapters)
    stress = [f'<p>{html.escape(p)}</p>' for p in STRESS_PARAGRAPHS]
    blocks = [
        '<h1>Typography checks</h1>', *stress,
        '<h2>Bold and italic</h2><p>Normal <strong>bold letterforms</strong> and <em>italic emphasis</em> should be recognizably different. <strong><em>Combined emphasis</em></strong> must remain legible.</p>',
        '<h2>Paragraph rhythm</h2><p>Very short.</p><p>A paragraph of moderate length provides a contrasting rhythm, and it should not cause the entire page to become visually ragged merely because one short line appears.</p>',
        '<blockquote><p>Indented passages should read as quotations, not as broken columns of text.</p></blockquote>',
        '<h2>Lists and tables</h2><ul><li>First point</li><li>A second, longer point with punctuation and numbers: 1, 2, 3.</li></ul>',
        '<table><thead><tr><th>Measure</th><th>First</th><th>Second</th></tr></thead><tbody><tr><td>Width</td><td>12</td><td>18</td></tr><tr><td>Count</td><td>8</td><td>16</td></tr></tbody></table>',
        '<h2>Links and a footnote</h2><p>Go to <a href="#note1">the note</a> and return without losing your place.</p><aside id="note1"><p>Note one: this is a local link within the chapter.</p></aside>',
    ]
    write_epub(output / 'reading-stress.epub', 'Reading Test — Typography and Layout',
               '354fd5d3-b628-48d0-af28-8670609e0281', [('Type Specimen', ''.join(blocks))])

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=Path.cwd())
    args = ap.parse_args()
    build_samples(args.output)

if __name__ == '__main__':
    main()
