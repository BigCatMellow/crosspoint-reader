# Handoff to the build-capable agent

From: second-opinion agent (cloud sandbox, cannot compile firmware). Date: 2026-11-03.
Owner: bt 7274. Read this, then [PAPER_UI_PLAN.md](PAPER_UI_PLAN.md).

## Ground rules (from AGENTS.md, still apply)

- No commit without bt 7274's approval; no push without an explicit push instruction; never open a PR.
- Every firmware change goes through `.agents/skills/firmware-handoff` before it is called ready.
- Hardware testing is bt 7274's. Give a device test list with each step.

## 0. Sync first

Two branches exist on `origin` besides `develop` (`a93303a`):

| Branch | Content | Action |
| --- | --- | --- |
| `docs/second-opinion-review` | Research tool fixes, preview `index.html` fixes, `REVIEW_NOTES.md` | Read `research/fork-ui-reading/REVIEW_NOTES.md`. If you changed the same files locally, merge or tell bt 7274 about conflicts |
| `feat/x4pro-paper-ui` | This file and the Paper UI plan. No code | Base the Paper work here |

## 1. Confirm the build

```bash
git fetch origin && git checkout feat/x4pro-paper-ui
git submodule update --init freeink-sdk
pio run -e x4pro
```

Report: pass/fail, flash and RAM use from the build summary. These are the baseline for later steps.

## 2. Step 1 of the plan: Paper theme skeleton

Goal: a selectable "Paper" theme that builds and draws the shared chrome (headers, lists, menus) in the preview's
style. No new screens yet.

| File | Change |
| --- | --- |
| `src/CrossPointSettings.h:205` | Add `PAPER = 5` at the end of `UI_THEME`. Never reorder: the settings file stores the number |
| `src/CrossPointSettings.h:355` | Default `uiTheme` to `PAPER` under `#ifdef FREEINK_DEVICE_X4PRO`, else keep `LYRA` |
| `lib/I18n/translations/english.yaml` | Add `STR_THEME_PAPER: "Paper"`, then run `python3 scripts/gen_i18n.py lib/I18n/translations lib/I18n/` |
| `src/SettingsList.h:252` `homeThemeValues()` | **Trap:** it hides Cover Grid by dropping the last entry (`size - 1`). Appending Paper would hide Paper instead. Index the values by enum so Paper always shows and only `COVER_GRID` is filtered. Check how the Enum setting maps menu position to stored value before changing |
| `src/components/themes/paper/PaperTheme.{h,cpp}` | New. `class PaperTheme : public BaseTheme` plus `namespace PaperMetrics { values }`. Copy `LyraMetrics` (`src/components/themes/lyra/LyraTheme.h:8`) as the start |
| `src/components/UITheme.cpp` `setTheme()` | Add `case PAPER:` with `makeUniqueNoThrow<PaperTheme>()`, same OOM handling as the Lyra case |

Paper metrics, taken from `index.html` (480x800 layout):

| Element | Preview value |
| --- | --- |
| Corners | Square everywhere: `controlRadius`, `sheetRadius`, `capsuleRadius`, `listRowRadius`, `popupCornerRadius` = 0 |
| Header | ~46-52 px band, 1 px bottom rule, bold title left, battery icon + % right |
| Back button | Boxed (1 px border), left of title |
| List rows | 82 px cards, 1 px border, 10 px gap, bold title + regular meta line |
| Selection | Inverted fill (black background, paper text) |
| Footer nav | Two equal cells split by a 1 px rule (Library / Settings), icon + bold label |
| Colors | Black ink on paper; no gray fills except the disabled state |

Deliverable for step 1: build passes on `x4pro` and the non-PSRAM X3/X4 env (`pio run -e default`), Theme setting shows Paper on both, switching between Paper and Lyra works.
Photos of the Settings and Library lists on device from bt 7274.

## 3. After step 1

Continue with the order in `PAPER_UI_PLAN.md` (home, lists, reader chrome and quick settings, book detail).
Update the "Device test list" section of the plan as each screen lands, and add a short entry per step to
`REVIEW_NOTES.md`-style notes so the next agent can pick up.

## Open questions for bt 7274 (do not guess)

- Book detail screen does not exist in firmware. Confirm it is wanted, or have the library open the book directly.
- Paper on boards without touch: keep it button-only, or hide it there like Cover Grid without PSRAM?
