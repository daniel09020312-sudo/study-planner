# v93: 스터디 빙고 주마다 다른 칸(11/16 주부터), 이번 주(11/9 주)는 그대로
import sys
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
ok=True
def check(n,c,x=''):
    global ok
    print(('OK  ' if c else 'FAIL'),n,x)
    if not c: ok=False
def cells(now):
    R=Rig();p=R.open(1280,1000,ls={'gbb_note':'9999999999999'},now=now+'T10:00:00+09:00');close_dlg(p);p.wait_for_timeout(500)
    click(p,'[data-act="tab"][data-tab="play"]',700)
    c=p.evaluate("()=>[...document.querySelectorAll('.bcell span')].map(e=>e.textContent)")
    if not c:c=p.evaluate("()=>{var s=document.querySelector('[id^=\"c-bingo-\"]');return s?[...s.querySelectorAll('li,button,div')].filter(e=>e.children.length<=3&&/\\d/.test(e.textContent)).slice(0,0):[]}")
    err=R.errors;R.close();return c,err
OLD=['2시간 넘게 공부한 날 7일']
A,e=cells('2026-11-15');a=A;print('11/9 week',a)
w=[cells(d) for d in ['2026-11-16','2026-11-23','2026-11-30','2026-12-07']]
for d,(c,er) in zip(['11/16','11/23','11/30','12/07'],w):print(d,c,er)
check('9 cells each week',all(len(c)==9 for c,_ in w) and len(a)==9,[len(c) for c,_ in w])
check('weeks differ',len(set(tuple(c) for c,_ in w))==4)
check('no every-day cells in new weeks',not any('7일' in t for c,_ in w for t in c))
pairs=[('이번 주 공부 25시간','이번 주 공부 18시간'),('할 일 25개 완료','할 일 15개 완료'),('100점 넘긴 날 3일','120점 넘긴 날 2일')]
check('no same-kind pairs',not any(a in c and b in c for c,_ in w for a,b in pairs))
check('this week unchanged',a==['타이머로만 20시간', '할 일 30개 완료', '주말에 10시간 공부', '120점 넘긴 날 2일', '2시간 넘게 공부한 날 7일', '하루 순위 1등 2번', '할 일을 모두 끝낸 날 5일', '한 과목 8시간', '인증 7일'])
check('no errors',not e and not any(er for _,er in w))
print('ALL OK' if ok else 'SOME FAILED')
