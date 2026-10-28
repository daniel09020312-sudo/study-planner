# 다른 방에서 가져오기: 고정 일정과 학교 시간표를 따로 고르고, 학교 시간표가 이미 있으면 바꿀 수도 있다
import os
os.environ['LIGHT']='1'
src=open('/home/claude/planner/tools/t_carry.py',encoding='utf-8').read()
exec(src.split("# 세 번째: 가져올 것이 없음")[0])
def tgt():
    d=get_at('/rooms/'+RD+'/d/progress/m2') or {}
    return (d.get('tt') or {})
def optstate(k): return ev(P,"document.querySelector('#dlg-carry [data-k=\"%s\"]').getAttribute('aria-pressed')"%k)
tt0=tgt(); w0=(tt0.get('sch') or {}).get('w')
print('first import school:', bool(w0))
# 원본 학교 시간표를 바꾸고 다시 가져오기
STORE['rooms'][RS]['d']['progress']['m1']['tt']['sch']['w']['2']={'p0':{'t':'체육'}}
click(P, '#meBtn', 700); click(P, '.rmact.cr', 600); click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500)
print('sch default when exists:', optstate('sch'), '| label:', ev(P,"document.querySelector('#dlg-carry [data-k=\"sch\"] small').textContent"))
click(P, '#dlg-carry [data-act="cr-opt"][data-k="tt"]', 300)
click(P, '#dlg-carry [data-act="cr-opt"][data-k="sch"]', 300)
click(P, '#dlg-carry [data-act="cr-opt"][data-k="goal"]', 200); click(P, '#dlg-carry [data-act="cr-opt"][data-k="ev"]', 200); click(P, '#dlg-carry [data-act="cr-opt"][data-k="prog"]', 200); click(P, '#dlg-carry [data-act="cr-opt"][data-k="sub"]', 200)
print('go enabled:', ev(P,"!document.querySelector('[data-act=\"cr-go\"]').disabled"))
click(P, '[data-act="cr-go"]', 1800)
print('tgt keys', list(tgt().keys()), 'flash', ev(P,"(document.querySelector('.flash')||{}).textContent")); w1=(tgt().get('sch') or {}).get('w') or {}
keys=sorted((w1 if isinstance(w1,dict) else {i:x for i,x in enumerate(w1) if x}).keys(), key=str)
print('school after replace days:', keys, '| has 체육:', '체육' in str(w1))
print('errors', errors)
