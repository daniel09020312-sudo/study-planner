# v61: 마감 뒤 인증은 3점만, 점수 팝업은 순위 보너스 변화 제외
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
def run(now,d,others=''):
    R=Rig()
    PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['meta/config'].certHour=29;S['meta/config'].migCert5=1;S['days/m1_%s']={in:'%sT00:10:00.000Z',goals:[{id:'a',text:'1',sid:'s2',done:true},{id:'b',text:'2',sid:'s2',done:true},{id:'c',text:'3',sid:'s2',done:true}]};%sclearInterval(t);},5);})();"%(d,d,others)
    p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=now,pre=PRE);close_dlg(p);p.wait_for_timeout(1200)
    p.evaluate("()=>{window.__pops=[];new MutationObserver(m=>m.forEach(r=>r.addedNodes.forEach(n=>{if(n.className&&String(n.className).indexOf('pop')>=0)window.__pops.push(n.textContent);}))).observe(document.body,{childList:true,subtree:true});}")
    hint=ev(p,"[...document.querySelectorAll('.cert .hint')].map(e=>e.textContent).join(' | ')")
    click(p,'[data-act="cert"][data-date="%s"]'%d,900)
    r=(ev(p,"window.__pops"),hint,R.errors);R.close();return r
pops,hint,err=run('2026-10-30T21:00:00+09:00','2026-10-30')
check('on time today +60',pops==['+60점'],pops)
pops,hint,err=run('2026-10-31T06:00:00+09:00','2026-10-30')
check('late cert only +3',pops==['+3점'],pops)
check('late hint says 3 only','3점' in hint and '20점' not in hint,hint)
# 어제 마감 전 인증으로 하루 순위가 바뀌어도 팝업은 인증 점수만(10+50)
pops,hint,err=run('2026-10-31T01:00:00+09:00','2026-10-30',"S['days/m2_2026-10-30']={in:'2026-10-30T00:10:00.000Z',mins:{s2:120}};")
check('pop excludes rank bonus change',pops==['+60점'],pops)
check('no errors',not err,err)
print('ALL OK' if ok else 'SOME FAILED')
