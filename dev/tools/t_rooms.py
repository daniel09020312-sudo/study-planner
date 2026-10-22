import os
# 참여 코드로 방 들어가기, 새 방 만들기, 방 바꾸기를 가짜 Firebase로 확인한다.
import json, re, sys, base64, threading
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright
sys.path.insert(0, '/home/claude/planner/tools')
from rig import FONT_PKG, font_css, NPM

BASE = '/home/claude/planner'
SH = BASE + '/shots/'
SITE = 'https://planner.test/'
DB = 'https://fake-planner-default-rtdb.asia-southeast1.firebasedatabase.app'
import os
LIGHT = os.environ.get('LIGHT') == '1'
WEB = BASE + ('/web-light' if LIGHT else '/web')
PAGE = open(WEB + '/index.html', encoding='utf-8').read()
STORE = {}
LOCK = threading.Lock()
DENY_WRITES = {'on': False}
LOG = []


def norm(v):
    if isinstance(v, dict):
        o = {k: norm(x) for k, x in v.items()}
        o = {k: x for k, x in o.items() if x is not None}
        if not o:
            return None
        # Firebase처럼: 열쇠가 모두 0 이상의 정수이고 절반 넘게 차 있으면 배열로 돌려준다
        if all(re.fullmatch(r'0|[1-9][0-9]*', k) for k in o):
            mx = max(int(k) for k in o)
            if len(o) > (mx + 1) / 2:
                return [o.get(str(i)) for i in range(mx + 1)]
        return o
    if isinstance(v, list):
        o = {str(i): norm(x) for i, x in enumerate(v)}
        o = {k: x for k, x in o.items() if x is not None}
        if not o:
            return None
        ks = [int(k) for k in o]
        mx = max(ks)
        if len(o) > (mx + 1) / 2:
            return [o.get(str(i)) for i in range(mx + 1)]
        return o
    return v


def get_at(path):
    cur = STORE
    for seg in [p for p in path.split('/') if p]:
        if isinstance(cur, dict) and seg in cur:
            cur = cur[seg]
        elif isinstance(cur, list) and seg.isdigit() and int(seg) < len(cur):
            cur = cur[int(seg)]
        else:
            return None
    return cur


def set_at(path, val):
    segs = [p for p in path.split('/') if p]
    cur = STORE
    for seg in segs[:-1]:
        if not isinstance(cur.get(seg), dict):
            cur[seg] = {}
        cur = cur[seg]
    val = norm(val)
    if val is None:
        cur.pop(segs[-1], None)
    else:
        cur[segs[-1]] = val
    # 빈 부모 정리
    def prune(d):
        for k in list(d.keys()):
            if isinstance(d[k], dict):
                prune(d[k])
                if not d[k]:
                    d.pop(k)
    prune(STORE)


CORS = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET,PUT,DELETE,PATCH,OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type'}


def route(route_, request):
    u = request.url
    if u.startswith(SITE):
        rel=urlparse(u).path.lstrip('/') or 'index.html'
        fp=os.path.join(BASE+'/site',rel)
        if not os.path.isfile(fp): return route_.fulfill(status=404, body='')
        ct={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.webp':'image/webp','.png':'image/png','.webmanifest':'application/manifest+json'}.get(os.path.splitext(fp)[1],'application/octet-stream')
        return route_.fulfill(status=200, content_type=ct, body=open(fp,'rb').read())
    if u.startswith(DB):
        pu = urlparse(u)
        path = unquote(pu.path)
        if not path.endswith('.json'):
            return route_.fulfill(status=404, headers=CORS, body='')
        path = path[:-5]
        m = request.method
        LOG.append((m, path))
        if m == 'OPTIONS':
            return route_.fulfill(status=204, headers=CORS, body='')
        room_ok = re.match(r'^/rooms/[A-Za-z0-9_-]{12,40}(/|$)', path)
        if not room_ok:
            return route_.fulfill(status=401, headers=CORS, content_type='application/json', body='{"error":"Permission denied"}')
        resp = None
        with LOCK:
            if m == 'GET':
                data = get_at(path)
                if 'text/event-stream' in (request.headers.get('accept') or ''):
                    body = 'retry: 300\nevent: put\ndata: ' + json.dumps({'path': '/', 'data': data}, ensure_ascii=False) + '\n\n'
                    h = dict(CORS); h['Cache-Control'] = 'no-cache'
                    resp = (200, h, 'text/event-stream; charset=utf-8', body)
                else:
                    resp = (200, CORS, 'application/json', json.dumps(data, ensure_ascii=False))
            elif DENY_WRITES['on']:
                resp = (401, CORS, 'application/json', '{"error":"Permission denied"}')
            elif m == 'PUT':
                val = json.loads(request.post_data or 'null')
                set_at(path, val)
                resp = (200, CORS, 'application/json', json.dumps(val, ensure_ascii=False))
            elif m == 'DELETE':
                set_at(path, None)
                resp = (200, CORS, 'application/json', 'null')
        if resp:
            return route_.fulfill(status=resp[0], headers=resp[1], content_type=resp[2], body=resp[3])
        return route_.fulfill(status=405, headers=CORS, body='')
    if u.startswith('https://fonts.googleapis.com/'):
        mm = re.search(r'family=([^:&]+)', u)
        fam = mm.group(1).replace('+', ' ') if mm else ''
        if fam in FONT_PKG:
            return route_.fulfill(status=200, content_type='text/css', body=font_css(fam))
        return route_.fulfill(status=200, content_type='text/css', body='')
    if u.startswith('https://fonts.gstatic.com/fs/'):
        p = NPM + '/@fontsource/' + u.split('/fs/')[1]
        if os.path.exists(p):
            return route_.fulfill(status=200, content_type='font/woff2', body=open(p, 'rb').read())
    return route_.abort()


pw = sync_playwright().start()
br = pw.chromium.launch(args=['--font-render-hinting=none'])
errors = []


def newpage(w=1180, h=820, scale=1, ls=None):
    ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=scale, service_workers='block')
    ctx.route(re.compile(r'^https?://'), route)
    pg = ctx.new_page()
    pg.on('requestfailed', lambda r: print('REQFAIL', r.url[:90]))
    pg.on('response', lambda r: print('HTTP', r.status, r.url[:90]) if r.status>=400 and 'firebasedatabase' not in r.url else None)
    pg.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    pg.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' and 'net::ERR' not in m.text and 'EventSource' not in m.text else None)
    init = {'gbb_note': '9999999999999', 'gbb_pinask': json.dumps({'m1': 1, 'm2': 1, 'm3': 1, 'm4': 1, 'm5': 1})}
    init.update(ls or {})
    pg.add_init_script("try{var o=%s;if(!sessionStorage.getItem('__i')){for(var k in o)localStorage.setItem(k,o[k]);sessionStorage.setItem('__i','1');}}catch(e){}" % json.dumps(init))
    return ctx, pg


def click(pg, sel, wait=300):
    pg.evaluate("()=>{const d=document.querySelector('#dlg-reward [data-act=\"modal-close\"]');if(d)d.click();}");pg.wait_for_timeout(250)
    pg.locator(sel).first.click()
    pg.wait_for_timeout(wait)


def ev(pg, js):
    return pg.evaluate('()=>' + js)



import datetime
R1 = 'oldroomabcdefgh2'
STORE['rooms'] = {R1: {'d': {'meta': {'config': {'certHour': 26, 'roster': [{'id': 'm1', 'name': '민준'}, {'id': 'm2', 'name': '서연'}, {'id': 'm3', 'name': '도윤'}]}},
                             'subjects': {'s1': {'name': '미적분Ⅰ', 'order': 1, 'items': [{'id': 'i1', 'label': '문제집 풀이'}]}, 's2': {'name': '영어', 'order': 2, 'items': [{'id': 'i1', 'label': '지문 분석'}]}},
                             'days': {'m1_2026-10-20': {'date': '2026-10-20', 'goals': [{'id': 'g1', 'text': '예전 방 할 일', 'sid': 's1', 'done': False}]}}}}}
TOK = 'fake-planner.asia-southeast1'
def codes(): return {k[9:]: v for k, v in STORE.get('rooms', {}).items() if k.startswith('joincode-')}
def closepin(pg):
    pg.wait_for_timeout(300)
    if ev(pg, "!!document.querySelector('#dlg-pin')"): pg.evaluate("()=>{const b=document.querySelector('#dlg-pin [data-act=\"modal-close\"],#dlg-pin [data-act=\"pin-skip\"]');if(b)b.click();}"); pg.wait_for_timeout(300)
def me(pg): return ev(pg, "(()=>{const b=document.querySelector('#meBtn, .me');return b?b.textContent:''})()")

# ---- A: 예전 기기 (예전 판에서 쓰던 값이 그대로 남아 있음)
ca, A = newpage(ls={'gbb_remote': json.dumps({'url': DB, 'room': R1}), 'gbb_me': 'm1'})
A.goto(SITE + '#db=' + DB + '&room=' + R1, wait_until='commit'); A.wait_for_timeout(2200)
print('A legacy me    :', ev(A, "!document.querySelector('#view-gate')"), '| hash', ev(A, "location.hash"))
c = codes(); print('A auto code    :', list(c.values())[0] if c else None, '| meta/room', STORE['rooms'][R1]['d']['meta'].get('room'))
CODE1 = list(c.keys())[0]
print('A storage      :', ev(A, "JSON.stringify(Object.keys(localStorage).filter(k=>/gbb_(me|rooms|legacy)/.test(k)).sort())"))
click(A, '#meBtn', 600)
print('A settings     :', ev(A, "(document.querySelector('.rmsec')||{}).innerText"))
A.screenshot(path=SH + 'r_01_settings.png')
click(A, '[data-act="open"][data-modal="invite"]', 600)
print('A invite msg   :', ev(A, "(document.getElementById('invMsg')||{}).textContent"))
A.screenshot(path=SH + 'r_02_invite.png')
click(A, '[data-act="room-invite"]', 400)
click(A, '#dlg-invite [data-act="modal-close"]', 400)

# ---- B: 새 친구, 카톡 링크로 처음 들어옴
cb, B = newpage(w=390, h=844)
B.goto(SITE + '#join=' + TOK, wait_until='commit'); B.wait_for_timeout(1500)
print('B join screen  :', ev(B, "(document.querySelector('#view-join h1')||{}).textContent"), '| inputmode', ev(B, "document.getElementById('joinCode').inputMode"))
B.screenshot(path=SH + 'r_03_join.png')
B.locator('#joinCode').fill('123 456'); B.wait_for_timeout(900)
wrong = '123456' if '123456' not in c else '654321'
print('B wrong code   :', ev(B, "(document.querySelector('.serr')||{}).textContent"), '| input', ev(B, "document.getElementById('joinCode').value"))
B.locator('#joinCode').type(CODE1, delay=40); B.wait_for_timeout(2200)
print('B after code   :', ev(B, "(document.querySelector('#view-gate .gaterm')||{}).textContent"), '|', ev(B, "(document.querySelector('#view-gate h1')||{}).textContent"), '| names', ev(B, "[...document.querySelectorAll('#view-gate .person')].map(e=>e.textContent).join(',')"), '| hash', ev(B, "location.hash"))
B.screenshot(path=SH + 'r_04_gate.png')
click(B, '#view-gate .person >> nth=1', 600); closepin(B)
print('B in as        :', ev(B, "!document.querySelector('#view-gate')"), '| me key', ev(B, "localStorage.getItem('gbb_me@%s')" % R1))
print('B overflow     :', ev(B, "document.documentElement.scrollWidth>innerWidth+1"))

# ---- A: 새 방 만들기
click(A, '#meBtn', 600)
print('A room buttons :', ev(A, "[...document.querySelectorAll('.rmsec button')].map(e=>e.innerText.replace(/\\n/g,' / ')).join(' | ')"))
A.screenshot(path=SH + 'r_05a_settings.png')
click(A, '[data-act="open"][data-modal="rooms"]', 600)
print('A move modal   :', ev(A, "(document.getElementById('dlgT')||{}).textContent"), '|', ev(A, "[...document.querySelectorAll('.rmrow')].map(e=>e.innerText.replace(/\\n/g,' / ')).join(' | ')"), '| has new form', ev(A, "!!document.getElementById('nrName')"))
A.screenshot(path=SH + 'r_05b_move.png')
click(A, '.rmswap [data-modal="newroom"]', 600)
print('A new modal    :', ev(A, "(document.getElementById('dlgT')||{}).textContent"), '| people prefill', ev(A, "document.getElementById('nrPeople').value"))
A.fill('#nrName', '새 공부방'); A.fill('#nrPeople', '민준\n지호\n하준')
A.screenshot(path=SH + 'r_05_rooms.png')
click(A, '[data-act="nr-make"]', 3000)
c2 = codes(); new = [k for k in c2 if k != CODE1]; CODE2 = new[0] if new else None; R2 = c2[CODE2]['r'] if CODE2 else None
print('A new room     :', CODE2, c2.get(CODE2), '| config', STORE['rooms'].get(R2, {}).get('d', {}).get('meta'), '| subjects', list(STORE['rooms'].get(R2, {}).get('d', {}).get('subjects', {}).keys()))
print('A now in       :', ev(A, "!document.querySelector('#view-gate')"), '| invite popup', ev(A, "!!document.querySelector('#dlg-invite')"), '| code shown', ev(A, "(document.querySelector('.invbig b')||{}).textContent"), '| hash', ev(A, "location.hash"))
print('A new room days:', ev(A, "document.querySelectorAll('.goal').length"), '(예전 방 할 일이 안 보여야 함)')
A.screenshot(path=SH + 'r_06_newroom.png')
click(A, '#dlg-invite [data-act="modal-close"]', 300)

# ---- C: 새 방에 코드로 들어옴
cc, C = newpage()
C.goto(SITE + '#join=' + TOK, wait_until='commit'); C.wait_for_timeout(1300)
C.locator('#joinCode').type(CODE2, delay=30); C.wait_for_timeout(2200)
print('C gate         :', ev(C, "(document.querySelector('#view-gate .gaterm')||{}).textContent"), '| names', ev(C, "[...document.querySelectorAll('#view-gate .person')].map(e=>e.textContent).join(',')"))
click(C, '#view-gate .person >> nth=1', 600); closepin(C)
print('C in           :', ev(C, "!document.querySelector('#view-gate')"))

# ---- A: 예전 방으로 돌아가기
click(A, '#meBtn', 600); click(A, '[data-act="open"][data-modal="rooms"]', 600)
click(A, '[data-act="room-open"]', 2500)
print('A back old     :', ev(A, "!document.querySelector('#view-gate')"), '| room name', ev(A, "JSON.parse(localStorage.getItem('gbb_remote')).room===%s" % json.dumps(R1)))
# 방장: 코드 바꾸기, 이름 바꾸기
click(A, '#meBtn', 600); click(A, '[data-act="open"][data-modal="roomadm"]', 600)
A.fill('#rmRename', '처음 공부방'); click(A, '[data-act="room-rename"]', 600)
click(A, '[data-act="room-recode"]', 300); click(A, '[data-act="room-recode"]', 1500)
c3 = codes()
print('A recode       : old gone', CODE1 not in c3, '| codes', {k: v['n'] for k, v in c3.items()})
# 예전 코드로는 못 들어옴
cd, D = newpage()
D.goto(SITE + '#join=' + TOK, wait_until='commit'); D.wait_for_timeout(1200)
D.locator('#joinCode').type(CODE1, delay=30); D.wait_for_timeout(1500)
print('D old code     :', ev(D, "(document.querySelector('.serr')||{}).textContent"))
# 참여 링크를 연결 화면에 붙여넣기
ce, E = newpage()
E.goto(SITE, wait_until='commit'); E.wait_for_timeout(1200)
E.fill('#setupIn', 'https://planner.test/#join=' + TOK); click(E, '[data-act="setup-go"]', 600)
print('E paste link   :', ev(E, "(document.querySelector('#view-join h1')||{}).textContent"))
print('errors', errors)
br.close(); pw.stop()
