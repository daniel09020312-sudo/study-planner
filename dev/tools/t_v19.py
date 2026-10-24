import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
def st(p,e):return p.evaluate('()=>'+e)
def store(p,k):return json.loads(st(p,"JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
R=Rig()
p=R.open(1180,820,ls={'gbb_note':'9999999999999'});close_dlg(p)
T=st(p,"(()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})()")
Y=st(p,"(()=>{const d=new Date();d.setDate(d.getDate()-1);return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})()")
def score_rows():
    click(p,'[data-act="open"][data-modal="score"]',500)
    r=st(p,"[...document.querySelectorAll('#dlg-score .brk li')].map(l=>l.innerText.split(String.fromCharCode(10)).join(' ')).join(' | ')")
    h=st(p,"(document.querySelector('#dlg-score .hint')||{}).textContent")
    click(p,'#dlg-score [data-act="modal-close"]',400)
    return r,h
print('today goals  :',[(g['text'][:8],g['done']) for g in store(p,'days/m1_'+T)['goals']])
print('score before :',score_rows())
# 모두 끝내기
for gid in [g['id'] for g in store(p,'days/m1_'+T)['goals'] if not g['done']]:
    click(p,'#g-%s .chk'%gid,350)
print('cert hint    :',st(p,"(document.querySelector('.cert .hint')||{}).textContent"))
click(p,'[data-act="cert"][data-date="%s"]'%T,800)
st(p,"(()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b)b.click();})()");p.wait_for_timeout(400)
print('cert done    :',st(p,"[...document.querySelectorAll('.cert .hint')].map(e=>e.textContent).join(' / ')"))
print('score after  :',score_rows())
# 어제: 삭제 단추 없음, 완료 표시는 마감 뒤에도 됨(v37)
p.evaluate("(d)=>{const b=document.querySelector('.cal [data-act=pick-date][data-d=\"'+d+'\"]')||document.querySelector('[data-act=pick-date][data-d=\"'+d+'\"]');if(b)b.click();}",Y);p.wait_for_timeout(700)
print('picked       :',st(p,"(document.querySelector('.daycol')||{}).id"))
yg=[g for g in store(p,'days/m1_'+Y)['goals']]
undone=[g for g in yg if not g['done']]
print('yesterday    :',[(g['text'][:8],g['done']) for g in yg])
if undone:
    gid=undone[0]['id']
    print('chk disabled :',st(p,"(b=>b?b.disabled:'none')(document.querySelector('#g-%s .chk'))"%gid))
    click(p,'#g-%s .gmore'%gid,400)
    print('menu         :',st(p,"[...document.querySelectorAll('#ga-%s button, #ga-%s .gpast')].map(b=>b.textContent).join(',')"%(gid,gid)))
    # 오늘로 옮기기 -> 어제에는 '옮김'으로 남음
    b=st(p,"!!document.querySelector('#ga-%s [data-act=\"g-tomorrow\"],#ga-%s [data-act=\"g-today\"]')"%(gid,gid))
    click(p,'#ga-%s [data-act="g-tomorrow"], #ga-%s [data-act="g-today"]'%(gid,gid),800)
    print('after move   : Y',[(g['text'][:8],g['done'],g.get('mv')) for g in store(p,'days/m1_'+Y)['goals']],'| T has',gid in [g['id'] for g in store(p,'days/m1_'+T)['goals']])
    print('ghost shown  :',st(p,"!!document.getElementById('g-%s-mv')"%gid) or st(p,"document.querySelectorAll('.goal.mv').length"))
    p.screenshot(path=SH+'v19_ghost.png')
    # 되돌리기
    click(p,'.flash [data-act="undo"], .flash button',800)
    print('after undo   : Y',[(g['text'][:8],g['done'],g.get('mv')) for g in store(p,'days/m1_'+Y)['goals']])
print('score Y      :',st(p,"0"))
print('errors',R.errors)
# 할 일 숨기기
click(p,'#meBtn',600)
print('hide setting :',st(p,"[...document.querySelectorAll('[data-act=hide-goals]')].map(b=>b.textContent+':'+b.getAttribute('aria-pressed')).join(',')"))
click(p,'[data-act="hide-goals"][data-v="1"]',600)
print('saved hide   :',store(p,'progress/m1').get('hideGoals'))
st_=st(p,"JSON.stringify(window.__store)")
q=R.open(1180,820,ls={'gbb_note':'9999999999999','gbb_me':'m2'},pre="window.__SEED=%s;"%st_);close_dlg(q)
q.evaluate("()=>{Object.assign(window.__store,window.__SEED);window.__fire&&window.__fire();}");q.wait_for_timeout(600)
click(q,'[data-act="tab"][data-tab="room"]',900)
click(q,'#fr-m1 [data-act="fr-toggle"]',500)
print('m2 sees m1   :',st(q,"(document.getElementById('fg-m1')||{}).textContent"))
click(q,'#fr-m5 [data-act="fr-toggle"]',500)
print('m2 sees m5   :',st(q,"(document.getElementById('fg-m5')||{}).textContent")[:60])
print('errors',R.errors)
R.close()
