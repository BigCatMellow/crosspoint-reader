# X4 Pro fork study — UI and reading improvements

**2026-11-02 evidence:** verified repository source paths, source code and author documentation; performance descriptions are developer-reported or hypotheses, **not** independent device measurements.

| Priority | Fork | Idea | Potential value | Risk | Pinned source |
|---|---|---|---|---|---|
| P0 | CrossInk | Bitter/Lexend fonts; minimalist UI | Type choice and reading clarity | Need same-book real display tests | [Code](https://github.com/uxjulia/CrossInk/blob/9914146eeae7b46b300f475a16c32426fc02ec1f/README.md) |
| P0 | Xerif | Grayscale plane helpers | Sharp, stable antialiasing at small sizes | Verify actual X4 Pro panel/renderer output | [Code](https://github.com/Belphemur/Xerif-eReader/blob/b5cb9d2d16373a7858084f7615f22d0d6b7913fc/lib/GfxRenderer/GrayPlanes.h) |
| Deferred | Witch | Fixed-point glyph resampling | Consistent cached and uncached scaled glyphs | Check edge artifacts and speed. Deferred 2026-11-02, see [DECISIONS.md](DECISIONS.md) | [Code](https://github.com/jpirnay/witchhunt-reader/blob/f6a1019385d6f5be96ee3eebba146b76d00b8272/lib/GfxRenderer/ScaledGlyphResample.h) |
| P0 | Witch | Typography language profile | Better language-aware line breaks and punctuation | Some functionality already exists upstream | [Code](https://github.com/jpirnay/witchhunt-reader/blob/f6a1019385d6f5be96ee3eebba146b76d00b8272/lib/Epub/Epub/TypographyProfile.h) |
| P0 | PapyriX | Knuth-Plass line break layout | Reduce uneven justification and whitespace | Compare performance/memory under ESP32 | [Code](https://github.com/bigbag/papyrix-reader/blob/93425d868c79156b77fcb97a167b490ea3663e87/lib/RenderTypes/src/ParsedText.cpp) |
| P1 | CrossInk | Status bar tap area | Minimal UI with usable touch controls | Avoid accidental page turns | [Code](https://github.com/uxjulia/CrossInk/blob/9914146eeae7b46b300f475a16c32426fc02ec1f/src/activities/reader/ReaderStatusBarTapTarget.h) |
| P1 | Xerif | Quick page relayout | Fast font previews | Preview may differ from final pagination | [Code](https://github.com/Belphemur/Xerif-eReader/blob/b5cb9d2d16373a7858084f7615f22d0d6b7913fc/src/activities/reader/QuickPageRelayout.h) |
| P1 | Xerif | Page turn batching | Fewer redraws after quick consecutive presses | Preserve chapter boundary and progress | [Code](https://github.com/Belphemur/Xerif-eReader/blob/b5cb9d2d16373a7858084f7615f22d0d6b7913fc/src/activities/reader/PageTurnBatch.h) |
| P1 | Witch | Background rendering | Less intrusive indexing between chapters | Memory, lock and power limits | [Code](https://github.com/jpirnay/witchhunt-reader/blob/f6a1019385d6f5be96ee3eebba146b76d00b8272/docs/background-rendering.md) |
| P1 | Inx | In-book menu and presets | Lower navigation friction | Don't duplicate current toolbar | [Code](https://github.com/obijuankenobiii/inx/blob/8c632186da53e3d1b72ae7d5c72d1cf4855eb03f/src/activity/reader/Epub/MenuDrawer.h) |
| P2 | CrossInk | Stable page selection | Reliable scrubbing/navigation | Mainline may be sufficient | [Code](https://github.com/uxjulia/CrossInk/blob/9914146eeae7b46b300f475a16c32426fc02ec1f/src/activities/reader/StablePageSelectionModel.h) |
| P2 | Witch | Small caps | Publisher fidelity where needed | Measure and paint must agree | [Code](https://github.com/jpirnay/witchhunt-reader/blob/f6a1019385d6f5be96ee3eebba146b76d00b8272/lib/EpdFont/SmallCaps.h) |

## Existing CrossPoint source to inspect before anything is ported
- [SD card fonts](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/docs/sd-card-fonts.md) already provide direct TTF/OTF/TTC on external-RAM boards and `.cpfont` on all targets.
- [TextSettingsPreview.cpp](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/src/activities/settings/TextSettingsPreview.cpp) previews the real text layout.
- [ReaderToolbarUi.cpp](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/src/activities/reader/ReaderToolbarUi.cpp) already has a slim bottom sheet and scrub.
- [CjkBreaks.h](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/lib/Epub/Epub/CjkBreaks.h) provides existing multilingual break rules.
- [VectorFontSupport.h](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/lib/EpdFont/VectorFontSupport.h) gates vector font support to PSRAM.
- [SCOPE.md](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/SCOPE.md) prioritizes rendering/typography while freezing new built-in themes.

## Priority sequence
1. Compare a fixed EPUB in **Literata, Bitter, Atkinson Hyperlegible, Lexend Deca and current font**, at matching sizes. Test grayscale/font rendering and book body typography.
2. Study paragraph layout: margins, justification, line wrapping, hyphenation, glyph fidelity and language-specific breaks.
3. Improve clarity of in-book font controls *only when* existing toolbar behavior is deficient.
4. Measure repeated page turns, cold/warm book opens, and chapter transitions.
5. Defer optional small-caps and exotic formatting until core prose is excellent.

**Excluded:** games, flashcards, notes, stats dashboards, clocks, weather, new connectors or broad theme redesign.

Code snapshots are reference only, not a source merge. For all examined files, see [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json).
