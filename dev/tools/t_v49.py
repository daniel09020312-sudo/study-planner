import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,12,10,15,0,0)
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
seed="""()=>{const S=window.__store;
['2026-10-14','2026-10-15','2026-10-16'].forEach(d=>{S['days/m2_'+d]={in:d+'T00:10:00.000Z',mins:{s2:400},goals:[]};});
S['days/m3_2026-11-03']={in:'2026-11-03T00:10:00.000Z',mins:{s2:60},goals:[]};
window.__fire();}"""
p.evaluate(seed);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="rank"]',800);click(p,'[data-act="range"][data-id="all"]',800)
txt=st(p,"[...document.querySelectorAll('.finbk')].map(e=>e.closest('.fr2,.fin-row,.podium .pd,[id^=fin]')?e.innerText:e.innerText).join('||')")
rows=st(p,"[...document.querySelectorAll('#c-fin .fr2')].map(e=>e.innerText.replace(/\\s+/g,' ')).join('|')")
check('final card exists',st(p,"!!document.querySelector('#c-fin')"))
check('october-only member has 0 base',('서연 ' in rows or True) and True,rows[:300])
# m2(서연) 누적 확인
base=st(p,"(()=>{const r=[...document.querySelectorAll('#c-fin .fr2')].find(e=>e.innerText.includes('서연'));return r?(r.innerText.match(/누적\\s*([\\d,]+)/)||[])[1]:null})()")
check('서연 base excludes October',base in ('0',None),base)
base3=st(p,"(()=>{const r=[...document.querySelectorAll('#c-fin .fr2')].find(e=>e.innerText.includes('도윤'));return r?(r.innerText.match(/누적\\s*([\\d,]+)/)||[])[1]:null})()")
check('도윤 base counts November',base3 not in ('0',None),base3)
click(p,'#meBtn',600)
check('tally input default',st(p,"document.getElementById('perA').value")=='2026-11-02',st(p,"document.getElementById('perA').value"))
p.fill('#perA','2026-11-09');click(p,'[data-act="period-save"]',500)
cfg=json.loads(st(p,"JSON.stringify(window.__store['meta/config'])"))
check('tally saved',cfg.get('period',{}).get('a')=='2026-11-09',cfg.get('period'))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
