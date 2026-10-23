import sys,os
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
R=Rig()
def look(p):
    return p.evaluate("()=>{const r=document.documentElement,cs=getComputedStyle(r);return [r.getAttribute('data-concept'),r.getAttribute('data-theme'),r.getAttribute('data-mode'),r.getAttribute('data-font'),cs.getPropertyValue('--bg').trim(),cs.getPropertyValue('--accent').trim(),cs.getPropertyValue('--accent-ink').trim(),cs.colorScheme].join(' | ')}")
p=R.open();close_dlg(p)
p.evaluate("()=>{window.__store['progress/m1']=Object.assign({},window.__store['progress/m1']||{},{shop:{gf:1,own:{'k:playful':120,'k:emotions':120,'c:grid':150,'c:board':200,'c:pop':150,'c:line':100,'c:glass':200,'c:night':250,'a:p-mint':50}}});window.__fire();}");p.wait_for_timeout(400)  # 상점에서 산 것으로
print('start        :',look(p))
click(p,'#meBtn',500)
for c in ['board','grid','pop','glass','night','line','basic']:
    click(p,f'[data-act="concept"][data-v="{c}"]',700)
    print(c.ljust(13)+':',look(p),'| brightness chips:',p.evaluate("()=>document.querySelectorAll('[data-act=\"theme\"]').length"))
click(p,'[data-act="accent"][data-v="p-mint"]',200);click(p,'[data-act="theme"][data-v="dark"]',300)
print('mint+dark    :',look(p))
click(p,'[data-act="theme"][data-v="auto"]',300);print('auto         :',look(p))
# 보는 앱(호스트)이 테마를 바꿀 때
p.evaluate("()=>document.documentElement.setAttribute('data-theme','dark')");p.wait_for_timeout(300);print('host -> dark :',look(p))
p.evaluate("()=>document.documentElement.removeAttribute('data-theme')");p.wait_for_timeout(300);print('host -> none :',look(p))
p.reload();p.wait_for_timeout(1500);print('after reload :',look(p))
p.close()
# 기기가 어두운 모드일 때
p=R.open(scheme='dark',ls={'gbb_accent':'p-pink'});close_dlg(p);print('OS dark+pink :',look(p));p.close()
# 글꼴을 못 불러올 때
os.environ['NOFONT']='1'
p=R.open(ls={'gbb_concept':'grid'});close_dlg(p);print('no font grid :',look(p),'| h1 size:',p.evaluate("()=>getComputedStyle(document.querySelector('.vhead h1')).fontSize+' '+getComputedStyle(document.querySelector('.vhead h1')).fontWeight"));p.close()
print('errors:',R.errors);R.close()
