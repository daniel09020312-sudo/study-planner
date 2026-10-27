import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,11,20,12,0,0)
def seed(mins):
    return "(M)=>{const S=window.__store;M.forEach((m,i)=>{const d=new Date(2026,10,10+i);const k=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');S['days/m1_'+k]={goals:[],mins:{s2:m},in:k+'T00:10:00.000Z'};});window.__fire();}"
R=Rig()
# 6일만(하루는 8시간 정각) -> 안 뜸
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate(seed(""),[430,440,450,470,420,480,455]);p.wait_for_timeout(1500)
check('no egg when a day is 8h',not st(p,"!!document.querySelector('#dlg-egg')"))
# 7일 모두 7시간대 -> 뜸
q=R.open(390,844,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(q)
q.evaluate(seed(""),[430,440,450,470,420,479,455]);q.wait_for_timeout(1800)
check('egg shows',st(q,"!!document.querySelector('#dlg-egg')"))
click(q,'[data-act="egg-x"] >> nth=0' if False else '#dlg-egg .btn',700)
check('egg closes and remembered',st(q,"!document.querySelector('#dlg-egg')") and st(q,"!!localStorage.getItem('gbb_egg7')"))
q.wait_for_timeout(1200)
check('not shown again',st(q,"!document.querySelector('#dlg-egg')"))
for w,exp in [(390,'grid'),(520,'none'),(700,'none'),(820,'none'),(1180,'none')]:
    r=R.open(w,900,ls={'gbb_note':'9999999999999'});close_dlg(r)
    d=r.evaluate("()=>getComputedStyle(document.getElementById('navMore')).display")
    check('navMore at %d'%w,d==exp,d)
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
