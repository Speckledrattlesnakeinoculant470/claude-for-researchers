# Changelog

Notable, user-facing changes to this toolkit. This is a curated list of the
updates worth knowing about — not every commit (see the git history for that).
Useful for deciding whether to re-copy anything from `starter/` into a project
you set up from an earlier version.

Versioning is calendar-based (`vYYYY.MM`): this is a guide and a copy-in starter
pack, not a linked library, so there is no API to break — the version answers
"how current is my copy?", nothing more.

## v2026.06 — 2026-06-13

First tagged release of the current structure. Everything below landed this month.

### Action needed if you set up a project before this release
- **Skills must use the folder format `skills/<name>/SKILL.md`.** A flat
  `skills/<name>.md` file is silently *not* registered as a slash command. If your
  skills are flat files, move each `<name>.md` to `<name>/SKILL.md`.
- The skills below were rewritten. If you copied earlier versions, re-copy them
  from `starter/.claude/skills/` to get the fixes.

### Added
- **Adaptive bootstrapping.** Both setup routes now install *by relevance* instead
  of installing everything: the README bootstrap prompt selects skills from your
  project description, and a new interactive `scripts/bootstrap.sh` asks a few
  questions and installs only what applies. The workbook / brief /
  next-session-prompts trio plus CLAUDE.md is the universal core; everything else
  is conditional.
- **Global skills** (`~/.claude/skills/`) documented — install a skill once and use
  it in every project; bootstrapping checks there before making a local copy.
- **Overleaf-via-git workflow** and the `overleaf-sync` skill, for collaborating on
  a shared Overleaf project from its git remote.
- **AI-output staging**: `numerics/generated/` and `figures/generated/` folders for
  Claude-produced outputs pending your review.
- **Context-monitoring note** in the session-length section: the read-only `/context`
  (what's filling the window) and `/usage` (where tokens/cost go) commands, plus a rule
  of thumb — glance at ~50%, act by ~70%, don't wait for auto-compaction, and for
  research prefer a fresh session seeded from your documents over repeated (lossy)
  compaction.

### Changed
- **`latex-compile`** rewritten: compiles with `pdflatex` and captures stdout
  (avoiding the `latexmk` stale-log trap), greps with `-a` (pdflatex embeds binary
  bytes that silently defeat plain grep), uses correct severity thresholds, and
  reformats rather than rewords when fixing overfull boxes.
- **`sync-wb-nb`** gained a `regenerate` mode that rebuilds a whole `.nb` from its
  `.wb` with proper syntax colouring and section headings — for new or
  fully-rewritten notebooks, alongside the existing cell-by-cell sync.
- **`nb-to-wolfbook`** rewritten to make every converted cell *bridge-safe*: each
  statement goes on one physical line, so the tool that runs cells from VS Code
  cannot silently mis-evaluate a statement that was wrapped across several lines.
  The line-boundary detector handles the tricky Wolfram cases — postfix `&`
  (`Function`) ends a statement while `&&` continues it, `/;` (`Condition`) and `/.`
  continue, `2.` (a number) ends, and backslash-continued long numbers/strings
  (e.g. high-precision values, `*^-76` exponents) re-join with no inserted space.
  Ships helper scripts (`nb2wb.py`, `nb2wb_extract.wls`, `wl_normalize.py`).
- **Permissions model** in `starter/.claude/settings.json`: allow routine commands,
  *ask* before anything dangerous (including `sudo`/`mkfs`/`fdisk`/`shred`), block
  nothing outright — so Claude never stalls but always pauses before a risky action.
- Templates consolidated into `starter/` (the old `examples/` folder was retired);
  the `sync-condensed` skill was renamed `sync-brief`.
- The **dual-remote mirror hook is now opt-in** (off by default). It was a silent
  trap before — see Fixed.

### Fixed
- **Silent dual-remote mirror hook.** The starter's `settings.json` shipped an
  *active* `PostToolUse` hook running `scripts/git-push-both.sh`, but the starter
  didn't include that script — so a copied project appeared to mirror pushes to a
  second remote (e.g. institution GitLab) while silently doing nothing. The hook now
  ships **off** (empty `PostToolUse`), the `git-push-both.sh` template is included
  under `starter/scripts/`, and both bootstrap routes enable it only if you say you
  use two remotes, with the exact block to paste documented in `settings.json`.

### Clarified
- The opening of the guide now states its scope explicitly: this is a workspace and
  workflow toolkit to make *your* research faster, not a system for getting Claude
  to conduct research autonomously.
