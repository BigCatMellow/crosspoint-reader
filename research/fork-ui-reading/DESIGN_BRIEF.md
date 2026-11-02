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
