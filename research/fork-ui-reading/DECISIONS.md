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

Audit status: Rounds 1–4 recorded; Round 5 recorded below. No HTML or firmware changed by this decision log update.


## 2026-11-04 — Paper UI feature audit, Round 5: display, lighting, screen behavior

User-approved interface preferences (not firmware implementation approval):

| Feature | Decision | Interpretation / implementation check |
| --- | --- | --- |
| Frontlight Brightness | Keep visible | Direct lighting adjustment from an appropriate display control surface; do not permanently overlay the book. Verify device range and native firmware support. |
| Warm Light / Color Temperature | Keep visible | Direct color-temperature adjustment when X4 Pro hardware/firmware supports it; avoid suggesting a functional control on unsupported targets. |
| Dark Mode | Keep accessible | Available on demand; not a permanent reading-page control. |
| Screen Refresh Controls | Keep accessible | Refresh frequency / ghosting options available in display settings. |
| Manual Screen Refresh | Keep accessible | Trigger refresh on demand, without a permanent reading-page button. |
| Screen Orientation | Keep visible | Direct manual portrait/landscape control when relevant; earlier automatic-orientation preference remains subject to sensor/firmware verification. |
| Sleep Screen Customization | Keep accessible | Rarely used configuration, available outside reading surface. |
| Battery Percentage | Keep visible | Show in stable UI chrome such as Home / open toolbar; avoid constant overlays on text. |

Cross-round interpretation: “Keep visible” means obvious at the relevant moment or in the appropriate controls, not necessarily always rendered over the book. Lighting and orientation need actual X4 Pro capability checks before implementing controls. This audit does not authorize firmware modifications, flashing, or deleting existing features.

Audit status: Rounds 1–5 recorded; Round 6 recorded below. No HTML or firmware changed by this decision log update.


## 2026-11-04 — Paper UI feature audit, Round 6: device, connectivity, and transfers

User-approved interface preferences (not firmware implementation approval):

| Feature | Decision | Interpretation / implementation check |
| --- | --- | --- |
| Physical Button Customization | Keep accessible | Reachable in device settings; never compromise default physical page turning. |
| Disable Touch Page Turning | Keep visible | Direct on/off control for page-turn taps; other necessary touch interactions remain usable. Requires separate tap-zone routing verification. |
| Bluetooth Page Turners | Remove | No dedicated controls in Paper UI; do not remove firmware-level Bluetooth functionality. |
| USB Book Transfer | Keep visible | Clear transfer entry point and state/instructions when relevant; do not imply transfer works without host/device support. |
| Wireless Book Transfer | Keep visible | Clear Wi-Fi transfer action and connection information, subject to current firmware capabilities. |
| Online Book Catalogs (OPDS) | Keep accessible | Secondary book acquisition tool, not part of the default Home screen. |
| Reading Progress Sync | Remove | No sync controls in Paper UI; preserve underlying firmware implementation and any existing data. |
| Wi-Fi and Bluetooth Controls | Keep visible | Direct connectivity status and on/off or connection controls in a relevant device screen; no permanent overlay during reading. |
| Quick Resume / Sleep Behavior | Keep visible | Make resume-to-current-book behavior immediate; expose sleep behavior where relevant without cluttering reading. |

Cross-round interpretation: preserve a clean reading page, but keep transfer, connectivity, lighting, text settings, and touch page-turn behavior easy to access from appropriate direct surfaces. Where “keep visible” refers to an interaction rather than a button (such as quick resume), it means obvious behavior without extra steps. Hardware/firmware feasibility of touch-zone separation, USB, Wi-Fi transfer, and sleep behaviors must be verified before implementation.

Audit status: All six preference rounds recorded. Final integrated feature review follows separately; no HTML or firmware changed by this decision log update.

## 2026-11-04 — Integrated feature review (design proposal, not approved implementation)

### Screen model
1. **Home:** current book and large Continue Reading action, Library, Settings. Recently read books accessible without taking over Home. Battery shown in stable chrome.
2. **Reading:** text dominates; physical buttons and touch page-turning. No permanent toolbar, page numbers, covers, or status overlays. A simple temporary control surface provides Table of Contents, Go to Position, search, dictionary, previous location, reading progress/chapter, and settings as appropriate. Avoid persisting controls over prose.
3. **Library:** text-based title/author entries open books directly, no Book Details screen. Search, sort, recent, and collections/folders are available on demand.
4. **Reading Settings:** directly expose font, size, line spacing, margins, paragraph formatting, and presets, with alignment/hyphenation on demand. Font and preset availability must be implemented/verified; do not display simulated functionality as native.
5. **Display & Device:** direct brightness, warmth, orientation, battery, touch-page-turn disable, connections, transfer, and quick resume/sleep. Rare functions such as refresh cadence, manual refresh, dark mode, sleep screens, button remapping, and OPDS stay accessible without extra reading-page chrome.

### Existing preview conflicts to resolve
- Remove Bookmark action, Book Details step, cover presentation, and dedicated skip-chapter controls from custom UI.
- Search and sorting are currently always shown in the Library preview; relocate to accessible on-demand controls.
- Current Go To / Text tools should remain straightforward; Dictionary and Return to Last Position are desired direct actions but must be verified for real firmware integration.
- Implement touch-page-turn disable without losing tap-to-open toolbar, dictionary selection, or necessary controls.
- The old seven-screen native Paper plan includes a mandatory new Book Details screen and should not be treated as current design approval.

### Feasibility and review gates
- **Confirm in source/device:** automatic rotation detection, warm-light support, font installation and selection, dictionary selection and installed-data path, transfer modes, wake/quick resume, and independent paragraph formatting.
- **Potential new implementation:** saved reading presets and a touch-page-turn-only disable switch, if unsupported by upstream.
- **Acceptance checks:** no feature crowds reading page; book opens from Library in one action; Continue Reading resumes in one action; settings visibly reflect the actual values; disabled controls are honest; touch/physical button behavior and ebook contents remain intact.
- Preserve firmware capabilities, saved settings, file data, and EPUB semantics even for controls removed from Paper UI. No flash, merge, or source change is authorized merely by preference approval.

Review status: design synthesis recorded; behavior and native capability verification pending. HTML mockup remains an older prototype until separately updated.
