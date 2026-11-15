"""Builds ../index.html from data/*.json inside the shared shell (src/shell/).  Run: python3 src/build.py
group → discipline → field → its ten papers. Each paper: authors · year · venue above, title, and a fold saying why it still matters."""
import glob, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'shell')); import shell

def tx(c): return ''.join(ch + ('︎' if 0x2190 <= ord(ch) <= 0x2bff else '') for ch in c)   # keep symbols in text form

GROUPS = [
  ('Humanities', '❦', [('History', '⧗'), ('Philosophy', '∴'), ('Religious studies', '✺'), ('Arts & music', '♫'), ('Literature', '¶')]),
  ('Social sciences', '⚖', [('Economics', '¤'), ('Political science', '⚑'), ('Psychology', 'Ψ'), ('Sociology', '⁂'),
                            ('Anthropology', '☥'), ('Linguistics', 'ʃ'), ('Communication', '≋'), ('Education', '✎'), ('Geography', '⊕'), ('Law', '§')]),
  ('Natural sciences', '☉', [('Physics', '⚛'), ('Astronomy', '✶'), ('Chemistry', '⌬'), ('Biology', '❀'),
                             ('Neuroscience', '∿'), ('Earth sciences', '◒')]),
  ('Formal sciences', '∑', [('Mathematics', 'π'), ('Statistics', 'σ'), ('Computer science', 'λ'), ('Systems & information', '⇄')]),
  ('Applied sciences', '⚒', [('Medicine & health', '⚕'), ('Engineering', '⚙'), ('Architecture & planning', '⌂'),
                             ('Environment', '❧'), ('Business', '↗')]),
]
# field order per discipline (the locked list)
ORDER = {
 'History': ['Ancient (Greece & Rome)', 'Medieval', 'Early modern', 'Modern & global', 'Latin American', 'Economic history', 'History of science'],
 'Philosophy': ['Epistemology', 'Metaphysics', 'Ethics', 'Political philosophy', 'Philosophy of mind', 'Philosophy of science', 'Philosophy of language'],
 'Arts & music': ['Art history', 'Musicology', 'Ethnomusicology', 'Film studies'],
 'Literature': ['Literary theory'],
 'Economics': ['Microeconomic theory', 'Macroeconomics & growth', 'Econometrics', 'Behavioral', 'Development', 'Labor', 'Public', 'Environmental & energy economics', 'International trade', 'Financial economics'],
 'Political science': ['Comparative politics', 'International relations', 'Political economy', 'Voting & public opinion'],
 'Psychology': ['Cognitive', 'Social', 'Developmental', 'Clinical', 'Personality & individual differences', 'Evolutionary'],
 'Sociology': ['Stratification & inequality', 'Social networks', 'Demography', 'Criminology', 'Organizations & economic sociology'],
 'Anthropology': ['Cultural anthropology', 'Biological anthropology & human evolution', 'Archaeology'],
 'Linguistics': ['Syntax', 'Phonology', 'Semantics & pragmatics', 'Historical linguistics', 'Sociolinguistics', 'Psycholinguistics'],
 'Geography': ['Human & economic geography'],
 'Law': ['Law & economics'],
 'Religious studies': ['Study of religion'],
 'Communication': ['Media & communication'],
 'Education': ['Learning & education research'],
 'Physics': ['Particle physics', 'Atomic, molecular & optical', 'Condensed matter', 'Statistical mechanics', 'Quantum foundations & information', 'Gravitation', 'Plasma physics & fusion'],
 'Astronomy': ['Cosmology', 'Stars & galaxies', 'Planetary science & exoplanets', 'Black holes & gravitational waves'],
 'Chemistry': ['Organic', 'Inorganic', 'Physical', 'Theoretical & computational', 'Materials & polymers', 'Catalysis', 'Analytical'],
 'Biology': ['Molecular biology', 'Biochemistry', 'Structural biology', 'Cell biology', 'Genetics & genomics', 'Developmental biology', 'Evolutionary biology', 'Ecology',
             'Microbiology', 'Virology', 'Immunology', 'Plant biology', 'Animal behavior', 'Systems & synthetic biology', 'Bioinformatics'],
 'Neuroscience': ['Cellular & molecular', 'Systems', 'Cognitive', 'Computational'],
 'Earth sciences': ['Geology & plate tectonics', 'Climate science', 'Oceanography', 'Atmospheric science', 'Paleontology'],
 'Mathematics': ['Algebra', 'Number theory', 'Analysis', 'Geometry', 'Topology', 'Probability', 'Combinatorics', 'Logic & foundations', 'Dynamical systems'],
 'Statistics': ['Inference', 'Bayesian statistics', 'Causal inference', 'Statistical learning'],
 'Computer science': ['Theory & complexity', 'Algorithms', 'Machine learning', 'AI alignment & interpretability', 'Natural language processing', 'Computer vision', 'Cryptography & security',
                      'Distributed systems', 'Programming languages', 'Databases', 'Networking', 'Human-computer interaction', 'Computer architecture'],
 'Systems & information': ['Information theory', 'Game & decision theory', 'Network science', 'Control theory', 'Optimization & operations research', 'Complexity science'],
 'Medicine & health': ['Epidemiology', 'Public & global health', 'Nutrition', 'Clinical trials & evidence-based medicine', 'Oncology', 'Cardiology', 'Endocrinology & metabolism', 'Infectious disease', 'Pharmacology', 'Neurology', 'Psychiatry'],
 'Engineering': ['Electrical & electronic', 'Mechanical', 'Civil & structural', 'Chemical', 'Aerospace', 'Biomedical', 'Materials science', 'Energy systems', 'Robotics'],
 'Architecture & planning': ['Architectural theory', 'Architectural history', 'Urban planning'],
 'Environment': ['Conservation biology'],
 'Business': ['Strategy', 'Organizational behavior', 'Innovation & entrepreneurship'],
}

# read every data file; a discipline may be split over several files
F = {}
for f in sorted(glob.glob(os.path.join(here, 'data', '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for fl in d['fields']:
        key = (d['discipline'], fl['field']); assert key not in F, key; F[key] = fl

def item(p):
    yr = str(p['year'])
    return {'q': f"{p['authors']} · {yr} · {p['venue']}", 'f': p['title'], 'm': p['why'], 'ml': 'Why it matters',
            'c': f"{p['authors']} ({yr}). {p['title']}. {p['venue']}."}

P, missing = [], []
for gname, gsig, discs in GROUPS:
    g = {'n': gname, 'i': tx(gsig), 'u': [], 't': []}
    for dname, dsig in discs:
        idx = []
        for fname in ORDER[dname]:
            fl = F.pop((dname, fname), None)
            if fl is None: missing.append(f'{dname} / {fname}'); continue
            idx.append(len(g['t']))
            ks = [item(p) for p in fl['papers']]
            xs = [dict(item(p), x=f'{len(P)}.{len(g["t"])}') for p in fl.get('more', [])]
            if xs: xs[0]['x1'] = 1
            g['t'].append({'t': fname, 'p': fl.get('lead', ''), 'n': len(ks), 'k': ks + xs})
        if idx: g['u'].append({'n': dname, 'i': tx(dsig), 't': idx})
    if g['u']: P.append(g)
assert not F, f'unplaced fields: {list(F)}'
if missing: print(f'{len(missing)} fields not in yet:', '; '.join(missing))

n = shell.build(P, os.path.join(here, '..', 'index.html'),
    title='The ten best papers for…', lead='The ten best papers for', key='tb',
    words=['group', 'discipline', 'field', 'paper'], steps=['group', 'discipline', 'field', 'papers'],
    theme='ink', end='', foot='<a class="foot" href="questions.html">By question →</a>',
    sub='<p class="sub">Not each field’s history but where it stands now: the papers today’s research runs on, or is still arguing with. Read the ten and you’re caught up.</p>',
    more='Need more?', morenote='the next ten')
print(f"{sum(len(t['k']) for g in P for t in g['t'])} papers in {sum(len(g['t']) for g in P)} fields, {n // 1024} KB")
