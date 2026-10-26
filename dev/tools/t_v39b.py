# v39: 냥댕이가 열리는 연출, 색 값
import sys,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
W,H=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (390,844)
R=Rig()
PRE="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;var p=S['progress/m1']||{};p.shop={own:{'k:cat':120},gf:1};S['progress/m1']=p;clearInterval(t);},5);})();"
p=R.open(W,H,scheme='dark',ls={'gbb_note':'9999999999999'},now='2026-10-21T19:00:00+09:00',pre=PRE);close_dlg(p);p.wait_for_timeout(1200)
def ev(js):return p.evaluate('()=>'+js)
ev("(()=>{const S=window.__store;for(let i=2;i<22;i++){const d=new Date(2026,9,21-i),k='days/m1_'+d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');S[k]={goals:[],mins:{s2:120,s3:120}};}window.__fire();return 1})()")
p.wait_for_timeout(400)
click(p,'#shopBtn',700);click(p,'[data-act="shop-cat"][data-v="color"]',500)
print('color prices  :', ev("[...new Set([...document.querySelectorAll('#shg-color .shi .shbuy b')].map(b=>b.textContent))].join(',')"))
click(p,'[data-act="shop-cat"][data-v="stk"]',500)
print('before        :', ev("!!document.querySelector('.rv2')"))
click(p,'[data-act="shop-buy"][data-id="k:dog"]',300);click(p,'[data-act="shop-buy"][data-id="k:dog"]',0)
for t,nm in [(700,'a'),(600,'b'),(500,'c'),(1700,'d')]:
    p.wait_for_timeout(t);p.screenshot(path=SH+'v39_rv_%s_%d.png'%(nm,W))
print('overlay       :', ev("(e=>e?e.getAttribute('aria-label'):null)(document.querySelector('.rv2'))"), '| focus', ev("document.activeElement&&document.activeElement.textContent"))
print('flag          :', ev("localStorage.getItem('gbb_rv_nyang')"))
click(p,'.rv2 [data-rv="go"]',900)
print('after go      :', ev("!!document.querySelector('.rv2')"), '| peek', ev("document.querySelectorAll('#shi-k-nyang .shall .stk').length"), '| modal', ev("!!document.getElementById('dlg-shop')"))
close_dlg(p);click(p,'#shopBtn',1500)
print('again         :', ev("!!document.querySelector('.rv2')"))
print('errors',R.errors)
R.close()
