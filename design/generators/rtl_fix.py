"""Add RLM (U+200F) to the start of Persian/English text lines and table cells, matching repo style."""
import re, sys
RLM = '‏'

def cell(c):
    s = c.strip()
    if not s or re.fullmatch(r':?-{3,}:?', s) or s.startswith(RLM) or s in ('—',):
        return ' ' + s + ' ' if s else ' '
    return ' ' + RLM + s + ' '

def line(l):
    if l.startswith('|'):
        parts = l.split('|')
        return '|'.join([parts[0]] + [cell(p) for p in parts[1:-1]] + [parts[-1]])
    m = re.match(r'^(#{1,6} |> |- |\d+\. |>\s*-\s)?(.*)$', l)
    pre, rest = m.group(1) or '', m.group(2)
    if not rest.strip() or rest.startswith(RLM) or rest.startswith(('```', '---', '<')):
        return l
    if pre == '' and l.startswith(('  ', '\t')):
        return l
    return pre + RLM + rest

def fix(text):
    out, code, front = [], False, False
    for i, l in enumerate(text.split('\n')):
        if i == 0 and l == '---':
            front = True; out.append(l); continue
        if front:
            out.append(l)
            if l == '---': front = False
            continue
        if l.startswith('```'):
            code = not code; out.append(l); continue
        out.append(l if code else line(l))
    return '\n'.join(out)

if __name__ == '__main__':
    p = sys.argv[1]
    t = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(fix(t))
