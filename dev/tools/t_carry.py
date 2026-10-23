# 다른 방에서 내 것 가져오기: 가짜 Firebase에 방 두 개를 두고 확인한다.
# (가짜 Firebase와 도우미는 t_rooms.py 앞부분을 그대로 쓴다)
import os, sys, json, datetime
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
TOK = 'fake-planner.asia-southeast1'
def closepin(pg):
    pg.wait_for_timeout(300)
    if ev(pg, "!!document.querySelector('#dlg-pin')"): pg.evaluate("()=>{const b=document.querySelector('#dlg-pin [data-act=\"modal-close\"],#dlg-pin [data-act=\"pin-skip\"]');if(b)b.click();}"); pg.wait_for_timeout(300)
def me(pg): return ev(pg, "(()=>{const b=document.querySelector('#meBtn, .me');return b?b.textContent:''})()")

def day(n): return (datetime.date.today() + datetime.timedelta(days=n)).isoformat()
T, T1, TP = day(0), day(1), day(-1)
RS, RD = 'srcroomabcdef12', 'dstroomabcdef34'
PER = [{'s': 510, 'e': 560}, {'s': 570, 'e': 620}, {'s': 630, 'e': 680}, {'s': 690, 'e': 740}, {'s': 810, 'e': 860}, {'s': 870, 'e': 920}, {'s': 930, 'e': 980}]
STORE['rooms'] = {
  RS: {'d': {
    'meta': {'config': {'certHour': 26, 'roster': [{'id': 'm1', 'name': '민준'}, {'id': 'm2', 'name': '서연'}]}, 'room': {'name': '1학기 방', 'code': '111222'}},
    'subjects': {'s1': {'name': '미적분Ⅰ', 'order': 1, 'items': [{'id': 'i1', 'label': '문제집 풀이'}, {'id': 'i2', 'label': '오답 정리'}]},
                 's2': {'name': '영어', 'order': 2, 'items': [{'id': 'i1', 'label': '지문 분석'}]},
                 's8': {'name': '생명과학 실험', 'order': 3, 'items': [{'id': 'i1', 'label': '보고서'}]},
                 's9': {'name': '후마니타스', 'order': 4, 'items': [{'id': 'i1', 'label': '독서'}]}},
    'events': {'e1': {'mid': 'm1', 'date': day(5), 'title': '미적 수행평가', 'sid': 's1', 'kind': 'perf'},
               'e2': {'mid': 'm2', 'date': day(5), 'title': '친구 일정', 'shared': True},
               'e3': {'mid': 'm1', 'date': day(7), 'title': '후마 발표', 'sid': 's9', 'shared': True},
               'e4': {'mid': 'm1', 'date': day(-3), 'title': '지난 수행평가'}},
    'plans': {'p1': {'mid': 'm1', 'sid': 's1', 'type': '문제집 풀이', 'unit': '쪽', 'note': '쎈', 'mode': 'split', 'total': 30, 'due': day(6), 'start': T, 'at': 1},
              'p2': {'mid': 'm1', 'sid': 's2', 'type': '지문 분석', 'mode': 'once', 'due': day(-2), 'at': 1}},
    'progress': {'m1': {'units': {'s1': [{'id': 'u1', 'n': '1단원'}, {'id': 'u2', 'n': '2단원'}]},
                        'checks': {'s1__i1': True, 's1__u1__i2': True, 's2__i1': True, 's9__i1': True, 's8__i1': True},
                        'scol': {'s1': '#E5484D'}, 'abbr': {'s1': '미적', 's2': '영'}, 'skip': {'s8': True}, 'goalMins': 300,
                        'title': 'b_star', 'reset': {'date': T, 'off': 3}, 'liked': {'n1': True},
                        'tt': {'b': [{'id': 'b1', 'k': 'academy', 't': '수학 학원', 'sid': 's1', 'sids': 's1,s2', 'd': '0101010', 's': 1080, 'e': 1260}],
                               'ov': {T1: {'b1': {'s': 1100, 'e': 1260}}, TP: {'b1': {'off': True}}},
                               'win': {'s': 540, 'e': 1380},
                               'sch': {'p': PER, 'w': {'1': {'p0': {'s': 's1', 'tc': '김', 'r': '101호'}, 'p1': {'t': '자습'}, 'p2': {'s': 's8'}}}}}}},
    'days': {'m1_' + TP: {'goals': [{'id': 'g0', 'text': '어제 할 일', 'sid': 's1', 'done': True}], 'mins': {'s1': 90}},
             'm1_' + T: {'goals': [{'id': 'g1', 'text': '오늘 할 일', 'sid': 's1', 'done': True}], 'mins': {'s1': 60}, 'certAt': T + 'T12:00:00.000Z'},
             'm1_' + T1: {'goals': [{'id': 'g2', 'text': '문제집 풀이 10쪽 (쎈)', 'sid': 's1', 'done': False, 'pid': 'p1', 'part': 1, 'amt': 10},
                                    {'id': 'g3', 'text': '후마 책 읽기', 'sid': 's9', 'done': False, 'ts': 1200, 'te': 1260},
                                    {'id': 'g4', 'text': '겹치는 일', 'sid': 's2', 'done': False}]},
             'm2_' + T1: {'goals': [{'id': 'gf', 'text': '친구 할 일', 'sid': 's2', 'done': False}]}}}},
  RD: {'d': {
    'meta': {'config': {'certHour': 26, 'roster': [{'id': 'm1', 'name': '지호'}, {'id': 'm2', 'name': '민준'}]}, 'room': {'name': '2학기 방', 'code': '333444'}},
    'subjects': {'sa': {'name': '미적분Ⅰ', 'order': 1, 'items': [{'id': 'x1', 'label': '오답 정리'}, {'id': 'x2', 'label': '문제집 풀이'}]},
                 'sb': {'name': '영어', 'order': 2, 'items': [{'id': 'y1', 'label': '지문 분석'}]}},
    'progress': {'m2': {'abbr': {'sa': '미분'}}},
    'days': {'m2_' + T1: {'goals': [{'id': 'gq', 'text': '겹치는 일', 'sid': 'sb', 'done': False}]}}}},
  'joincode-111222': {'r': RS, 'n': '1학기 방'}, 'joincode-333444': {'r': RD, 'n': '2학기 방'}}
D = lambda p: get_at('/rooms/' + RD + '/d/' + p)
LSV = {'gbb_rooms': json.dumps([{'url': DB, 'room': RD, 'name': '2학기 방', 'code': '333444'}, {'url': DB, 'room': RS, 'name': '1학기 방', 'code': '111222'}, {'url': DB, 'room': 'otherroomabcd99', 'name': '모르는 방'}]),
       'gbb_remote': json.dumps({'url': DB, 'room': RD}), 'gbb_legacy_room': '-', 'gbb_me@' + RD: 'm2', 'gbb_me@' + RS: 'm1',
       'gbb_pinask@' + RD: json.dumps({'m1': 1, 'm2': 1})}
cx, P = newpage(w=390, h=844, scale=2, ls=LSV)
P.goto(SITE + '#j=' + TOK, wait_until='commit'); P.wait_for_timeout(2500); closepin(P)
print('me            :', me(P))
click(P, '#meBtn', 700)
print('tile          :', ev(P, "(document.querySelector('.rmact.cr')||{}).innerText"))
P.screenshot(path=SH + 'carry_0_settings.png', full_page=False)
click(P, '.rmact.cr', 700)
print('pick list     :', ev(P, "[...document.querySelectorAll('#dlg-carry .rmrow')].map(r=>r.innerText.replace(/\\n/g,' / ')).join(' | ')"))
click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500)
print('preview       :', ev(P, "document.querySelector('#dlg-carry .db').innerText.replace(/\\n/g,' / ')"))
print('go button     :', ev(P, "(b=>b.textContent+' disabled='+b.disabled)(document.querySelector('[data-act=\"cr-go\"]'))"))
P.screenshot(path=SH + 'carry_1_preview.png')
click(P, '[data-act="cr-go"]', 1800)
print('flash         :', ev(P, "(document.querySelector('.flash span')||{}).textContent"))
# 되돌리기 확인
click(P, '[data-act="undo"]', 1500)
print('undo          : events', D('events'), '| plans', D('plans'), '| subjects', sorted((D('subjects') or {}).keys()))
# 다시 가져오기
click(P, '#meBtn', 700); click(P, '.rmact.cr', 600); click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500); click(P, '[data-act="cr-go"]', 1800)
ev_ = D('events') or {}; pl_ = D('plans') or {}; sb_ = D('subjects') or {}
hum = [k for k, v in sb_.items() if v.get('name') == '후마니타스']
print('subjects      :', [(k, v['name'], [i['label'] for i in v['items']]) for k, v in sb_.items()], '| 생명과학 실험 안 만듦', not any(v.get('name') == '생명과학 실험' for v in sb_.values()))
H = hum[0] if hum else None
print('events        :', sorted([(v['date'] == day(5) and 'd5' or v['date'] == day(7) and 'd7' or 'past', v['title'], v['mid'], v.get('sid') == ('sa' if v['title'] == '미적 수행평가' else H) if v.get('sid') else None, v.get('shared')) for v in ev_.values()]))
print('plans         :', [(v['mid'], v['sid'], v['type'], v['due'] == day(6)) for v in pl_.values()])
PID = list(pl_.keys())[0] if pl_ else None
dt = D('days/m2_' + T) or {}; d1 = D('days/m2_' + T1) or {}
print('today goals   :', [(g['text'], g['sid'], g['done']) for g in dt.get('goals', [])], '| mins', dt.get('mins'), '| cert', dt.get('certAt'))
print('tomorrow goals:', [(g['text'], g['sid'] == 'sa' and 'sa' or g['sid'] == 'sb' and 'sb' or g['sid'] == H and 'hum' or g['sid'], g.get('pid') == PID if g.get('pid') else None, g.get('ts')) for g in d1.get('goals', [])])
print('past day      :', D('days/m2_' + TP))
pr = D('progress/m2') or {}
print('units         :', pr.get('units'))
print('checks        :', sorted(k.replace(H or '#', 'HUM') for k in (pr.get('checks') or {})))
print('scol/abbr/skip:', pr.get('scol'), pr.get('abbr'), pr.get('skip'), '| goalMins', pr.get('goalMins'))
print('not copied    :', {k: pr.get(k) for k in ('title', 'reset', 'liked')})
tt = pr.get('tt') or {}
b = (tt.get('b') or [{}])[0]
print('tt block      :', {k: b.get(k) for k in ('k', 't', 'sid', 'sids', 'd', 's', 'e')}, '| ov', {d: {('NEW' if k == b.get('id') else k): v for k, v in o.items()} for d, o in (tt.get('ov') or {}).items()}, '| win', tt.get('win'))
w = (tt.get('sch') or {}).get('w')
print('school        :', w if not isinstance(w, list) else {i: x for i, x in enumerate(w) if x})
# 세 번째: 가져올 것이 없음
click(P, '#meBtn', 700); click(P, '.rmact.cr', 600); click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500)
print('again         :', ev(P, "(b=>b.textContent+' disabled='+b.disabled)(document.querySelector('[data-act=\"cr-go\"]'))"), '|', ev(P, "[...document.querySelectorAll('#dlg-carry .crchk small')].map(e=>e.textContent).join(' | ')"))
# 이름을 고른 적 없는 방
click(P, '[data-act="cr-back"]', 500)
print('unknown room  :', ev(P, "[...document.querySelectorAll('#dlg-carry .rmrow')].filter(r=>r.innerText.includes('모르는 방')).map(r=>r.innerText.replace(/\\n/g,' / ')+' btn='+!!r.querySelector('button')).join('')"))
print('src untouched :', len(get_at('/rooms/' + RS + '/d/events')), len(get_at('/rooms/' + RS + '/d/days')))
print('non-admin rec  :', ev(P, "!!document.querySelector('[data-act=\"cr-opt\"][data-k=\"rec\"]')"), '| today mins', (D('days/m2_' + T) or {}).get('mins'))
P.evaluate("()=>{const b=document.querySelector('#dlg-carry [data-act=\"modal-close\"]');if(b)b.click();}"); P.wait_for_timeout(400)

# ---- 방장이면: 점수와 공부 기록 (따로 켜야만)
STORE['rooms'][RD]['d']['meta']['config']['admin'] = 'm2'
P.reload(); P.wait_for_timeout(2500); closepin(P)
click(P, '#meBtn', 700); click(P, '.rmact.cr', 600); click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500)
print('admin rec row :', ev(P, "(b=>b?b.getAttribute('aria-pressed')+' / '+b.innerText.replace(/\\n/g,' / '):null)(document.querySelector('[data-act=\"cr-opt\"][data-k=\"rec\"]'))"))
print('go (rec off)  :', ev(P, "(b=>b.textContent+' disabled='+b.disabled)(document.querySelector('[data-act=\"cr-go\"]'))"))
click(P, '[data-act="cr-opt"][data-k="rec"]', 400)
P.screenshot(path=SH + 'carry_2_rec.png')
click(P, '[data-act="cr-go"]', 1800)
print('rec flash     :', ev(P, "(document.querySelector('.flash span')||{}).textContent"))
dp = D('days/m2_' + TP) or {}; dt = D('days/m2_' + T) or {}
print('past day      :', {k: dp.get(k) for k in ('mins', 'certAt')}, [(g['text'], g['done']) for g in dp.get('goals', [])])
print('today day     :', {k: dt.get(k) for k in ('mins', 'certAt')}, [(g['text'], g['done']) for g in dt.get('goals', [])])
pr = D('progress/m2') or {}
print('ledger/reset  :', pr.get('crl'), '| reset', pr.get('reset'), '| title', pr.get('title'))
# 이 방에서 공부한 기록이 따로 있을 때 다시 가져와도 두 번 더해지지 않음
STORE['rooms'][RD]['d']['days']['m2_' + T]['mins']['sa'] = STORE['rooms'][RD]['d']['days']['m2_' + T]['mins'].get('sa', 0) + 25
P.reload(); P.wait_for_timeout(2500); closepin(P)
click(P, '#meBtn', 700); click(P, '.rmact.cr', 600); click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500)
print('again rec     :', ev(P, "(b=>b?b.innerText.replace(/\\n/g,' / '):null)(document.querySelector('[data-act=\"cr-opt\"][data-k=\"rec\"]'))"))
STORE['rooms'][RS]['d']['days']['m1_' + T]['mins']['s1'] = 80  # 원래 방에서 20분 더 공부함
click(P, '[data-act="cr-back"]', 400); click(P, '#dlg-carry [data-act="cr-pick"][data-id="%s"]' % RS, 1500)
click(P, '[data-act="cr-opt"][data-k="rec"]', 400); click(P, '[data-act="cr-go"]', 1800)
print('updated today :', (D('days/m2_' + T) or {}).get('mins'), '(sa 60+25 -> 80+25=105)')
click(P, '[data-act="undo"]', 1500)
print('undo          :', (D('days/m2_' + T) or {}).get('mins'), '| past still', bool(D('days/m2_' + TP)))

# ---- 방에서 나가기: 다른 방이 있으면 그 방으로
P.evaluate("()=>{const a=JSON.parse(localStorage.getItem('gbb_rooms')).filter(x=>x.room!=='otherroomabcd99');localStorage.setItem('gbb_rooms',JSON.stringify(a));}")
click(P, '#meBtn', 700)
P.evaluate("()=>{const b=document.querySelector('[data-act=\"setup-reset\"]');b.scrollIntoView();b.click();}"); P.wait_for_timeout(400)
P.evaluate("()=>{const b=document.querySelector('[data-act=\"setup-reset\"]');b.click();}"); P.wait_for_timeout(3000); closepin(P)
print('left -> room  :', ev(P, "JSON.parse(localStorage.getItem('gbb_remote')||'null')"), '| flash', ev(P, "(document.querySelector('.flash span')||{}).textContent"), '| setup screen', ev(P, "!!document.querySelector('#view-setup, .setup')"))
click(P, '#meBtn', 700)
P.evaluate("()=>{const b=document.querySelector('[data-act=\"setup-reset\"]');b.scrollIntoView();b.click();}"); P.wait_for_timeout(400)
P.evaluate("()=>{const b=document.querySelector('[data-act=\"setup-reset\"]');b.click();}"); P.wait_for_timeout(3000)
print('left last     :', ev(P, "location.hash"), '| join screen', ev(P, "(document.querySelector('h1')||{}).textContent"), '| rules shown', ev(P, "document.body.innerText.includes('보안 규칙')"))
P.screenshot(path=SH + 'carry_3_left.png')
print('errors', errors)
br.close(); pw.stop()
