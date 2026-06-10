# nb-to-wolfbook

Converts existing Mathematica files (.nb notebooks or .m scripts) to Wolfbook format
(.wb) so they can be opened and run inside VS Code with the Wolfbook extension.

## When to invoke
`/nb-to-wolfbook <file-or-directory>`

Use when the user has existing .nb or .m files and wants to work with them in Wolfbook.
Accepts a single file or a directory — if given a directory, convert all .nb and .m
files found in it (non-recursively).

## Background: the .wb format

Wolfbook .wb files are plain-text JSON following VS Code's Notebook API. The structure:

```json
{
 "cells": [
  {
   "kind": 2,
   "languageId": "wolfram",
   "value": "f[x_] := x^2",
   "metadata": {},
   "outputs": []
  },
  {
   "kind": 1,
   "languageId": "markdown",
   "value": "# Section heading or prose note",
   "metadata": {},
   "outputs": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "displayName": "Wolfram Language",
   "language": "wolfram",
   "name": "wolfram"
  }
 }
}
```

Rules:
- `kind: 2` = Wolfram code cell; `kind: 1` = Markdown text cell
- `languageId` (NOT `language`) is REQUIRED on every cell — VS Code builds each cell
  as a `vscode.NotebookCellData` and rejects the file with "NotebookCellData MUST have
  'languageId' property" if it is missing. Use `"wolfram"` for code, `"markdown"` for
  text. (The Wolfbook serializer passes the parsed JSON straight through to VS Code,
  so the on-disk keys must match `vscode.NotebookData`/`NotebookCellData` exactly.)
- Use exactly 1-space indentation throughout
- `value` must be a valid JSON string: `\` → `\\`, `"` → `\"`, newlines → `\n`
- `outputs: []` for all cells — outputs are not preserved, user will re-run
- UTF-8 encoding

**Always use Python's `json` module to write the file** — never build JSON strings
manually. Use `json.dumps(data, indent=1, ensure_ascii=False)`.

## Steps for .m files

1. Read the file with the Read tool.
2. Split into code blocks: runs of 2 or more consecutive blank lines mark cell
   boundaries. Each contiguous block of non-blank lines becomes one cell.
3. Identify section-header comments: if a block consists entirely of a comment like
   `(* === Title === *)` or `(* Section: Residues *)`, make it a markdown cell
   (`kind: 1`) with the comment text as the heading. All other blocks are code cells
   (`kind: 2`).
4. Write a short Python script that:
   - Builds the cell list
   - Writes `json.dumps(notebook, indent=1, ensure_ascii=False)` to `<basename>.wb`
     in the same directory as the source file
5. Run the script with the Bash tool.
6. Report: `Created <basename>.wb — N code cells, M markdown cells.`

## Steps for .nb files

The .nb format is proprietary. Try conversion paths in this order:

**Path A — wolframscript available** (`which wolframscript` succeeds):
1. Export the notebook as a package file:
   ```bash
   wolframscript -code 'Export["<basename>.m", Import["<abs-path>.nb", "Package"]]'
   ```
2. Convert the resulting .m file using the .m steps above.
3. Note in the output: text/formatted cells were not preserved — only code survives
   the Package export.

**Path B — wolframscript not available, Python available**:
1. Check for `mathematica2jupyter`: `pip show mathematica2jupyter 2>/dev/null`
   - If absent: `pip install mathematica2jupyter`
2. Convert: `python -m mathematica2jupyter <file.nb> <basename>.ipynb`
3. Read the resulting .ipynb (JSON). For each cell where `cell_type == "code"`,
   join the `source` list into a single string and create a `kind: 2` cell.
   For `cell_type == "markdown"`, create a `kind: 1` cell.
4. Write the .wb file.
5. Note in the output: converted via mathematica2jupyter; output cells not preserved.

**Path C — neither available**:
Tell the user:
> "Automatic .nb conversion requires either wolframscript (needs a Mathematica
> licence) or Python with pip. You can also convert manually: open the notebook in
> Mathematica desktop, go to File → Save As, choose 'Package (.m)', save it, then
> run `/nb-to-wolfbook` on the resulting .m file."

## Output format

Report one line per file:

```
Converted: residues.nb  →  residues.wb   (14 code cells, wolframscript)
Converted: helpers.m    →  helpers.wb    (6 code cells, 2 markdown cells)

Note: output cells are not preserved — re-run cells in VS Code to regenerate results.
```

If any file could not be converted, say which one and why.
If the notebook was heavily graphics-based, warn that some cells may need manual
cleanup after opening.
