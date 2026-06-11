---
name: sync-wb-nb
description: "Propagate a change made in a Wolfbook .wb notebook into the paired .nb notebook so the two stay identical. Use immediately after every .wb edit."
---

# sync-wb-nb

Propagate `.wb` edits into the paired `.nb` so the two stay identical. We edit/test in the
`.wb` (Wolfbook MCP); the `.nb` is the mirror we cannot run. Direction is always
`.wb` → `.nb` (the `.wb` is authoritative; `/nb-to-wolfbook` handles the initial reverse
conversion).

## When to invoke
**Always, immediately after editing or adding cells in any `.wb`.** Add to your CLAUDE.md:
> Always run `/sync-wb-nb` immediately after editing or adding cells in any `.wb`.

## Method: run the committed helper script

All the logic (backup, box conversion, stability gate, unique-target assertions,
post-write verification with automatic restore) lives in `sync-wb-nb.wls` in this skill's
directory. One Bash call per operation:

```bash
WLS=".claude/skills/sync-wb-nb/sync-wb-nb.wls"   # path from project root
wolframscript -file "$WLS" stability "<snippet>"            # is the .wb cell box-stable?
wolframscript -file "$WLS" replace   "<wbSnippet>" ["<nbOldSnippet>"]   # sync an edited cell
wolframscript -file "$WLS" insert    "<wbSnippet>" "<nbAnchorSnippet>"  # sync a new cell
wolframscript -file "$WLS" verify    "<snippet>"            # check a cell is in sync
```

- `<snippet>` selects the cell and **must be a single token** (a symbol name defined in the
  cell, e.g. `"myFunction"`): in box structures `myFunc[x_` never matches — `myFunc`, `[`,
  `x_` are separate strings.
- `replace` takes a second snippet when the OLD `.nb` cell doesn't contain the new token
  (e.g. new code introduces `newSymbol`; locate the old cell by one of its own existing tokens).
- `insert` needs a snippet of the `.nb` cell the new cell goes AFTER.
- Non-default notebook pair: append `<wbPath> <nbPath>` (absolute paths) as trailing args.
  Set defaults in `sync-wb-nb.wls` (see the `defaultWb`/`defaultNb` variables at the top).
- Exit 0 + `PASS: …` = success. Exit 1 + `FAIL: …` = nothing (or a restored backup) on disk.

Workflow per synced cell: `stability` → fix source if it fails → `replace`/`insert` →
done (verification is built in). Report the PASS lines.

## Hard rules (the script enforces #2–#5; you own #1)

1. **Keep synced code cells pure code.** The code→boxes conversion discards `(* … *)`
   comments, so a commented cell would differ between the two files. Notes go in a separate
   text cell or the workbook.
2. **Box-round-trip stability.** A fraction with a *product* numerator (`a*b/c`)
   reassociates `Times` through `FractionBox` and breaks `===`; atomic-numerator fractions
   are stable. Fix by assigning the numerator to a local (`c2 = a*b; … c2/c`), re-validate
   the maths numerically, then sync. The script refuses to write unstable code.
3. **Backup before write, restore on failed verification.** Automatic (`/tmp/sync-wb-nb-backup-*.nb`).
4. **Unique-target assertion.** Ambiguous or missing snippet matches abort before writing.
5. **Verify, don't trust**: after writing, the `.nb` cell must parse `===` the `.wb` code.

## Why wolframscript (not Python)

Only the Wolfram kernel can convert code text to Input boxes (`MakeBoxes`) and parse `.nb`
box structures back; a Python splice would also leave the `.nb`'s internal byte-offset
cache stale. Import→modify→Export regenerates it correctly and preserves outputs.

## Implementation notes (for maintaining the script)

- Snippet matching uses `ToString[boxes, InputForm, PageWidth -> Infinity]` — default
  `ToString` line-wraps and can split a token across a `\` continuation, silently breaking
  `StringContainsQ`.
- Cell replacement uses `Position`+`Select`(SameQ)+`ReplacePart`, never `nb /. oldCell ->
  new`: a literal Cell as a `/.` LHS can silently fail to fire. UUID-anchored `/.` rules
  are fine for *insertion* (the anchor cell is matched by its UUID option, not its body).
- Markdown `.wb` cells (kind 1) are not handled by the script; mirror them manually as
  `Cell[text, "Subsection"/"Text"]` matching neighbouring styles.
- Quote the project path (spaces + parentheses); wolframscript needs absolute paths.
