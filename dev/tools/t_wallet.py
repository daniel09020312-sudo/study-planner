# 모든 방 잉크: 지갑 만들기, 다른 방 잇기, 산 것 같이 쓰기, 선물, 지갑 합치기, 관리자 무제한(서명), 가짜 서명 막기
import os, sys, json, datetime
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
TOK = 'fake-planner.asia-southeast1'
ADM = os.environ.get('ADM_CODE', '')  # 관리자 코드는 저장소에 두지 않는다(시험할 때만 넣음)
T = datetime.date.today().isoformat()
def room(name, roster, days):
    return {'d': {'meta': {'config': {'certHour': 26, 'roster': roster}, 'room': {'name': name, 'code': '1'}},
                  'subjects': {'s1': {'name': '미적분Ⅰ', 'order': 1, 'items': []}}, 'days': days}}
RA, RB, RC = 'walletroomaaaa01', 'walletroombbbb02', 'walletroomcccc03'
STORE['rooms'] = {
  RA: room('가 방', [{'id': 'm1', 'name': '민준'}, {'id': 'm2', 'name': '서연'}], {'m1_' + T: {'goals': [], 'mins': {'s1': 1500}}}),   # 150방울
  RB: room('나 방', [{'id': 'm9', 'name': '지호'}, {'id': 'm3', 'name': '민 준'}], {'m3_' + T: {'goals': [], 'mins': {'s1': 900}}}),  # 90방울
  RC: room('다 방', [{'id': 'm5', 'name': '민준'}], {'m5_' + T: {'goals': [], 'mins': {'s1': 300}}})}  # 30방울
def W(): return {k[7:]: v for k, v in STORE['rooms'].items() if k.startswith('wallet-')}
def rooms_ls(*rs): return json.dumps([{'url': DB, 'room': r, 'name': r} for r in rs])
def dev(me_map, cur, extra=None):
    ls = {'gbb_remote': json.dumps({'url': DB, 'room': cur}), 'gbb_legacy_room': '-', 'gbb_rooms': rooms_ls(*me_map.keys())}
    for r, m in me_map.items(): ls['gbb_me@' + r] = m; ls['gbb_pinask@' + r] = json.dumps({m: 1})
    ls.update(extra or {})
    cx, pg = newpage(w=390, h=844, ls=ls)
    pg.goto(SITE + '#j=' + TOK, wait_until='commit'); pg.wait_for_timeout(5500)
    pg.evaluate("()=>document.querySelectorAll('#notes .note .x').forEach(b=>b.click())")
    return cx, pg
def go(pg, r):
    pg.evaluate("(r)=>{localStorage.setItem('gbb_remote',JSON.stringify({url:%s,room:r}));location.reload();}" % json.dumps(DB), r); pg.wait_for_timeout(6000)
    pg.evaluate("()=>document.querySelectorAll('#notes .note .x').forEach(b=>b.click())")
def wallet_text(pg):
    pg.evaluate("()=>{const b=document.getElementById('shopBtn');b.click();}"); pg.wait_for_timeout(800)
    t = ev(pg, "(document.querySelector('.wallet')||{innerText:''}).innerText.replace(/\\n/g,' / ')")
    pg.evaluate("()=>{const b=document.querySelector('#dlg-shop [data-act=\"modal-close\"]');if(b)b.click();}"); pg.wait_for_timeout(400)
    return t
def prog(r, m): return (get_at('/rooms/%s/d/progress/%s' % (r, m)) or {})

def shop(pg): pg.evaluate("()=>document.getElementById('shopBtn').click()"); pg.wait_for_timeout(800)
def close(pg): pg.evaluate("()=>{const b=document.querySelector('#dlg-shop [data-act=\"modal-close\"]');if(b)b.click();}"); pg.wait_for_timeout(400)
def flash(pg): return ev(pg, "(document.querySelector('.flash span')||{}).textContent")
def make_code(pg):
    shop(pg); click(pg, '[data-act="wal-open"]', 400); click(pg, '[data-act="wal-code"]', 1500)
    c = ev(pg, "(document.getElementById('walCodeT')||{}).textContent"); close(pg); return c
def link(pg, code):
    shop(pg); click(pg, '[data-act="wal-open"]', 400); pg.fill('#walLinkIn', code); click(pg, '[data-act="wal-link"]', 3500)
    f = flash(pg); close(pg); return f
# ---- 기기 D: 가 방(민준 m1)
cD, D = dev({RA: 'm1', RB: 'm3'}, RA)
w1 = prog(RA, 'm1').get('wal')
print('A wallet      :', bool(w1), '| shop', wallet_text(D))
shop(D); click(D, '[data-act="shop-buy"][data-id="c:line"]', 300); click(D, '[data-act="shop-buy"][data-id="c:line"]', 1500); close(D)
print('A bought      :', (W().get(w1) or {}).get('own'))
# ---- 같은 기기, 같은 이름이어도 나 방은 따로
go(D, RB)
wB = prog(RB, 'm3').get('wal')
print('B separate    :', bool(wB) and wB != w1, '| shop', wallet_text(D))
# ---- 가 방에서 연동 코드 만들기 -> 나 방에서 넣기
go(D, RA)
code = make_code(D)
print('code          :', bool(code) and len(code) == 9, '| mapping', [k for k in STORE['rooms'] if k.startswith('walletcode-')], '| code not stored in wallet', code.replace('-', '') not in json.dumps(W().get(w1)))
go(D, RB)
print('wrong code    :', link(D, 'ZZZZ-ZZZZ'))
print('link          :', link(D, code))
print('B linked      : pointer', prog(RB, 'm3').get('wal') == w1, '| old->new', (W().get(wB) or {}).get('to') == w1, '| shop', wallet_text(D))
shop(D); print('B owns line   :', ev(D, "(document.querySelector('#shi-c-line .sha')||{}).innerText"), '| rooms', ev(D, "(document.querySelector('.wlrooms')||{innerText:''}).innerText")); close(D)
# 나 방에서 지호에게 선물 20
shop(D); click(D, '[data-act="gift-open"]', 400); click(D, '#giftPanel [data-act="gift-to"][data-id="m9"]', 300)
D.fill('#giftN', '20'); D.wait_for_timeout(300); click(D, '[data-act="gift-send"]', 300); click(D, '[data-act="gift-send"]', 1500); close(D)
D.wait_for_timeout(23000)
print('B after gift  :', wallet_text(D))
# ---- 다른 기기에서 이름이 같은 '민준'(다 방): 저절로 붙지 않음
cF, F = dev({RC: 'm5'}, RC)
w3 = prog(RC, 'm5').get('wal')
print('C separate    :', w3 not in (w1, wB), '| shop', wallet_text(F))
# 코드를 다시 만들면 예전 코드는 못 씀
go(D, RA); code2 = make_code(D)
print('regen         :', code2 != code, '| mappings', len([k for k in STORE['rooms'] if k.startswith('walletcode-')]))
print('old code      :', link(F, code))
print('new code      :', link(F, code2), '| C pointer', prog(RC, 'm5').get('wal') == w1, '| shop', wallet_text(F))
# ---- 나 방만 떼어 내기
go(D, RB)
shop(D); click(D, '[data-act="wal-open"]', 400); click(D, '[data-act="wal-unlink"]', 300); click(D, '[data-act="wal-unlink"]', 3500); close(D)
wB2 = prog(RB, 'm3').get('wal')
print('unlink        :', wB2 not in (w1, wB), '| B key gone from shared', (RB + '_m3') not in (W().get(w1) or {}).get('rm', {}), '| shop', wallet_text(D))
go(D, RA)
# ---- 관리자 코드
if ADM:
    shop(D); click(D, '[data-act="adm-open"]', 400); D.fill('#admCode', 'wrong-code'); click(D, '[data-act="adm-go"]', 1200)
    print('adm wrong     :', flash(D))
    D.fill('#admCode', ADM); click(D, '[data-act="adm-go"]', 1800)
    print('adm ok        :', flash(D), '| unl saved', bool((W().get(w1) or {}).get('unl')), '| wallet', ev(D, "document.querySelector('.wl b').textContent"))
    click(D, '[data-act="shop-buy"][data-id="c:night"]', 300); click(D, '[data-act="shop-buy"][data-id="c:night"]', 1500)
    print('adm buy       :', (W().get(w1) or {}).get('own', {}).get('c:night'), '(0)')
    click(D, '[data-act="gift-open"]', 400); click(D, '#giftPanel [data-act="gift-to"][data-id="m2"]', 300); D.fill('#giftN', '5000'); D.wait_for_timeout(300)
    click(D, '[data-act="gift-send"]', 300); click(D, '[data-act="gift-send"]', 1500); close(D)
    print('adm gift      :', [g['n'] for g in (get_at('/rooms/%s/d/gifts' % RA) or {}).values()])
    print('linked room C :', wallet_text(F) if F else '')
    go(F, RC); print('C after reload:', wallet_text(F))
    # 무제한 표시를 다른 지갑에 베껴도 안 됨
    with LOCK: STORE['rooms']['wallet-' + wB2]['unl'] = STORE['rooms']['wallet-' + w1]['unl']
    go(D, RB); print('forged copy   :', wallet_text(D))
    cS, Sp = dev({RA: 'm2'}, RA)
    print('receiver      :', wallet_text(Sp))
print('errors', errors)
br.close(); pw.stop()
