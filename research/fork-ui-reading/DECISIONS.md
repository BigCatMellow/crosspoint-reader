# Reading-quality decision record

2026-11-02: prioritize ordinary prose font and layout evidence before adapting scaled-glyph rasterization.

Baseline source already supports TTF/OTF on PSRAM boards, in-book font controls and real text-layout preview. Normal glyph rendering can use grayscale; the separate scaled path uses black/white coverage, primarily affecting small caps, superscripts and subscripts. That is a narrower impact than the user's focus on ordinary body text.

Keep the existing scaled-glyph prototype outside production. No merge, flashing, or new setting now. Revisit only when controlled X4 Pro tests show that the improvement is perceptible with acceptable CPU, battery and memory costs.

The next step is to compare font families with the fixed EPUBs and FONT_BASELINE.md. Improve the existing interface only when actual navigation friction is observed.

Trust in the engineering recommendation is not a waiver of required firmware tests, review, human acceptance, or hardware evaluation. This record and its host-only scripts do not change firmware output.
