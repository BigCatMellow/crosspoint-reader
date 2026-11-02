# X4 Pro reading quality and clean UI: fork research archive

**Research/reference only — no runtime or firmware changes.** Checked 2026-11-02 against [the target `develop` branch](https://github.com/BigCatMellow/crosspoint-reader/tree/e8299b5f126817282939059d6505f90429489276). The Xteink X4 Pro is the main interest. Do not assume X4 Pro features are compatible with ESP32-C3 hardware.

The archive preserves:
- [FORK_REVIEW.md](FORK_REVIEW.md) — ranked, sourced findings and integration risks.
- [DESIGN_BRIEF.md](DESIGN_BRIEF.md) — book-first UI and reading-quality guidelines.
- [QUALITY_TEST_PLAN.md](QUALITY_TEST_PLAN.md) — hardware validation criteria, **not executed**.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) — 22 exact, commit-pinned fork source links.
- [reference_code/](reference_code/) — five unmodified MIT-licensed C++ headers isolated from the firmware build.
- [licenses/](licenses/) — upstream MIT copyright and license notices.
- [tools/fetch_pinned_sources.py](tools/fetch_pinned_sources.py) — optional fetcher for the other pinned references.

**Goal:** strong typography, faithful EPUB rendering, comfortable paragraph rhythm, fast page turning and quiet menus. No games, notes apps, stats dashboards, weather, clocks, new sync engines, or decorative theme expansion.

**Existing CrossPoint work comes first:** direct TTF/OTF/TTC fonts on PSRAM boards (including X4 Pro), SD fonts, reader toolbar, real-layout text settings preview, and CJK text support already exist. Compare with those before importing any solution. See [SCOPE.md](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/SCOPE.md) and [AGENTS.md](https://github.com/BigCatMellow/crosspoint-reader/blob/e8299b5f126817282939059d6505f90429489276/AGENTS.md). Mainline freezes new built-in themes.

No borrowed code is compiled; no fonts or images are bundled. The source snapshots are not tested or approved for production use. Any future firmware change must follow repo review and hardware handoff rules.
