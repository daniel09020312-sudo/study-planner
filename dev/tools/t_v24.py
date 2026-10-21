import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
SEED=open('/home/claude/planner/tools/t_v23.py').read().split('SEED="""')[1].split('"""')[0]
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999'});close_dlg(p);p.evaluate(SEED);p.wait_for_timeout(700)
chips=lambda pg:st(pg,"[...document.querySelectorAll('.cell .sev')].map(i=>i.textContent).join(',')")
print('default      :',chips(p))
print('legend       :',st(p,"(document.querySelector('.calleg')||{}).innerText.split(String.fromCharCode(10)).join(' ')"))
click(p,'[data-act="abbr-open"]',700)
print('tab          :',st(p,"(document.querySelector('.ttsets button[aria-pressed=true]')||{}).textContent"),'| inputs',st(p,"document.querySelectorAll('#dlg-ttset .abin input').length"),'| ph',st(p,"[...document.querySelectorAll('#dlg-ttset .abin input')].map(i=>i.placeholder).join(',')"))
p.fill('#dlg-ttset .abin input[data-id="s5"]','화반');p.dispatch_event('#dlg-ttset .abin input[data-id="s5"]','change');p.wait_for_timeout(500)
p.locator('#dlg-ttset').screenshot(path=SH+'v24_abbr.png')
click(p,'#dlg-ttset [data-act="modal-close"]',600)
print('after        :',chips(p),'| saved',json.loads(st(p,"JSON.stringify(window.__store['progress/m1'].abbr)")))
st_=st(p,"JSON.stringify(window.__store)")
q=R.open(1180,820,ls={'gbb_note':'9999999999999','gbb_me':'m2'},pre="window.__SEED=%s;"%st_);close_dlg(q)
q.evaluate("()=>{Object.assign(window.__store,window.__SEED);window.__fire&&window.__fire();}");q.wait_for_timeout(600)
print('m2 sees own  :',chips(q)[:80],'(공유된 것만, 기본 줄임말)')
print('errors',R.errors)
R.close()
