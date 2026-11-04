# Reading-quality decision record

2026-11-02: prioritize ordinary prose font and layout evidence before adapting scaled-glyph rasterization.

Baseline source already supports TTF/OTF on PSRAM boards, in-book font controls and real text-layout preview. Normal glyph rendering can use grayscale; the separate scaled path uses black/white coverage, primarily affecting small caps, superscripts and subscripts. That is a narrower impact than the user's focus on ordinary body text.

Keep the existing scaled-glyph prototype outside production. No merge, flashing, or new setting now. Revisit only when controlled X4 Pro tests show that the improvement is perceptible with acceptable CPU, battery and memory costs.

The next step is to compare font families with the fixed EPUBs and FONT_BASELINE.md. Improve the existing interface only when actual navigation friction is observed.

Trust in the engineering recommendation is not a waiver of required firmware tests, review, human acceptance, or hardware evaluation. This record and its host-only scripts do not change firmware output.


## 2026-11-04 — Paper UI feature audit, Round 1: reading experience

User-approved interface preferences (not a firmware implementation approval):

| Feature | Decision | Interpretation / implementation check |
| --- | --- | --- |
| Physical page buttons | Keep visible | Primary, obvious way to turn pages; physical controls already exist, no need to duplicate on-screen. |
| Touchscreen page turning | Keep visible | Direct tap-to-turn interaction on the reading page. |
| Reading progress | Keep accessible | Not permanently shown while reading; available through reading controls. |
| Chapter information | Keep accessible | Not permanently shown while reading; accessible through reading controls. |
| Reading toolbar | Keep accessible | Hidden during normal reading; easily invoked, without nested navigation. |
| Bookmarks | Remove | Do not expose bookmark controls in the custom Paper UI. Do not delete the underlying firmware capability or saved bookmark data. |
| Automatic page orientation | Keep visible | Desired automatic behavior rather than an extra on-screen control; verify X4 Pro orientation-detection support before promising automation. |

Guiding outcome: reading text dominates; common interactions feel immediate and obvious, without persistent chrome. The newer HTML mockup currently shows a bookmark action and will need reconciliation after the full feature audit.

Status: Round 1 recorded. Round 2 (navigation and reading tools) awaiting user decisions. No HTML or firmware changed by this record.
