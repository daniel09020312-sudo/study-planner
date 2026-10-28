import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,28,10,0,0)
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate("()=>{const S=window.__store;Object.keys(S).filter(k=>k.startsWith('duels/')).forEach(k=>delete S[k]);window.__fire();}");p.wait_for_timeout(300)
click(p,'#navMore',300);click(p,'.mitem[data-tab="play"]',700)
click(p,'[data-act="play-tab"][data-id="duel"]',600)
click(p,'[data-act="open"][data-modal="duel"]',600)
check('kind chips',st(p,"document.querySelectorAll('.dialog [data-k=\"kind\"]').length")==3)
check('len chips',st(p,"document.querySelectorAll('.dialog [data-k=\"len\"]').length")==3)
click(p,'.dialog [data-k="b"] >> nth=0',200) if False else None
p.locator('.dialog [data-k="b"]').last.click();p.wait_for_timeout(200)
p.locator('.dialog [data-v="time"]').click();p.wait_for_timeout(200)
p.locator('.dialog [data-k="len"][data-v="3"]').click();p.wait_for_timeout(200)
click(p,'[data-act="duel-add"]',600)
print('flash',st(p,"(document.querySelector('.flash')||{}).textContent"));ds=json.loads(st(p,"JSON.stringify(Object.fromEntries(Object.entries(window.__store).filter(e=>e[0].startsWith('duels/')).map(e=>[e[0].slice(6),e[1]])))"))
did=[k for k,v in ds.items() if v.get('kind')]
did=did[0] if did else ''
d=ds.get(did,{})
check('duel saved with kind/days',d.get('kind')=='time' and d.get('days')==3,d)
# 상대가 수락 -> 3일 공부 시간 비교
p.evaluate("(id)=>{const S=window.__store;const d=S['duels/'+id];d.status='on';d.start='2026-10-26';d.days=3;S['days/'+d.a+'_2026-10-27']={in:'x',mins:{s2:90},goals:[]};S['days/'+d.b+'_2026-10-27']={in:'x',mins:{s2:30},goals:[]};window.__fire();}",did);p.wait_for_timeout(600)
txt=st(p,"(document.querySelector('.duel')||{}).innerText")
check('time duel shows hours',('시간' in txt) and ('분' in txt),txt.replace('\n',' | '))
check('kind label',('공부 시간' in txt) and ('3일' in txt))
# 다 끝난 대결: 다시 붙기
p.evaluate("(id)=>{const S=window.__store;S['duels/'+id].start='2026-10-20';window.__fire();}",did);p.wait_for_timeout(500)
check('rematch button',st(p,"!!document.querySelector('[data-modal=\"duel\"][data-kind]')"))
click(p,'[data-modal="duel"][data-kind]',500)
check('rematch prefilled',st(p,"document.querySelector('.dialog [data-k=\"kind\"][aria-pressed=\"true\"]').dataset.v")=='time')
# 패드 폭
for w,exp in [(560,8),(390,4)]:
    q=R.open(w,900,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(q)
    vis=st(q,"[...document.querySelectorAll('.navs > button')].filter(b=>getComputedStyle(b).display!=='none').length")
    check('nav buttons at %d'%w,vis==exp,vis)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
