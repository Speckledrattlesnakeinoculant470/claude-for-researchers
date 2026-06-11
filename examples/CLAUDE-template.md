# CLAUDE.md — [Project Name]

<!--
INSTRUCTIONS FOR FILLING THIS IN:
- Fill in every section. Don't leave placeholders.
- Keep it to one screenful per section where possible.
- Update "Current status" and "Open tasks" at the end of every session.
- Move finished items out of "Open tasks" into next-session-prompts.md (DONE log).
- Do NOT use this file as a logbook. It is a current-state snapshot.
-->

## Goal
<!-- One paragraph. What is this project? What is the mathematical/scientific object?
     What is the open question you are working toward? -->

[e.g., Compute the integral of four modular Eisenstein series over the fundamental
domain as a function of their spectral parameters, using the Rankin–Selberg unfolding method.]

## Files
<!-- Map of every file Claude needs to know about. One line each.
     Be explicit about which file is authoritative. -->

- **brief.tex** — short (20–30 pp) self-contained reference; READ FIRST in every new session.
  Contains current results, key formulas, open questions. No derivations.
- **workbook.tex** — full working record (~N pp): every proof, derivation, failed attempt,
  and discussion in complete detail. Not a paper draft — a research journal in LaTeX.
  Too large to read in full — grep or search by section label.
- **next-session-prompts.md** — task log. Top section = next task; bottom = DONE log.
- **numerics/** — computation scripts. `README.md` inside explains each file.

## Conventions
<!-- Notation Claude must get right. Be precise about signs, normalizations, definitions. -->

- [e.g., ξ(s) = π^{-s/2} Γ(s/2) ζ(s). Functional equation ξ(s) = ξ(1-s).]
- [e.g., E*_s = ξ(2s) E(z,s) = completed Eisenstein series. Simple poles at s=0,1, residues ∓½.]
- [Add your own conventions here]

## Current status
<!-- One screenful. What is established? What is the last result? What is the exact next step?
     Update this before ending every session. -->

**Last result (DATE):** [what was computed/proved]

**Established:**
- [bullet list of what is rigorous and complete]

**Open:**
- [bullet list of what is pending, ranked by priority]

**Next step:** [the single most important thing to do next]

## Chat formatting (IMPORTANT)
In chat replies, do NOT use LaTeX markup ($...$, \frac, \xi, etc.) — it does not
render in Claude Code's chat window. Write math in plain Unicode:
  ξ, μ, σ, Γ, ζ, ∑, ∏, ∫, √, ½, →, ≈, ≠, ≤, ⇒
  single subscripts/superscripts (one char): M₃, μ₀, sᵢ, x², yⁿ
  multi-char sub/superscripts: M_{ab}, e^{-π t}, τ^{-2}
LaTeX belongs ONLY inside .tex files.

## Skills
<!-- List skills defined in .claude/skills/ and when to invoke them. -->

- `/latex-compile` — compile workbook.tex or brief.tex, fix errors and overfull boxes.
  Use after any edit to a .tex file.
- `/sync-condensed` — propagate load-bearing changes from workbook.tex to brief.tex.
  Use after establishing a new result.
- `/nb-to-wolfbook` — convert .nb notebooks or .m scripts to Wolfbook's .wb format.
  Use when migrating existing Mathematica files to work in VS Code with Wolfbook.
- `/overleaf-sync` — sync the `Overleaf/` git clone of a shared paper: status/pull/diff/publish.
  Only if you collaborate on Overleaf via its git remote. Remove this line otherwise.

## Writing style in workbook.tex (IMPORTANT)
<!-- Tell Claude how detailed to be when writing in your main document.
     Researchers often want very different levels of detail than Claude's default. -->

workbook.tex is the AUTHORITATIVE, COMPREHENSIVE record. Show every step of every
calculation. State each substitution, each application of the functional equation,
each sign. Never collapse multi-step manipulations into "one finds" or "a short
computation gives." If in doubt, over-explain.

[Adapt this section to your own preference — some researchers want the opposite:
 terse, theorem-style prose. Be explicit either way.]

## Structure and cross-references in workbook.tex (IMPORTANT)
<!-- Claude navigates workbook.tex with grep and targeted reads, not by reading top to bottom.
     These rules make that navigation reliable. -->

- Use \label on every section, subsection, theorem, proposition, equation, and figure.
  Cross-reference explicitly with \ref / \eqref. More cross-references than you would
  write for a human reader is the right amount.
- Maintain a clear section hierarchy (sections → subsections → subsubsections with
  meaningful names). Flat structure makes targeted reads unreliable.

## Corrections in workbook.tex (NON-NEGOTIABLE)
<!-- This rule prevents Claude from working from wrong information in future sessions. -->

If something in workbook.tex is discovered to be wrong, REPLACE IT IN PLACE. Do not
append a correction paragraph later ("earlier I claimed X, but actually Y").

Reason: Claude reads different parts of workbook.tex in each session. If the wrong
version stays in the file and the correction is only further down, Claude may read
the wrong statement in a later session and never see the correction. It will then
work from incorrect information, confidently.

## Citations (NON-NEGOTIABLE)
<!-- This rule prevents fabricated references from entering the paper. -->

Never write a citation into any file without first verifying the paper exists on
Semantic Scholar, arXiv, or OpenAlex. Use /verify-citation before adding any reference.
If you cannot confirm the paper exists, say so — do not invent a plausible alternative.

## Anti-sycophancy rule (IMPORTANT)
<!-- This rule makes capitulation visible and reversible. -->

If you change your answer because I expressed doubt or disagreement, say so explicitly:
"I am revising my earlier answer because you pushed back."
Do not quietly update a formula or derivation without flagging the change.

If I ask you to check a contested result, re-derive it from the definitions in
this file — do not let the prior conversation influence the derivation.

## AI-generated outputs
<!-- Keeps AI-produced results separate from your own computations. -->

All plots, tables, and numerical outputs you produce go in `numerics/generated/`
or `figures/generated/` until I have reviewed them and traced them to a committed
script. Never include `generated/` content in workbook.tex without my explicit instruction.

## Numerics
<!-- Primary computation engine, venv location, any gotchas. -->

- Primary engine: Python + mpmath (precision: `mp.dps = 30` unless stated otherwise)
- venv: `numerics/venv/` — run scripts as `numerics/venv/bin/python numerics/script.py`
- Route all long-running output to `numerics/run.log`
- AI-produced outputs: `numerics/generated/` (provisional, requires review before use)

## Git
<!-- Remote setup, identity, push procedure. -->

- Remote `github`: https://github.com/YOUR_USERNAME/YOUR_REPO.git (primary)
- Remote `gitlab`: git@git.YOUR_INSTITUTION.ac.uk:YOUR_ID/YOUR_REPO.git (institution mirror)
- Push: `git push github main` (hook auto-mirrors to gitlab)
- Commit author: YOUR_NAME <your-email@example.com>
- NO Co-Authored-By trailers in commits.

## LaTeX gotchas
<!-- Any project-specific LaTeX issues Claude should know about. -->

- `\Res` is defined as `\DeclareRobustCommand` (used in section titles → .toc)
- Macros in use: [list your custom macros]
- Compile: `pdflatex workbook.tex` twice (for TOC), or `latexmk -pdf`
