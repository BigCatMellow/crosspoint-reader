# Paper UI: porting the X4 Pro preview to firmware

Status: plan, no firmware code yet. Branch `feat/x4pro-paper-ui`, based on `develop` at `a93303a`.
Requested by bt 7274 on 2026-11-03.

## Decisions (from bt 7274)

| Question | Decision |
| --- | --- |
| Replace or add? | New theme, **Paper**, made the default on X4 Pro. Existing themes stay as fallback. |
| Scope | All 7 preview screens in one pass. |
| Builds | Run `pio run -e x4pro` on bt 7274's computer through the linked Claude desktop app. The cloud sandbox cannot reach the PlatformIO registry. |
| UI font | Built-in firmware UI font. Inter is not used on the device. |

Known conflicts, accepted by bt 7274: `SCOPE.md` freezes new themes upstream, and `DESIGN_BRIEF.md` lists new
themes as a non-goal for the research pass. This work stays on the fork and will not be offered upstream as-is.

## Precedent

`COVER_GRID` already does what Paper needs: an enum value in `CrossPointSettings::UI_THEME`
(`src/CrossPointSettings.h:205`), Lyra chrome for shared screens (`src/components/UITheme.cpp:48`), and its own
home screen through `UITheme::hasCoverGridHome()` and `CoverGridHomeUi` (a `UiAppHost`), created in
`HomeActivity::onEnter()` (`src/activities/home/HomeActivity.cpp:239`). Paper follows the same path.

## Screen map

| Preview screen | Firmware owner | Work |
| --- | --- | --- |
| Shared look: square corners, 1 px rules, bold titles, boxed back button, battery top right | New `PaperTheme : BaseTheme` + `PaperMetrics` in `src/components/themes/paper/` | Metrics table and overrides for `drawHeader`, `drawButtonMenu`, list styling. Applies to every list/settings screen for free |
| Home: current-book hero (title, author, chapter, progress, Continue Reading) + Library / Settings footer | New `PaperHomeUi : UiAppHost`, hooked like `CoverGridHomeUi` | Uses `RecentBooksStore` data HomeActivity already loads |
| Library: 4 large cards per page | `LibraryListActivity` with Paper list metrics | Row height and paging from metrics; check `rowProvider` path stays allocation-free |
| Book detail: current-place card + chapters card | **New screen** (does not exist today) | Small `UiAppHost` between library and reader; needs progress and TOC title from the book cache. Biggest design risk |
| Chapters | `EpubReaderChapterSelectionActivity` | Styling via theme; "current chapter" subtitle |
| Reader: full-bleed text, tap left/right = page, center = chrome; chrome = top bar (back, chapter, settings) + bottom bar | `EpubReaderActivity` + `ReaderToolbarUi` | Reuse existing tap routing and toolbar owner; restyle, no new gesture handler (`ui-activities.md`: one gesture, one owner) |
| Quick settings: preview, size −/+, 3 line-spacing, 3 margin options | `ReaderToolbarUi` sheet + `TextSettingsPreview` | Map to real settings: `fontPointSize` (8–22 on PSRAM), `lineSpacing` (`LINE_SPACING_*`), `screenMargin` (5–40 step 5). Preview's 3 choices pick from those |
| Settings menu | `SettingsActivity` | Theme styling only |

## Other changes

- `CrossPointSettings`: add `PAPER = 5`; default `uiTheme` to `PAPER` when `FREEINK_DEVICE_X4PRO` is defined.
  Settings file stores the number, so adding at the end keeps existing values valid.
- `SettingsList.h:254`: add `STR_THEME_PAPER`. Translation strings go through the repo's translation workflow
  (`.agents/rules/generated-files-cache.md#translation-workflow`); English first, other languages fall back.
- Any strings in new screens ("Current place", "Continue reading", "Chapters") get `StrId`s, no literals.

## Memory and rules

- New UI hosts hold props and interaction tables as members (as `CoverGridHomeUi` does), allocated with
  `makeUniqueNoThrow` in `onEnter()`, freed in `onExit()`. Steady-state repaint must not allocate.
- Paper is X4 Pro first. On boards without touch the same screens must still work by buttons, or Paper falls back
  to Lyra the way `COVER_GRID` falls back without PSRAM.
- Firmware change, so `.agents/skills/firmware-handoff` applies before any commit: build, four reviews,
  bt 7274's hardware test.

## Order of work

1. Theme enum, setting, string, `PaperTheme` metrics + header/list drawing. Build.
2. `PaperHomeUi`. Build.
3. Library card metrics, chapters styling, settings styling. Build.
4. Reader chrome restyle and quick-settings sheet mapped to real settings. Build.
5. Book detail screen and its navigation (library → book → reader/chapters). Build.
6. Handoff reviews; device test list for bt 7274.

## Device test list (to fill as screens land)

- Every screen by touch and by buttons, with button remapping, in portrait.
- Reader: tap zones, chrome show/hide, page turn while chrome is open, chapter crossing, sleep/wake keeps place.
- Quick settings: each size/spacing/margin choice reflows the book and survives reboot.
- Switching theme back to Lyra restores the old UI.
