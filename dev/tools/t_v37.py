# v37: 인증 마감 새벽 5시, 어제 할 일은 마감 뒤에도 완료 표시, 늦은 인증 점수
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
def ev(p,js):return p.evaluate('()=>'+js)
def store(p,k):return json.loads(ev(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
def clean(p):
    for _ in range(4):p.evaluate("()=>document.querySelectorAll('#notes .note .x').forEach(b=>b.click())");p.wait_for_timeout(150)
Y,YY='2026-10-20','2026-10-19'
PRE="(function(){var k=0;var t=setInterval(function(){var S=window.__store;if(!S)return;var d=S['days/m1_2026-10-20'];if(d){delete d.certAt;}S['days/m1_2026-10-19']={goals:[{id:'go1',text:'그제 할 일',sid:'s2',done:false}]};clearInterval(t);},5);})();"
# ---- 새벽 4시 30분: 아직 마감 전
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T04:30:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(1500);clean(p)
print('migrated      :', {k:(store(p,'meta/config') or {}).get(k) for k in ('certHour','migCert5')})
print('04:30 banner  :', ev(p,"[...document.querySelectorAll('.cert .what b')].map(e=>e.textContent).join(' | ')"), '|', ev(p,"(document.querySelector('.cert .hint')||{}).textContent"))
R.close()
# ---- 아침 8시: 마감 뒤
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T08:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(1500);clean(p)
print('08:00 banner  :', ev(p,"(e=>e?e.innerText.replace(/\\n/g,' / '):null)(document.querySelector('.cert.late'))"))
p.screenshot(path=SH+'v37_late.png')
click(p,'.cert.late [data-act="pick-date"]',800)
yg=store(p,'days/m1_'+Y)['goals']
print('yesterday     : chk disabled', ev(p,"[...document.querySelectorAll('#c-goals .chk')].map(b=>b.disabled).join(',')"))
undone=[g for g in yg if not g.get('done')][0]
click(p,'[data-act="goal-toggle"][data-date="%s"][data-id="%s"]'%(Y,undone['id']),700)
print('toggle done   :', [g.get('done') for g in store(p,'days/m1_'+Y)['goals']], '| flash', ev(p,"(document.querySelector('.flash span')||{}).textContent"))
click(p,'[data-act="cert"][data-date="%s"]'%Y,700)
d=store(p,'days/m1_'+Y);print('cert          :', bool(d.get('certAt')), '| hint', ev(p,"(document.querySelector('.cert .hint')||{}).textContent"))
# 그제는 그대로 막힘
click(p,'[data-act="pick-date"][data-d="%s"]'%YY,800) if ev(p,"!!document.querySelector('[data-act=\"pick-date\"][data-d=\"%s\"]')"%YY) else ev(p,"0")
p.evaluate("(d)=>{const b=document.createElement('button');b.setAttribute('data-act','goal-toggle');b.setAttribute('data-date',d);b.setAttribute('data-id','go1');document.body.appendChild(b);b.click();b.remove();}",YY);p.wait_for_timeout(600)
print('2 days ago    :', [g.get('done') for g in store(p,'days/m1_'+YY)['goals']], '| flash', ev(p,"(document.querySelector('.flash span')||{}).textContent"))
# 어제 할 일 더하기는 예전처럼 막힘(완료 표시만 됨)
print('errors',R.errors)
R.close()
