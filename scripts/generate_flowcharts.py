#!/usr/bin/env python3
"""
Generate flowchart PNGs using Graphviz.
Usage:  python3 scripts/generate_flowcharts.py
Output: assets/flowchart-setup.png, assets/flowchart-session.png
"""

import os
import graphviz

os.makedirs('assets', exist_ok=True)

BG = '#0d1117'

# ── Node styles ───────────────────────────────────────────────────────────────
S_TERM = {                          # start / end (green pill)
    'shape': 'rectangle', 'style': 'filled,rounded',
    'fillcolor': '#1a4731', 'color': '#3fb950', 'penwidth': '2',
    'fontcolor': '#aff5c4', 'fontname': 'Helvetica-Bold', 'fontsize': '14',
    'width': '3.4', 'height': '0.52', 'fixedsize': 'false',
}
S_PROC = {                          # process box (blue)
    'shape': 'rectangle', 'style': 'filled,rounded',
    'fillcolor': '#0c1f3f', 'color': '#388bfd', 'penwidth': '2',
    'fontcolor': '#79c0ff', 'fontname': 'Helvetica', 'fontsize': '12',
    'width': '4.2', 'fixedsize': 'false',
}
S_DEC = {                           # decision diamond (amber)
    'shape': 'diamond', 'style': 'filled',
    'fillcolor': '#2b1e00', 'color': '#d29922', 'penwidth': '2',
    'fontcolor': '#e3b341', 'fontname': 'Helvetica', 'fontsize': '12',
}
S_LOOP = {                          # loop-back indicator (muted green)
    'shape': 'rectangle', 'style': 'filled,rounded,dashed',
    'fillcolor': '#0d1f12', 'color': '#3fb950', 'penwidth': '1.5',
    'fontcolor': '#3fb950', 'fontname': 'Helvetica', 'fontsize': '11',
    'width': '3.0', 'fixedsize': 'false',
}

# ── Edge styles ───────────────────────────────────────────────────────────────
_E = {'color': '#8b949e', 'penwidth': '1.8',
      'fontname': 'Helvetica-Bold', 'fontsize': '11', 'fontcolor': '#8b949e'}
E_MAIN = {**_E}
E_YES  = {**_E, 'fontcolor': '#3fb950'}
E_NO   = {**_E, 'fontcolor': '#f85149'}


def make_graph(name, title, pad='0.55'):
    return graphviz.Digraph(
        name,
        graph_attr={
            'bgcolor':    BG,
            'rankdir':    'TB',
            'splines':    'spline',      # default Bezier; inline labels fully supported
            'nodesep':    '0.6',
            'ranksep':    '0.7',
            'fontname':   'Helvetica-Bold',
            'fontsize':   '17',
            'fontcolor':  '#e6edf3',
            'label':      title,
            'labelloc':   't',
            'pad':        pad,
            'dpi':        '180',
        }
    )


def nd(g, nid, lbl, sty):
    g.node(nid, label=lbl, **sty)


def ed(g, a, b, sty, lbl='', **kw):
    attrs = {**sty}
    if lbl:
        attrs['label'] = f'  {lbl}  '
    attrs.update(kw)
    g.edge(a, b, **attrs)


def same_rank(g, *nodes):
    with g.subgraph() as s:
        s.attr(rank='same')
        for n in nodes:
            s.node(n)


# ── Chart 1 — Setting up a new research project ───────────────────────────────

def chart_setup():
    g = make_graph('setup', 'Setting up a new research project\n\n\n', pad='0.55,0.9')

    nd(g, 'start',  'New research project', S_TERM)
    nd(g, 'cla',    'Write CLAUDE.md\n'
                    'goal · file map · conventions · git config\n'
                    'current status · open tasks · skills list',  S_PROC)
    nd(g, 'cond',   'Write brief.tex (short reference)\n'
                    'established results only · no proofs\n'
                    '15–30 pages · read first every session',      S_PROC)
    nd(g, 'nsp',    'Write next-session-prompts.md\n'
                    'first task at top · DONE log at bottom',      S_PROC)
    nd(g, 'sett',   'Configure .claude/settings.json\n'
                    'allow routine · ask before risky · deny destructive\n'
                    'add pre-compact hook · test in terminal first', S_PROC)
    nd(g, 'ddual',  'Dual\nremotes?',                              S_DEC)
    nd(g, 'dual',   'Add GitHub + GitLab remotes\n'
                    'configure git-push-both.sh',                  S_PROC)
    nd(g, 'skills', 'Write .claude/skills/\n'
                    'one .md file per repeatable procedure\n'
                    'list each skill in CLAUDE.md',                S_PROC)
    nd(g, 'end',    'Open Claude Code',                            S_TERM)

    ed(g, 'start',  'cla',    E_MAIN)
    ed(g, 'cla',    'cond',   E_MAIN)
    ed(g, 'cond',   'nsp',    E_MAIN)
    ed(g, 'nsp',    'sett',   E_MAIN)
    ed(g, 'sett',   'ddual',  E_MAIN)
    ed(g, 'ddual',  'dual',   E_YES,  lbl='yes')
    ed(g, 'ddual',  'skills', E_NO,   lbl='no')
    ed(g, 'dual',   'skills', E_MAIN)
    ed(g, 'skills', 'end',    E_MAIN)

    same_rank(g, 'ddual', 'dual')
    return g


# ── Chart 2 — Each working session ────────────────────────────────────────────

def chart_session():
    g = make_graph('session', 'Each working session')

    nd(g, 'start',  'Open Claude Code',                            S_TERM)
    nd(g, 'load',   'CLAUDE.md auto-loads\n'
                    'read top task from next-session-prompts.md\n'
                    'read brief.tex if context is stale',          S_PROC)
    nd(g, 'work',   'Work: edit · compile · compute',              S_PROC)
    nd(g, 'dchk',   'Natural\ncheckpoint?',                        S_DEC)
    nd(g, 'cmit',   'git commit\nsmall + descriptive message',     S_PROC)
    nd(g, 'drsl',   'Result\nestablished?',                        S_DEC)
    nd(g, 'upd',    'Update workbook.tex\n'
                    'sync brief.tex\n'
                    'update CLAUDE.md status',                     S_PROC)
    nd(g, 'ddon',   'Session\ndone?',                              S_DEC)
    nd(g, 'wrap',   'Update CLAUDE.md: last result + next step\n'
                    'write next task in next-session-prompts.md\n'
                    'move completed tasks to DONE log',            S_PROC)
    nd(g, 'end',    'git push',                                    S_TERM)
    # Loop indicator — avoids the messy back-edge across the whole chart
    nd(g, 'loop',   '↩  not done — repeat from Work',             S_LOOP)

    ed(g, 'start', 'load',  E_MAIN)
    ed(g, 'load',  'work',  E_MAIN)
    ed(g, 'work',  'dchk',  E_MAIN)

    ed(g, 'dchk',  'cmit',  E_YES,  lbl='yes')
    ed(g, 'dchk',  'drsl',  E_NO,   lbl='no')
    ed(g, 'cmit',  'drsl',  E_MAIN)          # merge back

    ed(g, 'drsl',  'upd',   E_YES,  lbl='yes')
    ed(g, 'drsl',  'ddon',  E_NO,   lbl='no')
    ed(g, 'upd',   'ddon',  E_MAIN)          # merge back

    ed(g, 'ddon',  'wrap',  E_YES,  lbl='yes')
    ed(g, 'ddon',  'loop',  E_NO,   lbl='no')  # loop indicator, no back-edge

    ed(g, 'wrap',  'end',   E_MAIN)

    same_rank(g, 'dchk', 'cmit')
    same_rank(g, 'drsl', 'upd')
    return g


# ── Render ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    for builder, stem in [(chart_setup,   'flowchart-setup'),
                          (chart_session, 'flowchart-session')]:
        g = builder()
        path = g.render(filename=f'assets/{stem}', format='png',
                        engine='dot', cleanup=True)
        print(f'Saved {path}')
    print('Done.')
