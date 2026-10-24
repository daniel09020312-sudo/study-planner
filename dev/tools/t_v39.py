# v39: 움직이는 이모티콘 팩 3개, 냥댕이는 고양이와 강아지 팩을 모두 사야 보이고 살 수 있다
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T19:00:00+09:00');close_dlg(p)
def ev(js):return p.evaluate('()=>'+js)
def store(k):return json.loads(ev("JSON.stringify(window.__store[%s]||null)"%json.dumps(k)))
def txt(sel):return ev("(e=>e?e.innerText.replace(/\\n/g,' / '):null)(document.querySelector(%s))"%json.dumps(sel))
def clean():
    for _ in range(4):
        p.evaluate("()=>document.querySelectorAll('#notes .note .x').forEach(b=>b.click())");p.wait_for_timeout(250)
p.wait_for_timeout(1200)
ev("(()=>{const S=window.__store;for(let i=2;i<22;i++){const d=new Date(2026,9,21-i),k='days/m1_'+d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');S[k]={goals:[],mins:{s2:120,s3:120}};}window.__fire();return 1})()")
p.wait_for_timeout(500)
click(p,'#shopBtn',700);click(p,'[data-act="shop-cat"][data-v="stk"]',600)
print('packs         :', ev("[...document.querySelectorAll('#shg-stk .shi')].map(e=>e.querySelector('.shn b').textContent).join(' | ')"))
print('hidden card   :', txt('#shi-k-nyang'), '| imgs', ev("document.querySelectorAll('#shi-k-nyang img').length"), '| buy', ev("document.querySelectorAll('#shi-k-nyang [data-act=\"shop-buy\"],#shi-k-nyang [data-act=\"shop-peek\"]').length"))
# 숨은 팩을 억지로 사려고 해도 안 됨
p.evaluate("()=>{for(let i=0;i<2;i++){const b=document.createElement('button');b.setAttribute('data-act','shop-buy');b.setAttribute('data-id','k:nyang');document.body.appendChild(b);b.click();b.remove();}}");p.wait_for_timeout(500)
print('forced buy    :', (store('progress/m1') or {}).get('shop',{}).get('own',{}).get('k:nyang'))
clean();ev("(()=>{const e=document.getElementById('shi-k-nyang');e.scrollIntoView({block:'center'});return 1})()");p.wait_for_timeout(300);p.screenshot(path=SH+'v39_shop_hidden.png')
click(p,'[data-act="shop-buy"][data-id="k:cat"]',300);click(p,'[data-act="shop-buy"][data-id="k:cat"]',800)
print('after cat     :', txt('#shi-k-nyang .sha'))
click(p,'[data-act="shop-buy"][data-id="k:dog"]',300);click(p,'[data-act="shop-buy"][data-id="k:dog"]',800)
print('after dog     :', txt('#shi-k-nyang .shn'), '| buy btn', ev("document.querySelectorAll('#shi-k-nyang [data-act=\"shop-buy\"]').length"))
click(p,'[data-act="shop-peek"][data-id="k:nyang"]',900)
print('peek nyang    :', ev("document.querySelectorAll('#shi-k-nyang .shall .stk').length"), '| loaded', ev("[...document.querySelectorAll('#shi-k-nyang .shall img')].filter(i=>i.complete&&i.naturalWidth>=2880&&i.classList.contains('sa')).length"))
clean();ev("(()=>{const e=document.getElementById('shi-k-nyang');e.scrollIntoView({block:'start'});return 1})()");p.wait_for_timeout(600);p.screenshot(path=SH+'v39_shop_open.png')
close_dlg(p)
# 메시지: 냥댕이 안 산 상태 -> 탭 이름은 그대로(이제 보임), 산 뒤 보내기
click(p,'[data-act="tab"][data-tab="chat"]',900)
if not ev("!!document.getElementById('stkPick')"):click(p,'#msgStk',500)
print('tabs          :', ev("[...document.querySelectorAll('.stkpick .seg button')].map(b=>b.textContent).join(',')"))
click(p,'[data-act="stk-pack"][data-id="cat"]',500)
print('cat grid      :', ev("document.querySelectorAll('.stkgrid [data-act=\"stk-send\"]').length"))
clean();ev("(()=>{const e=document.getElementById('stkPick');if(e)e.scrollIntoView({block:'end'});return 1})()");p.wait_for_timeout(500);p.screenshot(path=SH+'v39_chat_cat.png')
click(p,'[data-act="stk-send"][data-id="cat-09"]',900)
ms=[v for k,v in json.loads(ev("JSON.stringify(window.__store)")).items() if k.startswith('msgs/') and v.get('stk')]
print('sent          :', [m['stk'] for m in ms])
R.close()

# 처음 사람: 비밀 탭
R=Rig()
p=R.open(390,844,ls={'gbb_note':'9999999999999'},now='2026-10-21T19:00:00+09:00');close_dlg(p);p.wait_for_timeout(1200)
click(p,'[data-act="tab"][data-tab="chat"]',900)
if not ev("!!document.getElementById('stkPick')"):click(p,'#msgStk',500)
print('tabs new      :', ev("[...document.querySelectorAll('.stkpick .seg button')].map(b=>b.textContent).join(',')"))
click(p,'[data-act="stk-pack"][data-id="nyang"]',500)
print('secret        :', txt('.stklock'), '| imgs', ev("document.querySelectorAll('.stkgrid img').length"), '| q', ev("document.querySelectorAll('.stkgrid .stkq').length"))
print('seg overflow  :', ev("(s=>s.scrollWidth+'/'+s.clientWidth)(document.querySelector('.stkpick .seg'))"), '| page x', ev("document.documentElement.scrollWidth"))
clean();ev("(()=>{const e=document.getElementById('stkPick');if(e)e.scrollIntoView({block:'end'});return 1})()");p.wait_for_timeout(300);p.screenshot(path=SH+'v39_chat_secret.png')
p.evaluate("()=>{const b=document.createElement('button');b.setAttribute('data-act','stk-send');b.setAttribute('data-id','nyang-01');b.setAttribute('data-chan','all');document.body.appendChild(b);b.click();b.remove();}");p.wait_for_timeout(500)
print('forced send   :', len([1 for k,v in json.loads(ev("JSON.stringify(window.__store)")).items() if k.startswith('msgs/') and str(v.get('stk','')).startswith('nyang')]))
print('errors',R.errors)
R.close()
