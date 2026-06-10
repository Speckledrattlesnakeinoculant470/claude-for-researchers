# latex-compile

Compile a LaTeX document, fix errors and overfull hboxes, and report the result.

## When to invoke
After any edit to a .tex file. Also invoke before committing.

## Input
The user may specify a file: `/latex-compile brief.tex`. Default: `manuscript.tex`.

## Steps

1. Run `pdflatex -interaction=nonstopmode -halt-on-error <file>` twice
   (second pass resolves cross-references and TOC).

2. Check the output for:
   - **Fatal errors** (`! ` lines): fix before proceeding. Common causes:
     - Undefined control sequence → check macro definitions
     - Missing `{` → usually a fragile macro in a section title; use `\DeclareRobustCommand`
     - Missing `$` → math mode error, stray character
   - **Undefined references** (`LaTeX Warning: Reference ... undefined`):
     report to user; these are usually harmless if expected (forward references)
     but worth flagging.
   - **Overfull hboxes** (`Overfull \hbox`): for lines > 5pt over, fix by:
     - Adding `\allowbreak` or a line break at a natural word boundary
     - Switching inline math to display math
     - Adding `\emergencystretch=3em` to the preamble (last resort)

3. Report:
   - Page count (`Output written on ... (N pages)`)
   - Number of undefined references
   - Number of overfull hboxes > 5pt
   - Any fatal errors encountered and how they were fixed

## Output format
```
Compiled <file>: N pages, M undefined refs, K overfull hboxes.
[If errors: fixed X, remaining Y (describe)]
```
