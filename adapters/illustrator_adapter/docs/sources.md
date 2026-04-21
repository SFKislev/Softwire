# Sources

## api-index.txt

**Extraction date:** 2026-04-21

**Method:** Mechanical — parsed from TypeScript definitions using `tools/extract_api_index.py`

**Primary upstream source:**

- https://github.com/docsforadobe/Types-for-Adobe/blob/master/Illustrator/2022/index.d.ts
  - File: `Illustrator/2022/index.d.ts`
  - Size: ~206 KB, 12,028 lines
  - Generated from Adobe's ESTK scripting dictionary XML (not hand-authored)
  - Covers Illustrator 2022 (version 26.x)

**Live Effects note:**

The `.d.ts` types `applyEffect(liveEffectXML: string): void` but does not enumerate valid
effect name strings — these are runtime-only and version/locale-specific. The index instructs
agents to call `app.liveEffectsList` at runtime to discover valid names rather than guessing.
No structured authoritative source for effect name strings exists.

**Symbol counts (this extraction):**

| Kind | Count |
|------|-------|
| CLASS | 140 |
| ENUM | 733 |
| PROPERTY | 1217 |
| METHOD | 311 |
| LIVEEFFECT | 3 (runtime discovery + application symbols) |
| INTENT_EFFECT | 14 (natural-language aliases for live effects) |
| **TOTAL** | **2430** |

**Extraction script:**

`adapters/illustrator_adapter/tools/extract_api_index.py`

Parses `declare enum`, `declare class`, properties, and methods from the `.d.ts`.
Run with:

```
python adapters/illustrator_adapter/tools/extract_api_index.py \
  /path/to/Illustrator/2022/index.d.ts \
  adapters/illustrator_adapter/docs/api-index.txt
```

**To update:**

1. Download the latest `index.d.ts` from `docsforadobe/Types-for-Adobe`
2. Re-run the extraction script
3. Re-append the LIVEEFFECT section from the bottom of the current `api-index.txt`
4. Update extraction date and counts here

**Notes:**

- The `.d.ts` is community-generated from Adobe's ESTK XML dictionaries — not hand-authored prose
- It does not cover the Live Effects XML string system (applyEffect parameters)
- No official AdobeDocs GitHub repo exists for Illustrator (unlike InDesign's `AdobeDocs/indesign-18-dom`)
- The 2022 version of the types is the most complete available; Adobe has not published updates
