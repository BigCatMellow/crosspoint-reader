#!/usr/bin/env python3
"""Build original, font-neutral EPUB samples for CrossPoint X4 Pro comparisons.

Books:
  reading-prose.epub       EPUB 3, three chapters of plain prose. Every paragraph
                           starts with a [chapter.paragraph] marker so lost or
                           repeated text across page turns is easy to spot.
  reading-stress.epub      EPUB 3, typography stress page plus a separate notes
                           file reached through epub:type="noteref" links.
  reading-legacy-ncx.epub  EPUB 2.0.1 with toc.ncx only (no nav document), to
                           exercise the older table-of-contents path.

No dependencies outside the Python standard library. No embedded fonts or images.
Output is byte-identical across runs and operating systems.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

DATE = (2024, 1, 1, 0, 0, 0)
MODIFIED = '2026-11-02T00:00:00Z'
XHTML_NS = 'http://www.w3.org/1999/xhtml'
EPUB_NS = 'http://www.idpf.org/2007/ops'
FILE_MODE = 0o644 << 16
ZIP_UNIX = 3  # create_system; fixed so output does not depend on host OS

PROSE = [
    'The first page of a book should feel like an open door rather than a control panel. A reader notices the rhythm of a paragraph before noticing the software that made it. Lines of similar length are easier to follow than a column of scattered words, but a little variation gives prose its natural pace.',
    'At the window, the light changed slowly. Nothing on the desk moved except the shadow of a cup, which had stretched across a folded letter. The room had no clock. Its occupant preferred to judge the hour by the warmth of the glass and the sound of footsteps crossing the hall.',
    'A short sentence can create a pause. A longer sentence, unfolding clause by clause, gives the eye more work to do and makes irregular spaces between words much more visible. When a paragraph contains both, the line-breaking engine has to make sensible choices without drawing attention to itself.',
    'The person reading this passage is not expected to admire a font. The aim is simpler: letters should remain distinct, words should appear evenly spaced, and the end of one line should lead effortlessly to the start of the next. Good typography becomes most successful when it disappears.',
    'Near the garden gate, an old notebook lay open to a page of measurements. They were ordinary numbers, written with care: 18, 24, 36, and 48. Beside them stood a note about the weather, and a reminder to return before sunset. The smallest details were often the easiest to overlook.',
    'Another paragraph begins with no ornament and no special instruction. The setting should come from the reading software rather than from a publisher forcing its preferred typeface, margin, or line height. That is the purpose of this controlled sample: to compare the same words while changing one reader setting at a time.',
]
PROSE_HEADINGS = ('A Quiet Page', 'A Longer Passage', 'The Last Page')
PARAGRAPHS_PER_CHAPTER = 16

STRESS_PARAGRAPHS = [
    'Distinguish I, l, 1, |, O, 0, rn, m, vv, w, c, e, a, o, 8, B, S, 5, and the pairs cl / d. In small type, open counters and clear punctuation matter more than decoration.',
    'Compare quotation marks: “double,” ‘single,’ straight "double", and apostrophe’s shape. Also compare en dash – with em dash — and minus sign −. The ellipsis … should not be mistaken for three separate full stops...',
    'Accents and language: café, naïve, façade, piñata, jalapeño, Straße, smörgåsbord, Łódź, Ελληνικά, кириллица. Missing glyphs should be visible as missing, not silently substituted with the wrong letter.',
    'Spacing and wrapping: extraordinary, intercontinental, counterrevolutionary, incomprehensibility, electroencephalographically, and antidisestablishmentarianism. Keep each word together unless a valid break occurs.',
    'Numbers and punctuation: 0123456789, 1,234.56, (12:30), [42], {7}, #5, 50%, $19.95, €42, +4.0, 3/8, 2026–2027, and sentence endings?!',
]


def xhtml(title: str, body: str, *, epub2: bool = False) -> bytes:
    # EPUB 2 content is XHTML 1.1: no epub: namespace, no <meta charset>.
    ns = '' if epub2 else f' xmlns:epub="{EPUB_NS}"'
    meta = ('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' if epub2
            else '<meta charset="utf-8" />')
    content = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="{XHTML_NS}"{ns} xml:lang="en"><head><title>{html.escape(title)}</title>
{meta}</head><body>{body}</body></html>'''
    return content.encode('utf-8')


def container_xml() -> bytes:
    return b'''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>
<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
</rootfiles></container>'''


def write_zip(path: Path, entries: list[tuple[str, bytes]]) -> None:
    """Write an EPUB container: stored 'mimetype' first, then deflated entries."""
    for name, value in entries:
        ET.fromstring(value)  # every entry is XML; fail before writing a bad book
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w') as archive:
        for name, value, method in [('mimetype', b'application/epub+zip', zipfile.ZIP_STORED),
                                    *((n, v, zipfile.ZIP_DEFLATED) for n, v in entries)]:
            info = zipfile.ZipInfo(name, date_time=DATE)
            info.compress_type = method
            info.create_system = ZIP_UNIX
            info.external_attr = FILE_MODE
            archive.writestr(info, value)


def write_epub3(path: Path, title: str, identifier: str,
                chapters: list[tuple[str, str, str]],
                extra: list[tuple[str, str, str]] = ()) -> None:
    """chapters/extra: (filename, title, body). extra files are in the spine but not the TOC."""
    entries: list[tuple[str, bytes]] = [('META-INF/container.xml', container_xml())]
    manifest, spine, nav_list = [], [], []
    for number, (filename, chapter_title, body) in enumerate([*chapters, *extra], 1):
        ident = f'item{number}'
        entries.append((f'OEBPS/{filename}', xhtml(chapter_title, body)))
        manifest.append(f'<item id="{ident}" href="{filename}" media-type="application/xhtml+xml" />')
        spine.append(f'<itemref idref="{ident}" />')
        if number <= len(chapters):
            nav_list.append(f'<li><a href="{filename}">{html.escape(chapter_title)}</a></li>')
    entries.append(('OEBPS/nav.xhtml', xhtml(
        'Contents', f'<nav epub:type="toc"><h1>Contents</h1><ol>{"".join(nav_list)}</ol></nav>')))
    package = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:{identifier}</dc:identifier><dc:title>{html.escape(title)}</dc:title>
<dc:language>en</dc:language><dc:creator>CrossPoint Reading Research</dc:creator>
<meta property="dcterms:modified">{MODIFIED}</meta>
</metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />
{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>'''
    entries.append(('OEBPS/content.opf', package.encode('utf-8')))
    write_zip(path, entries)


def write_epub2_ncx(path: Path, title: str, identifier: str,
                    chapters: list[tuple[str, str, str]]) -> None:
    entries: list[tuple[str, bytes]] = [('META-INF/container.xml', container_xml())]
    manifest, spine, nav_points = [], [], []
    for number, (filename, chapter_title, body) in enumerate(chapters, 1):
        ident = f'item{number}'
        entries.append((f'OEBPS/{filename}', xhtml(chapter_title, body, epub2=True)))
        manifest.append(f'<item id="{ident}" href="{filename}" media-type="application/xhtml+xml" />')
        spine.append(f'<itemref idref="{ident}" />')
        nav_points.append(f'<navPoint id="np{number}" playOrder="{number}"><navLabel><text>'
                          f'{html.escape(chapter_title)}</text></navLabel><content src="{filename}" /></navPoint>')
    ncx = f'''<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head>
<meta name="dtb:uid" content="urn:uuid:{identifier}" /><meta name="dtb:depth" content="1" />
<meta name="dtb:totalPageCount" content="0" /><meta name="dtb:maxPageNumber" content="0" /></head>
<docTitle><text>{html.escape(title)}</text></docTitle><navMap>{"".join(nav_points)}</navMap></ncx>'''
    entries.append(('OEBPS/toc.ncx', ncx.encode('utf-8')))
    package = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="bookid">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:{identifier}</dc:identifier><dc:title>{html.escape(title)}</dc:title>
<dc:language>en</dc:language><dc:creator>CrossPoint Reading Research</dc:creator>
</metadata><manifest><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
{"".join(manifest)}</manifest><spine toc="ncx">{"".join(spine)}</spine></package>'''
    entries.append(('OEBPS/content.opf', package.encode('utf-8')))
    write_zip(path, entries)


def prose_chapters() -> list[tuple[str, str, str]]:
    chapters = []
    for chapter, heading in enumerate(PROSE_HEADINGS, 1):
        paragraphs = ''.join(
            f'<p>[{chapter}.{n + 1:02d}] {html.escape(PROSE[(chapter + n) % len(PROSE)])}</p>'
            for n in range(PARAGRAPHS_PER_CHAPTER))
        chapters.append((f'chapter-{chapter}.xhtml', heading, f'<h1>{heading}</h1>{paragraphs}'))
    return chapters


def stress_chapters() -> tuple[list[tuple[str, str, str]], list[tuple[str, str, str]]]:
    blocks = [
        '<h1>Typography checks</h1>', *(f'<p>{html.escape(p)}</p>' for p in STRESS_PARAGRAPHS),
        '<h2>Bold and italic</h2><p>Normal <strong>bold letterforms</strong> and <em>italic emphasis</em> should be recognizably different. <strong><em>Combined emphasis</em></strong> must remain legible.</p>',
        '<h2>Paragraph rhythm</h2><p>Very short.</p><p>A paragraph of moderate length provides a contrasting rhythm, and it should not cause the entire page to become visually ragged merely because one short line appears.</p>',
        '<blockquote><p>Indented passages should read as quotations, not as broken columns of text.</p></blockquote>',
        '<h2>Lists and tables</h2><ul><li>First point</li><li>A second, longer point with punctuation and numbers: 1, 2, 3.</li></ul>',
        '<table><thead><tr><th>Measure</th><th>First</th><th>Second</th></tr></thead><tbody><tr><td>Width</td><td>12</td><td>18</td></tr><tr><td>Count</td><td>8</td><td>16</td></tr></tbody></table>',
        '<h2>Notes and links</h2>'
        '<p>A footnote in a separate file<a epub:type="noteref" id="ref1" href="notes.xhtml#fn1">[1]</a> '
        'and a second one<a epub:type="noteref" id="ref2" href="notes.xhtml#fn2">[2]</a> '
        'should open without losing your place.</p>'
        '<p>A same-file cross-reference: go to <a href="#local-note">the local note</a> and return.</p>'
        '<aside id="local-note"><p>Local note: this is a link target inside the same chapter.</p></aside>',
    ]
    notes = ('<section epub:type="footnotes"><h2>Notes</h2>'
             '<aside epub:type="footnote" id="fn1"><p><a href="chapter-1.xhtml#ref1">1.</a> '
             'First note, stored in its own file as many publishers do.</p></aside>'
             '<aside epub:type="footnote" id="fn2"><p><a href="chapter-1.xhtml#ref2">2.</a> '
             'Second note, placed right after the first with no block between them.</p></aside></section>')
    return ([('chapter-1.xhtml', 'Type Specimen', ''.join(blocks))],
            [('notes.xhtml', 'Notes', notes)])


def build_samples(output: Path) -> None:
    write_epub3(output / 'reading-prose.epub', 'Reading Test — Ordinary Prose',
                'a5527c52-67ee-4339-a6ce-50bdd879a009', prose_chapters())
    chapters, notes = stress_chapters()
    write_epub3(output / 'reading-stress.epub', 'Reading Test — Typography and Layout',
                '354fd5d3-b628-48d0-af28-8670609e0281', chapters, notes)
    write_epub2_ncx(output / 'reading-legacy-ncx.epub', 'Reading Test — Legacy NCX',
                    '6f0c9d1e-3b52-4b8e-9a51-2d7c4e1f0a33', prose_chapters())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', type=Path, default=Path.cwd())
    args = ap.parse_args()
    build_samples(args.output)


if __name__ == '__main__':
    main()
