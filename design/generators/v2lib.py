"""Shared helpers for v2 CH scripts (CH-57+). Paths follow repo root REPO."""
import re, os, sys
REPO = os.environ.get('REPO', '/home/claude/customer-support-prd')
B = REPO + '/prd/'
S = B + '03 - PRD Sections/'
M = B + '00 - Master Project Index.md'
D = '2026-11-20'
RLM = '‏'
sys.path.insert(0, os.path.dirname(__file__))

def R(s, a, b):
    assert a in s, 'MISSING: ' + a[:120]
    return s.replace(a, b, 1)

def after_line(s, anchor, new):
    """insert `new` (one or more lines) after the line containing anchor"""
    i = s.index(anchor); j = s.index('\n', i)
    return s[:j + 1] + new.rstrip('\n') + '\n' + s[j + 1:]

def before_line(s, anchor, new):
    i = s.index(anchor); i = s.rfind('\n', 0, i) + 1
    return s[:i] + new.rstrip('\n') + '\n' + s[i:]

def front(s, new, note):
    s = re.sub(r'^version: .*$', f'version: {new}', s, count=1, flags=re.M)
    s = re.sub(r'^last_updated: .*$', f'last_updated: {D}', s, count=1, flags=re.M)
    return re.sub(r'^(change_note: ".*?)"$', lambda m: m.group(1) + f' · {new} — {note}"', s, count=1, flags=re.M)

def hist(s, ver, text, ref):
    rows = list(re.finditer(r'^\| ‏\d+\.\d+ \| ‏\d{4}-\d\d-\d\d \|.*$', s, flags=re.M))
    assert rows, 'no history'
    last = rows[-1]; ncol = last.group(0).count('|') - 1
    cells = [f'‏{ver}', f'‏{D}', f'‏{text}'] + ([f'‏{ref}'] if ncol >= 4 else [])
    return s[:last.end()] + '\n| ' + ' | '.join(cells) + ' |' + s[last.end():]

def rw(path, fn):
    s = open(path, encoding='utf-8').read(); t = fn(s); assert t != s, path
    open(path, 'w', encoding='utf-8').write(t); print('ok', path.split('/')[-1])

def row(*cells):
    return '| ' + ' | '.join(c if c.startswith(RLM) or c in ('—', '') else RLM + c for c in cells) + ' |'

def mi_dec(s, rows):
    """append DEC rows after the last DEC-3xx row of §6.1 (before ## ۷ / arch table handled by anchor)"""
    anchor = '| ‏DEC-320 |'
    last = None
    for m in re.finditer(r'^\| ‏DEC-3(2\d|3\d|4\d|5\d) \|.*$', s, flags=re.M):
        last = m
    pos = (last.end() if last else s.index('\n', s.index(anchor)))
    return s[:pos] + '\n' + '\n'.join(rows) + s[pos:]

def mi_ch(s, rowtxt):
    last = None
    for m in re.finditer(r'^\| ‏CH-\d+ \|.*$', s, flags=re.M):
        last = m
    return s[:last.end()] + '\n' + rowtxt + s[last.end():]

def mi_doc(s, name_anchor, ver, note):
    """update version + date cell in §5 doc table row starting with name_anchor"""
    m = re.search(r'^\| ‏' + re.escape(name_anchor) + r'.*$', s, flags=re.M)
    assert m, name_anchor
    cells = m.group(0).split('|')
    cells[3] = f' ‏**{ver}** '
    cells[4] = f' ‏{D} '
    if note: cells[5] = cells[5].rstrip() + f'؛ {note} '
    return s[:m.start()] + '|'.join(cells) + s[m.end():]
