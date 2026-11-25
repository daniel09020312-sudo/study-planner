# v110 할 순서 정하기: 누른 순서로 줄이 바뀌고 남은 할 일 앞에 번호, 다 고르면 저절로 저장, 번호 없애기, 되돌리기
import sys,datetime
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def ev(p,js):return p.evaluate('()=>'+js)
SC='/tmp/claude-0/-home-user/e7c3557b-cbdd-5867-afb0-e8d2fce386ea/scratchpad/'
T='2026-11-25'
def g(i,t,d=False):return "{id:'q%d',text:'%s',sid:'s%d',done:%s}"%(i,t,i,'true' if d else 'false')
pre="(function(){var t=setInterval(function(){var S=window.__store;if(!S)return;S['days/m1_%s']={goals:[%s,%s,%s,%s],in:'%sT00:10:00.000Z'};clearInterval(t);},2);})();"%(T,g(1,'영어 단어'),g(2,'수학 문제집'),g(3,'국어 복습',True),g(4,'화학 개념'),T)
R=Rig();p=R.open(390,844,ls={'gbb_note':'9999999999999'},now=datetime.datetime(2026,11,25,15,0,0),pre=pre);close_dlg(p);p.wait_for_timeout(500)
click(p,'[data-act="tab"][data-tab="cal"]',700)
def ids():return ev(p,"(window.__store['days/m1_%s'].goals||[]).map(g=>g.id).join(',')"%T)
check('chip',ev(p,"!!document.querySelector('[data-act=g-num]')"))
check('no numbers yet',ev(p,"!document.querySelector('#c-goals .gno')"))
click(p,'[data-act="g-num"]',400)
check('bar shown',ev(p,"!!document.querySelector('.gnbar')"))
check('only undone rows',ev(p,"document.querySelectorAll('#c-goals .gnrow').length")==3)
click(p,'button.gnb[data-id="q4"]',250);click(p,'button.gnb[data-id="q2"]',250)
check('numbers while picking',ev(p,"[...document.querySelectorAll('.gnb.on')].map(b=>b.textContent).join(',')")=='2,1'.replace('2,1','2,1'),ev(p,"[...document.querySelectorAll('.gnb')].map(b=>b.dataset.id+':'+b.textContent).join(',')"))
click(p,'button.gnb[data-id="q2"]',250);check('tap again removes',ev(p,"document.querySelectorAll('.gnb.on').length")==1)
click(p,'button.gnb[data-id="q2"]',250)
click(p,'[data-act="g-numsave"]',600)
check('order saved',ids()=='q4,q2,q1,q3',ids())
check('ord flag',ev(p,"window.__store['days/m1_%s'].ord===1"%T))
check('badges',ev(p,"[...document.querySelectorAll('#c-goals .gno')].map(b=>b.textContent).join(',')")=='1,2,3')
check('first highlighted',ev(p,"!!document.querySelector('#g-q4 .gno.n1')"))
p.query_selector('#c-goals').screenshot(path=SC+'gn1.png')
click(p,'[data-act="g-num"]',300);click(p,'button.gnb[data-id="q2"]',250);p.query_selector('#c-goals').screenshot(path=SC+'gn0.png');click(p,'[data-act="g-numx"]',300)
# 다시 정하기: 다 고르면 저절로 저장
click(p,'[data-act="g-num"]',400)
for i in ['q1','q4','q2']:click(p,'button.gnb[data-id="%s"]'%i,250)
p.wait_for_timeout(400)
check('auto save when all picked',ids()=='q1,q4,q2,q3' and not ev(p,"!!document.querySelector('.gnbar')"),ids())
# 끝내면 번호가 앞으로 당겨짐
click(p,'#g-q1 .chk',600)
check('renumber after done',ev(p,"[...document.querySelectorAll('#c-goals .gno')].map(b=>b.closest('li').id+':'+b.textContent).join(',')")=='g-q4:1,g-q2:2')
# 번호 없애기
click(p,'[data-act="g-num"]',400);click(p,'[data-act="g-numoff"]',600)
check('numbers off',ev(p,"!document.querySelector('#c-goals .gno')")and ev(p,"!window.__store['days/m1_%s'].ord"%T))
print('errors',R.errors);check('no errors',not R.errors,R.errors)
R.close();print('ALL OK' if ok else 'SOME FAILED')
