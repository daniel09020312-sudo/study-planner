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

# ---- 기기 D: 가 방(민준 m1)
cD, D = dev({RA: 'm1', RB: 'm3'}, RA)
w1 = prog(RA, 'm1').get('wal')
print('A wallet      :', bool(w1), '| dev', ev(D, "localStorage.getItem('gbb_wallet')") is not None, '| shop', wallet_text(D))
print('A synced rm   :', (W().get(w1) or {}).get('rm'))
# 가 방에서 '선' 사기
D.evaluate("()=>document.getElementById('shopBtn').click()"); D.wait_for_timeout(700)
click(D, '[data-act="shop-buy"][data-id="c:line"]', 300); click(D, '[data-act="shop-buy"][data-id="c:line"]', 1500)
print('A bought      :', (W().get(w1) or {}).get('own'))
D.evaluate("()=>{const b=document.querySelector('#dlg-shop [data-act=\"modal-close\"]');if(b)b.click();}"); D.wait_for_timeout(400)
# ---- 같은 기기에서 나 방(이름 '민 준', 띄어쓰기 달라도 같은 사람으로)
go(D, RB)
print('B linked      :', prog(RB, 'm3').get('wal') == w1, '| shop', wallet_text(D))
D.evaluate("()=>document.getElementById('shopBtn').click()"); D.wait_for_timeout(700)
print('B owns line   :', ev(D, "(document.querySelector('#shi-c-line .sha')||{}).innerText"))
# 나 방에서 지호에게 선물 20
click(D, '[data-act="gift-open"]', 400); click(D, '#giftPanel [data-act="gift-to"][data-id="m9"]', 300); click(D, '#giftPanel [data-act="gift-amt"][data-v="10"]', 300)
D.fill('#giftN', '20'); D.wait_for_timeout(300)
click(D, '[data-act="gift-send"]', 300); click(D, '[data-act="gift-send"]', 1500)
print('B gift        :', list((get_at('/rooms/%s/d/gifts' % RB) or {}).values()))
D.evaluate("()=>{const b=document.querySelector('#dlg-shop [data-act=\"modal-close\"]');if(b)b.click();}"); D.wait_for_timeout(23000)
print('B after gift  :', wallet_text(D), '| rm', (W().get(w1) or {}).get('rm', {}).get(RB + '_m3'))
# ---- 다른 기기 F에서 다 방(민준 m5)을 먼저 열면 지갑이 하나 더 생김
cF, F = dev({RC: 'm5'}, RC)
w2 = prog(RC, 'm5').get('wal')
print('C new wallet  :', bool(w2) and w2 != w1, '| shop', wallet_text(F))
# ---- 기기 D가 다 방을 열면 두 지갑이 합쳐짐
D.evaluate("(r)=>{const a=JSON.parse(localStorage.getItem('gbb_rooms'));a.push({url:%s,room:r,name:r});localStorage.setItem('gbb_rooms',JSON.stringify(a));localStorage.setItem('gbb_me@'+r,'m5');localStorage.setItem('gbb_pinask@'+r,JSON.stringify({m5:1}));}" % json.dumps(DB), RC)
go(D, RC)
print('merge         : old->new', (W().get(w1) or {}).get('to') == w2, '| dev now', json.loads(ev(D, "localStorage.getItem('gbb_wallet')"))['id'] == w2, '| own moved', (W().get(w2) or {}).get('own'))
print('C shop        :', wallet_text(D))
go(D, RA)
print('A follows     :', prog(RA, 'm1').get('wal') == w2, '| shop', wallet_text(D))
# ---- 관리자 코드
if ADM:
    D.evaluate("()=>document.getElementById('shopBtn').click()"); D.wait_for_timeout(700)
    click(D, '[data-act="adm-open"]', 400); D.fill('#admCode', 'wrong-code'); click(D, '[data-act="adm-go"]', 1200)
    print('adm wrong     :', ev(D, "(document.querySelector('.flash span')||{}).textContent"))
    D.fill('#admCode', ADM); click(D, '[data-act="adm-go"]', 1800)
    print('adm ok        :', ev(D, "(document.querySelector('.flash span')||{}).textContent"), '| unl saved', bool((W().get(w2) or {}).get('unl')), '| wallet', ev(D, "document.querySelector('.wl b').textContent"))
    click(D, '[data-act="shop-buy"][data-id="c:night"]', 300); click(D, '[data-act="shop-buy"][data-id="c:night"]', 1500)
    print('adm buy       :', (W().get(w2) or {}).get('own', {}).get('c:night'), '(0)')
    click(D, '[data-act="gift-open"]', 400); click(D, '#giftPanel [data-act="gift-to"][data-id="m2"]', 300); D.fill('#giftN', '5000'); D.wait_for_timeout(300)
    click(D, '[data-act="gift-send"]', 300); click(D, '[data-act="gift-send"]', 1500)
    print('adm gift      :', [g['n'] for g in (get_at('/rooms/%s/d/gifts' % RA) or {}).values()])
    D.screenshot(path=SH + 'wallet_adm.png')
    # 다른 기기에서 같은 지갑: 무제한으로 보임
    cG, G = dev({RA: 'm1'}, RA)
    print('other device  :', wallet_text(G))
    # 가짜 서명을 다른 지갑에 넣어도 무제한 아님
    with LOCK:
        STORE['rooms']['wallet-' + w1].pop('to', None)
        STORE['rooms']['wallet-' + w1]['unl'] = STORE['rooms']['wallet-' + w2]['unl']
    cH, H = dev({RB: 'm9'}, RB)
    wf = prog(RB, 'm9').get('wal')
    with LOCK: STORE['rooms']['wallet-' + wf]['unl'] = STORE['rooms']['wallet-' + w2]['unl']
    H.wait_for_timeout(4000)
    go(H, RB)
    print('forged copy   :', wallet_text(H))
    # 받은 사람(서연, 가 방)
    cS, Sp = dev({RA: 'm2'}, RA)
    print('receiver      :', wallet_text(Sp))
print('errors', errors)
br.close(); pw.stop()
