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

Status: Round 1 recorded. Round 2 recorded below. No HTML or firmware changed by this record.


## 2026-11-04 — Paper UI feature audit, Round 2: navigation and reading tools

User-approved interface preferences (not firmware implementation approval):

| Feature | Decision | Interpretation / implementation check |
| --- | --- | --- |
| Table of Contents | Keep accessible | Easy to reach on demand; no permanently displayed chapter list. |
| Previous / Next Chapter | Remove | No dedicated skip-chapter controls in Paper UI; preserve normal chapter navigation through Contents. |
| Go to Position | Keep visible | Offer a direct, clear location-jump action when navigation controls are displayed; avoid adding permanent chrome on the reading page. |
| Search Within Book | Keep accessible | Available from a simple reading-tools entry point, not a persistent search field. |
| Dictionary | Keep visible | Direct word lookup affordance during reading; depends on an installed dictionary and input/selection support, to be verified in firmware. |
| Footnotes | Remove | No dedicated Paper UI footnote tool; do not suppress EPUB note links/content or delete underlying reader behavior. |
| Return to Last Position | Keep visible | Direct way to return after a navigation jump; show when a previous position exists. |

Cross-round interpretation: “Keep visible” means straightforward direct access when relevant, not a permanent toolbar over the book. Reading remains full-bleed and distraction-free, per Round 1. Source capability and hardware interaction need checking before implementation.

Audit status: Rounds 1–2 recorded; Round 3 recorded below. The current HTML mockup and firmware remain unchanged by this decision log update.


## 2026-11-04 — Paper UI feature audit, Round 3: library and book management

User-approved interface preferences (not firmware implementation approval):

| Feature | Decision | Interpretation / implementation check |
| --- | --- | --- |
| Continue Reading | Keep visible | Primary Home action; resumes the current book directly. |
| Recently Read Books | Keep accessible | A direct, uncomplicated way to switch books without crowding Home. |
| Library Search | Keep accessible | Reachable in the Library on demand, not a permanent field if it costs reading space. |
| Library Sorting | Keep accessible | Available when needed; avoid taking permanent Library space. |
| Book Covers | Remove | Text-first library with titles and authors; do not render cover thumbnails in Paper UI. |
| Book Details | Remove | No mandatory intermediate details screen between a book in Library and reading. |
| Delete / Remove Books | Remove | No deletion control in custom Paper UI; do not remove existing files or underlying firmware functionality. |
| Collections / Folders | Keep accessible | Offer navigation by existing organization when needed, without making it the default Library view. |

Cross-round implications:
- Selecting a book should open it directly; chapter access remains available through the Table of Contents (Round 2).
- The Home screen must prioritize Continue Reading rather than book metadata or cover art.
- Do not delete underlying book files, metadata, covers, or device capabilities. "Remove" denotes removal from custom UI only.
- The current index.html still contains a Book Details screen and visible Library search/sort; reconcile after the audit rather than treating the existing mockup as final.

Audit status: Rounds 1–3 recorded; Round 4 recorded below. No HTML or firmware changed by this decision log update.


## 2026-11-04 — Paper UI feature audit, Round 4: typography and page layout

User-approved interface preferences (not firmware implementation approval):

| Feature | Decision | Interpretation / implementation check |
| --- | --- | --- |
| Font Selection | Keep visible | Direct choice in Reading Settings, showing current font. Installed font availability must be checked against firmware and device storage. |
| Text Size | Keep visible | Direct increase/decrease with the current value; update reading layout. |
| Line Spacing | Keep visible | Direct choices, with selected setting clearly indicated. |
| Page Margins | Keep visible | Direct choices, with selected setting clearly indicated. |
| Text Alignment | Keep accessible | Access on demand without occupying permanent Reading Settings space. |
| Hyphenation | Keep accessible | Access on demand; preserve the reading engine's existing behavior. |
| Paragraph Spacing / Indentation | Keep visible | Direct reading-layout control where firmware support exists; verify whether spacing and indentation are independently adjustable before implementing. |
| Reading Presets | Keep visible | Easy selection of stored combinations; verify current firmware support and avoid implying saved presets exist if custom storage must be added. |

Cross-round interpretation: These visible typography controls belong on the Reading Settings screen, not as permanent overlays on the book page. Avoid stacking extra screens and menus; prioritize legible, bounded settings layout for the X4 Pro. Presets and paragraph controls may require engineering work beyond the existing mockup; no implementation promises or new feature scope are granted by the audit.

Audit status: Rounds 1–4 recorded. Round 5 (display, lighting, and screen behavior) awaiting user decisions. No HTML or firmware changed by this decision log update.
