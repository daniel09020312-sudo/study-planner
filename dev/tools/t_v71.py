# v73: 수업 알림·잠깐 알림 닫기
import sys,json,re
sys.path.insert(0,'/home/claude/planner/tools')
exec(open('/home/claude/planner/tools/t_v28.py',encoding='utf-8').read().split("p=openat(")[0])
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
PRE_SCH="()=>{const S=window.__store;const p=S['progress/m1']=S['progress/m1']||{};p.tt=p.tt||{};p.tt.sch={p:[{s:510,e:560},{s:570,e:620}],w:{'3':{p0:{s:'s2'},p1:{s:'s3'}}}};window.__fire();}"
p=openat('2026-10-21T08:20:00+09:00',w=1180,h=820)
p.evaluate(PRE_SCH);p.wait_for_timeout(1500)
b0=banner(p);print(b0)
check('class banner shown with close','닫기' in b0 and ev(p,"!!document.querySelector('.schnow [data-act=\"sch-x\"]')"),b0)
p.evaluate("()=>document.querySelector('.schnow [data-act=\"sch-x\"]').click()");p.wait_for_timeout(500)
check('class banner closed',banner(p)=='')
settime(p,'2026-10-21T08:40:00+09:00')
check('same class stays closed',banner(p)=='',banner(p))
settime(p,'2026-10-21T09:25:00+09:00')
check('next class shows again',banner(p)!='',banner(p))
# 잠깐 알림 닫기
p.evaluate("()=>{const b=document.createElement('button');b.dataset.act='adm-ink';document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(300)
check('flash has close',ev(p,"!!document.querySelector('.flash [data-act=\"flash-x\"]')"))
p.evaluate("()=>document.querySelector('.flash [data-act=\"flash-x\"]').click()");p.wait_for_timeout(300)
check('flash closed',ev(p,"!document.querySelector('.flash')"))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
