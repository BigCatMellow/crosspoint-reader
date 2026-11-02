# Future verification checklist — no hardware tests performed

Use a fixed EPUB test set with plain prose, italics/bold, chapter boundaries, long words, punctuation/diacritics, code, lists, tables, images, footnotes and multilingual samples where supported. Compare at the same display brightness, orientation, page region and camera exposure.

### Legibility
- Font family and size (12/14/16/18pt or closest supported); check ink weight, line density, letter distinctions and italic quality.
- 1-bit vs 2-bit glyph output and gray edges; screenshot/photo small text and after repeated refreshes.
- Ragged-right versus justified paragraph spacing; hyphenation, awkward breaks and consistent margins.
- Test font switching, text relayout and whether the current paragraph remains stable.

### Interaction
- Number of steps to change type settings; physical button page-turn response and repeated presses.
- Touch target collisions, font quick previews, chapter boundary and end-of-book behavior.
- Cold/warm open and wake/resume persistence; no lost reading progress.

### Engineering
- Compare latest mainline before planning changes; reuse existing font, toolbar and pagination interfaces.
- Record X4 Pro PSRAM/heap, frame buffers, CPU latency, SD reads/writes, battery and refresh artifacts.
- Check compatibility with ESP32-C3 baseline if changes are intended to stay portable.
- Tests plus review and firmware-handoff per repository AGENTS.md for any future compiled change.

**No builds, tests, flashing, measurements or firmware modifications occurred as part of this archive.**
