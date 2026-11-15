"""Builds ../questions.html: the same papers, organised by the big questions the disciplines are trying to answer.
theme → question → a field that answers it → its papers on that question.  Run: python3 src/build_questions.py"""
import glob, hashlib, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'shell')); import shell
def tx(c): return ''.join(ch + ('︎' if 0x2190 <= ord(ch) <= 0x2bff else '') for ch in c)
def hid(t): return hashlib.md5(t.strip().lower().encode()).hexdigest()[:6]
PAP = {}
for f in sorted(glob.glob(os.path.join(here, 'data', '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for fl in d['fields']:
        for p in fl['papers'] + fl.get('more', []): PAP.setdefault(hid(p['title']), p)
def item(p):
    yr = str(p['year'])
    return {'q': f"{p['authors']} · {yr} · {p['venue']}", 'f': p['title'], 'm': p['why'], 'ml': 'Why it matters',
            'c': f"{p['authors']} ({yr}). {p['title']}. {p['venue']}."}
Q = json.load(open(os.path.join(here, 'questions.json'), encoding='utf-8'))
P, lost = [], 0
for th in Q['themes']:
    g = {'n': th['n'], 'i': tx(th.get('i', '')), 'u': [], 't': []}
    for q in th['qs']:
        idx = []
        for a in q['answers']:
            ks = [item(PAP[r]) for r in a['refs'] if r in PAP]; lost += len(a['refs']) - len(ks)
            if not ks: continue
            idx.append(len(g['t']))
            disc, fld = [x.strip() for x in a['field'].split('/', 1)]
            g['t'].append({'t': f'{disc} · {fld}', 'p': (q['p'] + ' ' + a['angle']) if not idx[:-1] else a['angle'], 'k': ks})
        if idx: g['u'].append({'n': q['q'], 't': idx})
    if g['u']: P.append(g)
if lost: print(f'{lost} refs no longer on the site (dropped)')
n = shell.build(P, os.path.join(here, '..', 'questions.html'),
    title='The best papers on…', lead='The best papers on', key='tq',
    words=['theme', 'question', 'field', 'paper'], steps=['theme', 'question', 'field', 'papers'],
    theme='ink', end='', foot='<a class="foot" href="index.html">By field →</a>',
    sub='<p class="sub">The same papers, sorted by the big questions they’re trying to answer. Pick a question to see which fields attack it, and from which side.</p>')
print(f"{len(P)} themes, {sum(len(g['u']) for g in P)} questions, {sum(len(t['k']) for g in P for t in g['t'])} paper slots, {n // 1024} KB")
