# v41: 바뀐 칸만 저장. 예전 기록(이 기기 저장)으로 연 직후, 오프라인일 때 써도 다른 기기에서 넣은 단원이 지워지지 않는다
import os, sys, json, datetime, time, re
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
TOK = 'fake-planner.asia-southeast1'
def closepin(pg):
    pg.wait_for_timeout(300)
    if ev(pg, "!!document.querySelector('#dlg-pin')"): pg.evaluate("()=>{const b=document.querySelector('#dlg-pin [data-act=\"modal-close\"],#dlg-pin [data-act=\"pin-skip\"]');if(b)b.click();}"); pg.wait_for_timeout(300)
T = datetime.date.today().isoformat()
R = 'patchroomabcdef1'
def b36(n):
    s = ''
    while n: s = '0123456789abcdefghijklmnopqrstuvwxyz'[n % 36] + s; n //= 36
    return s
def tok(): return b36(int(time.time() * 1000)) + '.t%03d' % (int(time.time() * 1000) % 1000)
STORE['rooms'] = {R: {'d': {
    'meta': {'config': {'certHour': 29, 'migCert5': 1, 'migHum': 1, 'roster': [{'id': 'm1', 'name': '민준'}, {'id': 'm2', 'name': '서연'}]}, 'room': {'name': '단원 방', 'code': '777888'}},
    'subjects': {'s1': {'name': '미적분Ⅰ', 'order': 1, 'items': [{'id': 'i1', 'label': '개념'}, {'id': 'i2', 'label': '문제집'}]},
                 's2': {'name': '물리학Ⅱ', 'order': 2, 'items': [{'id': 'i1', 'label': '개념'}]}},
    'progress': {'m1': {'units': {'s1': [{'id': 'u1', 'n': '1. 함수의 극한'}]}, 'checks': {'s1__u1__i1': True}}},
    'days': {'m1_' + T: {'goals': [{'id': 'g1', 'text': '처음 할 일', 'sid': 's1', 'done': False}]}}}},
  'joincode-777888': {'r': R, 'n': '단원 방'}}
def P(): return get_at('/rooms/' + R + '/d/progress/m1') or {}
def units(): return [u['n'] for u in (P().get('units') or {}).get('s1') or []]
def server_set(path, val):
    with LOCK:
        set_at('/rooms/' + R + '/d/' + path, val)
        set_at('/rooms/' + R + '/x/' + path.replace('/', '|'), tok())
BASE_LS = {'gbb_remote': json.dumps({'url': DB, 'room': R}), 'gbb_legacy_room': '-', 'gbb_rooms': json.dumps([{'url': DB, 'room': R, 'name': '단원 방', 'code': '777888'}]),
           'gbb_me@' + R: 'm1', 'gbb_test': '1', 'gbb_pinask@' + R: json.dumps({'m1': 1, 'm2': 1})}
cb, B = newpage(w=390, h=844, ls=BASE_LS)
B.goto(SITE + '#j=' + TOK, wait_until='commit'); B.wait_for_timeout(3000); closepin(B)
B.wait_for_timeout(4000)
w0 = P().get('wal'); nw0 = len([k for k in STORE['rooms'] if k.startswith('wallet-')])
print('first open    : units', units(), '| wallet', bool(w0), nw0)

# ---- 1) 다른 기기에서 단원 추가 -> 이 기기는 예전 저장으로 열고, 새 기록을 받기 전에(받기를 붙잡아 둠) 바로 체크
B.evaluate("()=>{const k='gbb_cache@%s',c=JSON.parse(localStorage.getItem(k));const p=c.t.progress.m1;delete p.wal;if(p.shop)delete p.shop.gf;c.full=Date.now();localStorage.setItem(k,JSON.stringify(c));}" % R)
p1 = P(); p1['units']['s1'].append({'id': 'u2', 'n': '2. 미분계수'}); p1['abbr'] = {'s1': '미적'}
server_set('progress/m1', p1)
held = []
B.route(re.compile(r'.*/d/progress/m1\.json.*'), lambda r, q: held.append(r) if q.method == 'GET' else r.fallback())
B.route(re.compile(r'.*/d\.json.*'), lambda r, q: held.append(r) if q.method == 'GET' else r.fallback())
B.reload(); B.wait_for_timeout(2500); closepin(B)
print('stale view    : fresh', ev(B, "__gbb.S.net.fresh()"), '| held GETs', len(held), '| shows u2', ev(B, "JSON.stringify(__gbb.view().progress.m1||{}).includes('미분계수')"))
B.evaluate("()=>{__gbb.editProg(function(p){p.checks['s2__i1']=true;});}"); B.wait_for_timeout(1500)
B.wait_for_timeout(4000)  # 지갑, shopGf는 기다려야 함
p2 = P()
print('after edit    : units', units(), '| abbr kept', (p2.get('abbr') or {}).get('s1'), '| new check', (p2.get('checks') or {}).get('s2__i1'), '| old check', (p2.get('checks') or {}).get('s1__u1__i1'))
print('no auto write : wal', p2.get('wal') == w0, '| wallets', len([k for k in STORE['rooms'] if k.startswith('wallet-')]) == nw0, '| gf', (p2.get('shop') or {}).get('gf'))
for r in held:
    try: r.fallback()
    except Exception as e: print('fallback err', e)
B.unroute(re.compile(r'.*/d/progress/m1\.json.*')); B.unroute(re.compile(r'.*/d\.json.*'))
B.wait_for_timeout(5000)
print('fresh later   : fresh', ev(B, "__gbb.S.net.fresh()"), '| view units', ev(B, "__gbb.unitsOf(__gbb.view(),'m1','s1').map(u=>u.n).join(',')"), '| wal kept', P().get('wal') == w0)

# ---- 2) 오프라인에서 체크 -> 그동안 다른 기기에서 단원 추가 -> 연결되면 바뀐 칸만
cb.set_offline(True); B.wait_for_timeout(300); B.evaluate("()=>window.dispatchEvent(new Event('offline'))")
B.evaluate("()=>{__gbb.editProg(function(p){p.checks['s1__u2__i2']=true;});__gbb.editDay(__gbb.today(),function(d){d.goals[0].done=true;});}"); B.wait_for_timeout(600)
ob = json.loads(ev(B, "localStorage.getItem('gbb_outbox@%s')||'[]'" % R))
print('outbox        :', [(x['p'], sorted((x.get('ops') or {}).keys())) for x in ob])
p3 = P(); p3['units']['s1'].append({'id': 'u3', 'n': '3. 도함수'}); server_set('progress/m1', p3)
dd = get_at('/rooms/' + R + '/d/days/m1_' + T) or {}; dd['mins'] = {'s1': 50}; server_set('days/m1_' + T, dd)
cb.set_offline(False); B.evaluate("()=>window.dispatchEvent(new Event('online'))"); B.wait_for_timeout(4000)
p4 = P(); d4 = get_at('/rooms/' + R + '/d/days/m1_' + T) or {}
print('after online  : units', units(), '| check', (p4.get('checks') or {}).get('s1__u2__i2'), '| day mins kept', d4.get('mins'), '| goal done', d4['goals'][0].get('done'), '| outbox', ev(B, "(JSON.parse(localStorage.getItem('gbb_outbox@%s')||'[]')).length" % R))
B.wait_for_timeout(2000)
print('view          :', ev(B, "__gbb.unitsOf(__gbb.view(),'m1','s1').map(u=>u.n).join(',')"), '| mins', ev(B, "JSON.stringify(__gbb.dayOf(__gbb.view(),'m1',__gbb.today()).mins)"))

# ---- 3) 단원 추가·삭제·순서 바꾸기(화면으로)가 그대로 되는지
click(B, '[data-act="tab"][data-tab="prog"]', 900)
print('jdiff         :', ev(B, "JSON.stringify(__gbb.jdiff({a:{x:1,y:[1,2]},b:{c:1},e:{}},{a:{x:2,y:[1,2]},d:{z:{}},e:null,f:[3]}))"))
print('opsMerge      :', ev(B, "JSON.stringify(__gbb.opsMerge({'units/s1':[1],'checks':{a:true}},{'units':{s2:[2]},'checks/b':true}))"))
print('errors', [e for e in errors if 'REQFAIL' not in e])
br.close(); pw.stop()
