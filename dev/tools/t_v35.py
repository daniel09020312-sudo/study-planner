# v35: 잉크 선물(방 안), 선물 메시지, 받은 사람 잉크
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T19:00:00+09:00');close_dlg(p)
def ev(js):return p.evaluate('()=>'+js)
def clean():
    for _ in range(4):
        p.evaluate("()=>document.querySelectorAll('#notes .note .x').forEach(b=>b.click())");p.wait_for_timeout(200)
p.wait_for_timeout(1200);clean()
click(p,'#shopBtn',700)
bal0=ev("document.querySelector('.wl b').textContent")
print('balance       :', bal0, '| admin link (artifact)', ev("!!document.querySelector('.admlink')"))
click(p,'[data-act="gift-open"]',500)
print('gift panel    :', ev("[...document.querySelectorAll('#giftPanel .chips:first-of-type .chip')].map(e=>e.textContent).join(',')"), '| button', ev("document.querySelector('[data-act=\"gift-send\"]').textContent"))
click(p,'#giftPanel [data-act="gift-to"][data-id="m2"]',300)
click(p,'#giftPanel [data-act="gift-amt"][data-v="10"]',300)
p.fill('#giftMsg','시험 잘 봐');p.wait_for_timeout(200)
print('ready         :', ev("document.querySelector('[data-act=\"gift-send\"]').textContent"))
clean();p.screenshot(path=SH+'v35_gift.png')
click(p,'[data-act="gift-send"]',300);print('confirm       :', ev("document.querySelector('[data-act=\"gift-send\"]').textContent"))
click(p,'[data-act="gift-send"]',800)
gifts={k:v for k,v in json.loads(ev("JSON.stringify(window.__store)")).items() if k.startswith('gifts/')}
msgs=[v for k,v in json.loads(ev("JSON.stringify(window.__store)")).items() if k.startswith('msgs/') and v.get('gift')]
print('saved         :', list(gifts.values()), '| msg', msgs)
print('flash         :', ev("(document.querySelector('.flash span')||{}).textContent"), '| balance', ev("document.querySelector('.wl b').textContent"), '(was', bal0+')')
# 직접 적기, 모자라면 막힘
click(p,'[data-act="gift-open"]',400);click(p,'#giftPanel [data-act="gift-to"][data-id="m3"]',300)
p.fill('#giftN','99999');p.wait_for_timeout(400)
print('too much      :', ev("(b=>b.textContent+' disabled='+b.disabled)(document.querySelector('[data-act=\"gift-send\"]'))"))
close_dlg(p)
# 받은 사람(m2)으로 보기
R.close()
R=Rig()
q=R.open(390,844,ls={'gbb_note':'9999999999999'},me='m2',now='2026-10-21T19:00:00+09:00');close_dlg(q)
q.evaluate("(g)=>{const S=window.__store;Object.assign(S,g);window.__fire();}",{**gifts,**{('msgs/gx%d'%i):m for i,m in enumerate(msgs)}});q.wait_for_timeout(800)
click(q,'#shopBtn',700)
print('receiver      :', q.evaluate("()=>document.querySelector('.wr small').textContent"))
close_dlg(q)
click(q,'[data-act="tab"][data-tab="chat"]',800)
click(q,'[data-act="chan"][data-id="m1"]',800)
print('dm bubble     :', q.evaluate("()=>(document.querySelector('.bb.gift')||{innerText:''}).innerText.replace(/\\n/g,' / ')"), '| preview', q.evaluate("()=>[...document.querySelectorAll('.chrow small')].map(e=>e.textContent).filter(t=>t.includes('잉크')).join('|')"))
q.screenshot(path=SH+'v35_dm.png')
print('errors',R.errors)
R.close()
