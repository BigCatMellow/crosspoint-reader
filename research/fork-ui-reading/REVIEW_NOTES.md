# Second-opinion review notes

Date: 2026-11-03. Reviewer: a second AI agent, working alongside the agent already improving this fork.
Requested by bt 7274. Branch: `docs/second-opinion-review`, based on `develop` at `a93303a`.

Purpose of this file: tell bt 7274 and the other agent what was checked, what changed and why, how it was
verified, and what is still open. Nothing here touches firmware, its build, or `src/`/`lib/`.

## 1. Scope

The fork's own work is three commits on top of upstream CrossPoint:

| Commit | Content |
| --- | --- |
| `1e054ed` | `research/fork-ui-reading/` archive, reference headers, licenses, fetch script |
| `8227851` | Decision record, font baseline, EPUB sample generator and tests |
| `a93303a` | `index.html` X4 Pro UI preview and `.nojekyll` at the repo root |

Everything else (about 211k lines of C/C++) is upstream. It was **not** audited in this pass.

## 2. Coordination with the other agent

- Before editing, `git fetch` showed `origin/develop` still at `a93303a` and no other branches. None of the
  findings below had been addressed in pushed work.
- Unpushed local work by the other agent cannot be seen from here. If it edited the same files, expect
  conflicts in `index.html` and `research/fork-ui-reading/tools/`.
- All changes are on a separate branch so `develop` is untouched.

## 3. Changes

### Research tools (`research/fork-ui-reading/tools/`)

| Finding | Change |
| --- | --- |
| `fetch_pinned_sources.py` ran network fetches on import | Added `main()` and `__main__` guard |
| A manifest `path` with `..` could write outside the target folder | `safe_relative()` rejects absolute paths and `..` |
| 9 of 22 entries had `blob_sha: null` and downloaded unchecked | Fetched each at its pinned commit and recorded the SHA (URLs are commit-pinned, so content cannot change). All 22 now verify |
| One failed download aborted the whole run | Per-file errors, summary line, exit code 1 on any failure |
| `downloaded_sources/` was not git-ignored | Added `research/fork-ui-reading/.gitignore` (also ignores generated `samples/` and `*.epub`). Kept local to avoid touching the upstream root `.gitignore` |
| Papyrix and Inx had no archived license | Fetched `LICENSE` at the pinned commits: both MIT. Added `licenses/papyrix-reader-LICENSE` and `licenses/inx-LICENSE` |
| Footnote check used a same-file `<aside>` and a text link | Added `epub:type="noteref"` links (`[1]`, `[2]`) to a separate `notes.xhtml` with two adjacent `epub:type="footnote"` asides. This matches the publisher pattern handled at `lib/Epub/Epub/parsers/ChapterHtmlSlimParser.cpp:1399` and `:2366`. Kept the same-file cross-reference |
| Prose chapters were rotations of the same 6 paragraphs, so lost or repeated text was invisible | Each paragraph starts with a `[chapter.paragraph]` marker |
| No NCX-only book, so `TocNcxParser` was never exercised | Added `reading-legacy-ncx.epub` (EPUB 2.0.1, `toc.ncx`, XHTML 1.1 meta) |
| Output was only deterministic on one OS (`ZipInfo.create_system` differs on Windows) | Fixed `create_system` and file mode |
| Test: `assert spec and spec.loader` ran after `module_from_spec(spec)` | Moved before use |
| Test: mimetype extra field / data-descriptor flag not checked | Added both checks, plus TOC type, noteref targets and marker uniqueness |

### Preview page (`index.html`)

| Finding | Change |
| --- | --- |
| `#readerText` defined five times with conflicting fonts and heights | One rule, in the last `#reader #readerText` block |
| Reader body used Georgia, which is missing on Linux and Android, so pagination differed per viewer | Loads Literata (one of the FONT_BASELINE candidates) from Google Fonts via `--reader-font`, Georgia as fallback |
| Pages were measured before the webfont loaded | Repaginates on `document.fonts.ready` and `loadingdone` |
| Text size was 15-30 px, which matches nothing on the device | Firmware points 8-22 (`src/ReaderFontSizes.h`), default 14 (`src/CrossPointSettings.h:121`), converted at `FONT_RASTER_DPI` 150 (`lib/EpdFont/EpdFontData.h:8`). Label shows `pt` |
| Measure element ignored letter/word spacing, alignment, hyphens, kerning | Copies them from the reader's computed style |
| `contentHeight-28` guard wasted about one line per page | Exact fit. Verified no overflow, below |
| Fixed 144 px settings preview clipped text at the new larger sizes | 200 px, still fixed so controls never move; text top-aligned |
| Font buttons found by matching `onclick` source text | `data-font-step` attributes |
| Dead code: `size()`, `pageSource()` | Removed |

### Docs

- `DECISIONS.md` referred to an "existing scaled-glyph prototype". None exists in this repo; reworded to point at
  the manifest reference.
- `FORK_REVIEW.md` still ranked glyph resampling P0 after `DECISIONS.md` deferred it; marked Deferred.
- `README.md` and `FONT_BASELINE.md` updated for the third book, new checks, licenses and this file.

## 4. Verification

| Check | Result |
| --- | --- |
| `python3 research/fork-ui-reading/tools/test_reading_samples.py` | 7/7 pass |
| EPUBCheck v5.3.0 on all three generated books | 0 fatals, 0 errors, 0 warnings each |
| `python3 research/fork-ui-reading/tools/fetch_pinned_sources.py` | 22/22 fetched, all hashes match |
| Headless Chrome: every point size (15) x line spacing (3) x margin (3) = 135 combinations, every page | No text overflow; every token appears on exactly one page |
| Headless Chrome: both settings screens at 14 pt and 22 pt Relaxed | No control pushed off screen |
| Headless Chrome: navigation, page turns, keyboard, tap zones | No JavaScript errors |

The sandbox could not reach Google Fonts, so the browser checks ran on the fallback serif. Pagination is
measured at runtime, so the same checks should hold with Literata, but this was not observed directly.

To verify by hand: open `index.html`, enter the reader, step through all sizes in quick settings, and check that
no page cuts off a line at the bottom.

## 5. Not changed (needs a decision from bt 7274)

- **`index.html` and `.nojekyll` at the root of `develop`.** These ride along with any rebase onto or PR to
  upstream. GitHub Pages currently serves from here, so moving them (to a `gh-pages` branch or `docs/preview/`)
  needs a Pages settings change at the same time. Not done to avoid breaking the published page.
- **Visual change:** default reader text is now 14 pt (29 px) instead of 21 px. This is what the device shows by
  default, but the preview looks noticeably larger than before.
- **Line spacing and margin buttons** still use preview-only values (1.38/1.58/1.78, 0/10/22 px). Firmware uses
  line-spacing multipliers of the font's own line height (`LINE_SPACING_*` in `src/CrossPointSettings.h`) and
  margins of 5-40 px in steps of 5. Mapping these exactly needs per-font metrics; left as-is.
- **`aliceProgress()`** reports invented percentages. Harmless in a demo.
- **Upstream firmware** was not reviewed. A targeted pass (reader, fonts, web server) can be done on request.

## 6. Repository rules followed

- `AGENTS.md` / `CLAUDE.md`: host-only Python and docs, so no firmware handoff required. No commits or pushes
  without explicit approval; no PR opened.
