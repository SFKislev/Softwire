# API Index Strategy

## Goal

Create compact, local, grep-friendly API indexes for each supported adapter so agents can search real class, enum, method, and property names before guessing.

This is not a full documentation mirror. The target is a symbol index (as full as possible) that improves speed and reduces hallucinated API calls.

## Target Output

For each adapter, prefer a structure like:

```text
adapters/<app>_adapter/docs/
  api-index.txt
  sources.md
```

### `api-index.txt`

A flat or lightly structured symbol list containing only high-value API surface:

- classes / objects
- enums / constants
- important methods
- important properties
- optional short descriptions if they stay compact

This file should be optimized for `rg`, not for narrative reading.

### `sources.md`

For provenance and maintenance, record:

- upstream source URLs
- extraction date
- what was extracted
- any cleanup or normalization rules used

## What To Extract

Extract symbol surfaces, not full prose.

Good:

- class names
- enum names
- constant names
- method names
- property names
- short signatures

Avoid:

- tutorials
- cookbooks
- installation guides
- long conceptual explanations
- large example dumps

## Preferred Source Pattern

Best case:

1. a page that already lists all classes or objects
2. a page that already lists all enums or constants

Examples:

- Photoshop-style class/enumeration reference indexes
- Illustrator object reference and scripting constants pages

Harder case:

- APIs like InDesign where the docs are split into many per-class pages
- in those cases, crawl the structured API pages and emit a normalized compact
  index

## Normalization Rules

Keep the output consistent across adapters.

- use plain UTF-8 text or simple Markdown
- prefer one symbol per line when possible
- group by section: `Classes`, `Enums`, `Methods`, `Properties`
- remove duplicate symbols
- strip navigation noise and unrelated site chrome
- keep descriptions short

## Quality Bar

The output is good if an agent can grep for user intent words like:

- `shadow`
- `resize`
- `crop`
- `blur`
- `save`
- `export`
- `text`
- `layer`

and quickly discover likely real API names instead of inventing them.

## Constraints

- Do not dump full documentation sets into the repo.
- Do not add large prose mirrors.
- Keep package size reasonable.
- Prefer extracted symbol indexes over copied manuals.
- Be careful about source licensing and redistribution; keep `sources.md`
  explicit.

## Suggested Work Split

Each adapter task should produce:

1. `docs/api-index.txt`
2. `docs/sources.md`

Recommended order:

1. find the best upstream symbol/index sources
2. extract a raw symbol list
3. clean and normalize it
4. record provenance in `sources.md`

## First Candidates

Start with adapters where compact reference indexes already exist:

- Photoshop
- Illustrator
- InDesign

These are likely to produce the highest improvement per unit of effort.
