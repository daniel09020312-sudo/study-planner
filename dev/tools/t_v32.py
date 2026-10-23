# 시간표 범위: 새벽 5시 ~ 다음 날 새벽 5시(24시간)
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
T='2026-10-21'
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T15:00:00+09:00');close_dlg(p)
def ev(js):return p.evaluate('()=>'+js)
def store(k):return json.loads(ev("JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
click(p,'[data-act="cal-mode"][data-id="tt"]',900)
print('range        :', ev("(c=>c.dataset.r0+'~'+c.dataset.r1+' h'+c.offsetHeight)(document.getElementById('tc-%s'))"%T))
labs=ev("[...document.querySelectorAll('.tthrs span, .tth span')].map(e=>e.textContent)") or []
print('labels       :', labs[:2], '...', labs[-3:], len(labs))
# 다음 날 새벽 3:30 칸 누르기
xy=p.evaluate("([d,m])=>{const c=document.getElementById('tc-'+d),sc=document.getElementById('ttScroll'),r0=+c.dataset.r0,hh=+c.dataset.hh;document.getElementById('c-tt').scrollIntoView({block:'start'});sc.scrollTop=Math.max(0,(m-r0)*hh/60-170);const r=c.getBoundingClientRect();return [r.left+r.width/2,r.top+(m-r0)*hh/60+5];}",[T,27*60+30])
p.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);e.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:x,clientY:y}));}",xy);p.wait_for_timeout(700)
print('slot title   :', ev("(document.getElementById('dlgT')||{}).textContent"))
gid=ev("(b=>b?b.dataset.id:null)(document.querySelector('#dlg-ttslot [data-act=\"tt-put\"]'))")
if gid:
    click(p,'#dlg-ttslot [data-act="tt-put"][data-id="%s"]'%gid,800)
    g=[x for x in store('days/m1_'+T)['goals'] if x['id']==gid][0];print('placed       :', g.get('ts'), g.get('te'), '(1650~1710)')
p.screenshot(path=SH+'v32_late.png')
print('errors',R.errors)
R.close()
