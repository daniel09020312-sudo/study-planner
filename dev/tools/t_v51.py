# 예전에 방장이 정한 시작일(집계 시작일 칸이 없던 때)이 있어도 점수는 처음부터 보이고, 그 날짜가 집계 시작일이 된다
import sys,datetime,json
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
def st(p,e):return p.evaluate('()=>'+e)
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
NOW=datetime.datetime(2026,10,28,15,0,0)
R=Rig();p=R.open(1180,820,ls={'gbb_note':'9999999999999'},now=NOW);close_dlg(p)
p.evaluate("()=>{const S=window.__store;S['meta/config'].period={s:'2026-11-02',e:'2026-12-08'};S['days/m1_2026-10-27']={in:'2026-10-27T00:10:00.000Z',mins:{s2:90},goals:[]};window.__fire();}");p.wait_for_timeout(600)
click(p,'[data-act="tab"][data-tab="rank"]',800)
t=st(p,"document.querySelector('#view-rank').innerText")
check('this week points visible',('이 기간에는 아직 점수가 없습니다' not in t),t[:120].replace('\n',' '))
click(p,'#meBtn',600)
check('settings start=10/12 tally=11/2',st(p,"document.getElementById('perS').value")=='2026-10-12' and st(p,"document.getElementById('perA').value")=='2026-11-02',(st(p,"document.getElementById('perS').value"),st(p,"document.getElementById('perA').value")))
print('errors',R.errors);check('no errors',not R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
