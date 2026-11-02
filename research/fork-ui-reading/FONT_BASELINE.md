# X4 Pro typography comparison baseline

Status: controlled comparison plan, not a verified choice of best font. No firmware changes or flashing.

## Goal
Prioritize normal text clarity and comfort, paragraph spacing, faithful italic/bold and punctuation, and simple in-book adjustments. Defer the proposed scaled-glyph rendering change until actual X4 Pro evidence supports it.

## Test files
Run the dependency-free generator:
    python3 research/fork-ui-reading/tools/make_reading_samples.py --output ./samples

Two original, font-neutral EPUBs will be produced:
- reading-prose.epub: three chapters of plain sustained prose for line wrapping, reading density, page turns and chapter boundaries.
- reading-stress.epub: easily confused letters (I/l/1, O/0, rn/m), accent marks, quotes, dashes, italics/bold, long words, lists, a table and a local footnote-style link.

Run host checks:
    python3 research/fork-ui-reading/tools/test_reading_samples.py

The tests check ZIP mimetype placement/compression, XML syntax, manifest/spine references, no bundled fonts/images and deterministic output. They DO NOT prove the X4 Pro renders these books correctly.

## Use what CrossPoint already supports
- Direct TTF/OTF/TTC loading on boards with external RAM, including X4 Pro. Copy permitted fonts into /fonts/ or /.fonts/ on the microSD. Use separate variants in a family folder; don't mix cpfont and TTF files (cpfont takes precedence).
- Actual code in src/ReaderFontSizes.h provides vector font sizes 8–22 pt and built-in sizes 12,14,16,18; compare at 14 pt initially, then 16 pt.
- The current reader already has an in-book toolbar and a real text-layout settings preview.
- No unlicensed third-party font files are included.

## One-variable-at-a-time A/B procedure
1. Record current font, 14 pt size, line spacing, margins, alignment, antialiasing, and orientation without resetting any other preference.
2. Compare baseline font with Literata, Bitter, Atkinson Hyperlegible, and Lexend Deca at the same 14 pt and other settings. These are candidates, not proven winners.
3. Read multiple pages of reading-prose.epub per font, not just the title page. Look for stroke weight, spacing consistency, confusion between similar letters and reading fatigue.
4. Take the two best to 16 pt and then adjust one layout variable per pass: justified versus left; line spacing; margins.
5. Use reading-stress.epub to examine bold/italic fidelity, unusual characters, table overflow and bad word breaks.
6. Verify physical page buttons, one-handed touch targets, chapter crossing, sleep/wake and saved progress. A pretty page that breaks navigation loses.

Do not use desktop screenshots or a browser simulator as a substitute for real e-ink screen refresh, ghosting, battery or speed measurements.

## Blank result grid
| Font (14 pt) | Clarity 1–5 | Prose comfort 1–5 | Spacing 1–5 | Italic/bold correct? | Missing glyphs? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Current | — | — | — | Untested | Unknown | |
| Literata | — | — | — | Untested | Unknown | |
| Bitter | — | — | — | Untested | Unknown | |
| Atkinson Hyperlegible | — | — | — | Untested | Unknown | |
| Lexend Deca | — | — | — | Untested | Unknown | |

## Decision
Prefer the font that reads comfortably over an extended session while preserving emphasis and fidelity. Only then tune line height and margins. Avoid extra settings or a replacement font engine without demonstrating a real deficiency.

Host test books checked with Python 3.13. Firmware builds and X4 Pro tests NOT run.
