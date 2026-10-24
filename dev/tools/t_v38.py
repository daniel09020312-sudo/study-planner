# v38: 그제 이전 할 일도 완료 표시와 늦은 인증
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
def ev(p,js):return p.evaluate('()=>'+js)
def store(p,k):return json.loads(ev(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
YY='2026-10-17'
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['days/m1_2026-10-17']={goals:[{id:'go1',text:'나흘 전 할 일',sid:'s2',done:false},{id:'go2',text:'나흘 전 둘째',sid:'s3',done:false}]};clearInterval(t);},5);})();"
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T19:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(1500)
p.evaluate("(d)=>{const b=document.createElement('button');b.setAttribute('data-act','pick-date');b.setAttribute('data-d',d);document.body.appendChild(b);b.click();b.remove();}",YY);p.wait_for_timeout(800)
print('chk enabled   :', ev(p,"[...document.querySelectorAll('#c-goals .chk')].map(b=>!b.disabled).join(',')"))
click(p,'[data-act="goal-toggle"][data-date="%s"][data-id="go1"]'%YY,600);click(p,'[data-act="goal-toggle"][data-date="%s"][data-id="go2"]'%YY,600)
print('done          :', [g.get('done') for g in store(p,'days/m1_'+YY)['goals']])
print('cert box      :', ev(p,"(e=>e?e.innerText.replace(/\\n/g,' / '):null)(document.querySelector('#c-goals .cert'))"))
click(p,'#c-goals [data-act="cert"][data-date="%s"]'%YY,700)
print('cert          :', bool(store(p,'days/m1_'+YY).get('certAt')), '|', ev(p,"(document.querySelector('#c-goals .cert .hint')||{}).textContent"))
# 할 일 더하기는 여전히 막힘: 저장소에 직접 새 할 일을 넣어 보내도 guardDay가 빼야 함
p.evaluate("(d)=>{const b=document.createElement('button');b.setAttribute('data-act','pick-date');b.setAttribute('data-d','2026-10-25');document.body.appendChild(b);b.click();b.remove();}",YY);p.wait_for_timeout(500)
print('future chk    :', ev(p,"[...document.querySelectorAll('#c-goals .chk')].map(b=>b.disabled).join(',')||'none'"))
print('errors',R.errors)
R.close()
