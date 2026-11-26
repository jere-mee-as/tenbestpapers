import json,re,sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from shell5 import page4
P=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tenbestpapers.json')))
tree=[];units=[];no=0;FP={}
for gi,g in enumerate(P):
    G={'n':g['n'],'i':g.get('i',''),'items':[]}
    for ui,u in enumerate(g['u']):
        no+=1; iid=f'{gi}.{ui}'; G['items'].append({'id':iid,'n':u['n'],'i':''})
        for fi,ti in enumerate(u['t']):
            f=g['t'][ti]; key=f'{no}.{fi+1}  {f["t"]}'; FP[key]=f.get('p','')
            for k in f['k']:
                parts=[p.strip() for p in k.get('q','').split('·')]
                y=next((p for p in parts if re.fullmatch(r'\d{4}',p)),'')
                units.append({'it':iid,'g':key+('  ·  further reading' if k.get('x') else ''),'fk':key,'t':k['f'],'au':parts[0] if parts else '','y':y,'v':parts[-1] if len(parts)>2 else '','m':k.get('m',''),'c':k.get('c',k['f']),'x':1 if k.get('x') else 0})
    tree.append(G)
core=[u for u in units if not u['x']]
site={'tree':tree,'units':units,'noun':['paper','papers'],'LINKS':[['By question →','questions.html'],['So you want to understand →','https://jere-mee-as.github.io/understanding/']],'FP':FP,'by':'discipline',
 'INTRO':'For every field, the ten papers today’s research runs on. Read them and you’re caught up.'}
theme=r'''
:root{--bg:#fdfdfb;--fg:#141414;--fg2:#2a2a2a;--dim:#5f5f5f;--line:#e0dfda;--line2:#ecebe6;--acc:#b31b1b;--hov:#f6f5f0;--sel:#fbf3e9;--hl:#fff3a8;--panel:#f7f6f2;--bar:#fdfdfb;
--display:"STIX Two Text",Times,serif;--text:"STIX Two Text",Times,serif;--dispw:600}
body{font-size:15.5px}#say{font-size:25px}
.pr{display:grid;grid-template-columns:44px minmax(0,1fr);gap:12px;align-items:baseline}
.pr .ti{font-style:italic;font-size:15.5px;line-height:1.35}
.pr .au{display:block;font-size:13px;color:var(--dim);font-variant:small-caps;letter-spacing:.02em}
.row.x .ti{color:var(--fg2)}
.sub{font-size:15px}
.d h3{font:italic 400 20px/1.3 var(--text)}
.d .cite{font-size:14px;color:var(--dim)}
.d .why{font-size:15.5px;line-height:1.55}
.fp{font-size:14px;color:var(--fg2)}
.nw .pr{padding:6px 0;border-bottom:1px solid var(--line2);width:100%;text-align:left}.nw button:hover .ti{color:var(--acc)}
'''
js=r'''
SITE.BLOB=u=>[u.g,u.t,u.au,u.y,u.v,u.m].join(' ');
SITE.COUNT=u=>!u.x;
SITE.SAY=(it,u,q)=>q?`The ten best papers on “${esc(q)}”`:!it?'The ten best papers for…':`The ten best papers for <b>${esc(it.n)}</b>`;
SITE.ROW=(u,Q)=>`<div class="pr"><span class="m">${u.y}</span><span><span class="ti">${hl(u.t,Q)}</span>${cpb(u.c)}<span class="au">${hl(u.au,Q)}</span></span></div>`;
SITE.DETAIL=(u,Q)=>`<h3>${hl(u.t,Q)}</h3><p class="cite">${esc(u.au)} (${esc(u.y)})${u.v?'. '+esc(u.v):''}.${cpb(u.c)}</p>${u.m?lab('Why it matters')+`<p class="why">${hl(u.m,Q)}</p>`:''}${SITE.FP[u.fk]?lab('Where the field stands')+`<p class="fp">${hl(SITE.FP[u.fk],Q)}</p>`:''}`;
SITE._H=it=>{const fs=[...new Set((BY[it.id]||[]).filter(u=>!u.x).map(u=>u.fk))];return `<p class="lead">${fs.length} field${fs.length==1?'':'s'}, ten core papers each, then further reading.</p>`};
SITE.FEATURE=()=>{const N=SITE.units.filter(u=>!u.x&&u.y).sort((a,b)=>b.y-a.y).slice(0,10);
 return `<h3>The newest papers on the lists</h3><div class="nw">${N.map(u=>`<button class="pr" data-jump="${u.ix}"><span class="m">${u.y}</span><span><span class="ti">${esc(u.t)}</span><span class="au">${esc(u.au)} · ${esc(ITEMS[u.it].n)}</span></span></button>`).join('')}</div>`};
'''
page4('tenbestpapers','The ten best papers for…','family=STIX+Two+Text:ital,wght@0,400;0,600;0,700;1,400',theme,site,js)
