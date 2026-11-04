# Reading-first design brief

The device should feel like a **book**: simple, clean, immediately understandable, not childlike. Typography and legibility take priority over visual tricks.

## Reading page
- Text dominates; status/progress chrome stays subtle and optional.
- Compare Literata, Bitter, Lexend Deca, Atkinson Hyperlegible and the current default font on **the same EPUB**. Do not declare a universal winner from a font's marketing.
- Assess letter shapes, contrast, weights, italics, punctuation, diacritics, fallback glyphs, anti-aliasing, hyphenation, line spacing, paragraph indentation and margins *together*.
- Prevent ugly justified gaps, lost words, drifting layout versus paint, frequent flashes and ghosting.
- Honor images, tables, chapter headings and footnotes when supplied by a book.

## Quiet interface
- Physical page buttons and one-handed operation remain first class.
- Font/size/line height/margins/alignment should be easy to adjust **without leaving the book**. Prefer extending existing simple UI rather than duplicating screens.
- Adequate invisible touch zones; consistent settings hierarchy, few visual decorations.
- Show loading feedback for slow font fetch/reflow, but not on every tap.
- Optional presets only if they genuinely reduce the number of interactions.

## Non-goals for this pass
New firmware UI themes, network services, games, clocks, Pomodoro tools, study systems, or reading statistics dashboards. This is a research/design reference, not implementation approval.


## 2026-11-04 — AI Design Bible application to Paper UI preview

Source: `BigCatMellow/Pilot_Projects/ai-design-bible` (`main`), especially `FOUNDATIONS.md`, `INTERACTION-AND-INFORMATION.md`, `VISUAL-SYSTEMS.md`, `ACCESSIBILITY.md`, `ANTI-PATTERNS.md`, and `EVALUATION.md`. These are advisory: CrossPoint requirements, the six feature-audit rounds in `DECISIONS.md`, hardware limits, and firmware rules remain authoritative.

Adopted principles:
- **Task hierarchy over uniform decoration:** Continue Reading dominates Home; text title/author entries dominate Library; actual book text dominates Reader. Remove unnecessary enclosing borders and stacked cards; use simple rules, spacing, and typography.
- **Progressive disclosure without hidden mysteries:** keep search and sorting on demand, and keep a single predictable reading-controls reveal. Actions needed for normal reading should not require memorized gestures.
- **One adjustment surface:** Reading Settings puts presets and font before size/spacing/margins, shows the actual selected option, and uses readable short labels. In-book quick settings and Settings entry should describe the same values, not drift.
- **State and feedback are functional requirements:** selected/disabled/focus states must be distinguishable in monochrome. Simulated dictionary, transfer, orientation, and lighting behavior must be identified as prototypes until implemented in firmware.
- **Hardware-first review:** validate 480 x 800 e-ink density, text reflow, tap and button inputs, legibility, long titles, orientation, and e-ink refresh costs on the actual X4 Pro before treating a preview as production-ready.
- **No artificial feature growth:** do not import dashboards, icons, animations, themes, or extra screens from the general-purpose Design Bible merely to satisfy a checklist.

Preview implementation on `feat/x4pro-paper-ui/index.html`:
- reduced home card framing and Library row boxes
- changed Settings navigation into a clear, border-light task list
- regrouped Reading Settings with clear section heading, preset first, font next, compact rows, and a live typographic preview
- improved keyboard focus states, library disclosure state, search labeling, and semantic availability cues

Verification: JavaScript syntax parsed successfully; static tag-balance checks passed for major HTML elements; structural checks confirmed the reading headings, reader focus target, disclosure states, removed Book Details, and removed bookmark action. This is **not** a browser interaction or X4 Pro hardware test. Native firmware remains unchanged.

Next evaluation: perform interaction and layout smoke tests in a browser at device dimensions, then compare side by side on the actual reader before porting. In particular inspect control visibility, scroll behavior in Reading Settings, dynamic font/preset selection, physical button equivalence, and touch page-turn disable without disabling toolbar access.
