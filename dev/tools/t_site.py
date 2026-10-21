import os
# 가짜 Firebase(REST, 스트리밍 흉내)에 두 브라우저를 붙여 웹 버전을 확인한다.
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
        return o or None
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


def calm(pg):
    # 이름을 고른 뒤 뜨는 창(비밀번호 정하기, 출석)을 모두 닫는다
    for _ in range(4):
        pg.wait_for_timeout(450)
        n = pg.evaluate("()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b){b.click();return 1;}return 0;}")
        if not n:
            pg.wait_for_timeout(500)
            if not pg.evaluate("()=>!!document.querySelector('.dialog')"):
                break


# ---- 주인(A): 주소 붙여넣고 연결
ca, A = newpage()
A.goto(SITE, wait_until='commit'); A.wait_for_timeout(1500)
print('A setup screen :', ev(A, "document.querySelector('#view-setup h1')&&document.querySelector('#view-setup h1').textContent"), '| nav hidden:', ev(A, "getComputedStyle(document.querySelector('.rail')).display"))
A.screenshot(path=SH + 'w_00_setup.png')
A.fill('#setupIn', 'firebase 주소 아님'); click(A, '[data-act="setup-go"]')
print('A bad input    :', ev(A, "(document.querySelector('.serr')||{}).textContent"))
A.fill('#setupIn', DB + '/'); click(A, '[data-act="setup-go"]', 1500)
print('A url after    :', ev(A, "location.hash.replace(/room=[a-z0-9]+/,'room=…')"), '| gate:', ev(A, "(document.querySelector('#view-gate h1')||{}).textContent"))
room = ev(A, "JSON.parse(localStorage.getItem('gbb_remote')).room")
print('room           :', len(room), 'chars')
# 연결 화면에서 기록 가져오기
A.screenshot(path=SH + 'w_01_gate_empty.png')
with A.expect_file_chooser() as fc:
    click(A, '[data-act="import-pick"]', 200)
fc.value.set_files(BASE + '/tools/test-data-nolock.json')
A.wait_for_timeout(2500)
print('store roster   :', [m['name'] for m in get_at('/rooms/' + room + '/d/meta/config')['roster']], '| subjects', len(get_at('/rooms/' + room + '/d/subjects') or {}))
print('A gate people  :', ev(A, "[...document.querySelectorAll('#view-gate .person')].map(e=>e.textContent).join(',')"), '| import card gone:', ev(A, "!document.getElementById('c-import')"))
click(A, '[data-act="who"][data-id="m1"]', 900)
ev(A, "(()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b)b.click();})()"); A.wait_for_timeout(500)
calm(A)
click(A, '#meBtn', 600)
print('A room section :', ev(A, "(document.querySelector('.rmsec')||{}).innerText.replace(/\\n/g,' ')"))
A.screenshot(path=SH + 'w_01_settings.png')
ev(A, "(()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b)b.click();})()"); A.wait_for_timeout(500)
print('A me           :', ev(A, "(document.querySelector('#meBtn')||{}).textContent"), '| tab', ev(A, "(document.querySelector('.view h1')||{}).textContent"))
A.evaluate("()=>{const b=document.querySelector('[data-act=\"cal-mode\"][data-id=\"list\"]');if(b)b.click();}");A.wait_for_timeout(600)
print('A list view  :',A.evaluate("()=>!!document.querySelector('.wk')+' '+(document.querySelector('.wkt')||{}).textContent"))
A.evaluate("()=>{const b=document.querySelector('[data-act=\"cal-mode\"][data-id=\"tt\"]');if(b)b.click();}");A.wait_for_timeout(700)
A.evaluate("()=>{const b=document.querySelector('.tttools [data-modal=\"ttset\"]');if(b)b.click();}");A.wait_for_timeout(500)
A.evaluate("()=>{const b=document.querySelector('[data-act=\"tt-new\"][data-v=\"school\"]');if(b)b.click();}");A.wait_for_timeout(300)
A.evaluate("()=>{const b=document.querySelector('[data-act=\"tt-ed-save\"]');if(b)b.click();}");A.wait_for_timeout(1200)
print('A tt saved   :',A.evaluate("()=>[...document.querySelectorAll('#dlg-ttset .ttrow b')].map(b=>b.textContent).join(',')"))
A.evaluate("()=>{const b=document.querySelector('#dlg-ttset [data-act=\"modal-close\"]');if(b)b.click();}");A.wait_for_timeout(500)
print('A tt blocks  :',A.evaluate("()=>document.querySelectorAll('.ttb.fx').length"))
A.evaluate("()=>{const b=document.querySelector('[data-act=\"cal-mode\"][data-id=\"cal\"]');if(b)b.click();}");A.wait_for_timeout(400)
A.evaluate("()=>{const b=document.querySelector('[data-act=\"cal-mode\"][data-id=\"cal\"]');if(b)b.click();}");A.wait_for_timeout(400)

# ---- 친구(B): 초대 링크로 들어오기
invite = SITE + '#db=' + DB + '&room=' + room  # 예전 초대 링크도 계속 들어와져야 한다
cb, B = newpage(w=820, h=1180)
B.goto(invite, wait_until='commit'); B.wait_for_timeout(2000)
print('B gate         :', ev(B, "(document.querySelector('#view-gate h1')||{}).textContent"), '| people', ev(B, "document.querySelectorAll('#view-gate .person').length"))
click(B, '[data-act="who"][data-id="m2"]', 900)
ev(B, "(()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b)b.click();})()"); B.wait_for_timeout(500)
calm(B)
click(B, '[data-act="tab"][data-tab="room"]', 900)
click(B, '[data-act="tmode"][data-v="pomo"]', 300)
click(B, '[data-act="timer-start"]', 800)
print('B live doc     :', json.dumps(get_at('/rooms/' + room + '/d/live/m2'), ensure_ascii=False))
click(A, '[data-act="tab"][data-tab="room"]', 1500)
print('A sees B       :', ev(A, "[...document.querySelectorAll('#c-people .fr')].map(e=>e.querySelector('b').textContent+': '+((e.querySelector('small.live')||{}).textContent||'-')).join(' | ')"))
A.screenshot(path=SH + 'w_02_A_room.png')
# 출석은 새 주기(10/12) 전이라 건너뜀
# 메시지: A가 전체방에 글, B가 이모티콘
click(A, '[data-act="tab"][data-tab="chat"]', 900)
A.fill('#msgInput', '다들 오늘 몇 시까지 해?'); click(A, '#msgSend', 800)
click(B, '[data-act="tab"][data-tab="chat"]', 1500)
print('B sees msg     :', ev(B, "[...document.querySelectorAll('#msgList .bb')].map(e=>e.textContent).slice(-2).join(' / ')"))
click(B, '#msgStk', 400); click(B, '[data-act="stk-send"]', 1200)
A.wait_for_timeout(1200)
print('A sees sticker :', ev(A, "(i=>i?(i.src.slice(0,5)+' '+i.naturalWidth+'px'):'none')([...document.querySelectorAll('#msgList .stk img')].slice(-1)[0])"))
A.screenshot(path=SH + 'w_03_A_chat.png')
print('A badge/B badge:', ev(A, "document.getElementById('chatBadge').textContent"), '/', ev(B, "document.getElementById('chatBadge').textContent"))
# 새로 고침(주소창에 초대 정보 없이) -> 저장된 연결로 다시 들어감
A.goto(SITE, wait_until='commit'); A.wait_for_timeout(2000)
print('A reload bare  :', ev(A, "(document.querySelector('.view h1')||{}).textContent"), '| hash', ev(A, "location.hash?'있음':'없음'"))
# 쓰기 거절(규칙 잘못) 안내
DENY_WRITES['on'] = True
click(A, '[data-act="tab"][data-tab="room"]', 900)
click(A, '[data-act="timer-start"]', 2500)
print('A denied banner:', ev(A, "(document.querySelector('#banner .notice')||{}).textContent"))
DENY_WRITES['on'] = False
# 연결 끊기
click(A, '#meBtn', 600); click(A, '[data-act="setup-reset"]', 300); click(A, '[data-act="setup-reset"]', 1500)
print('A after reset  :', ev(A, "(document.querySelector('#view-setup h1')||{}).textContent"), '| saved', ev(A, "localStorage.getItem('gbb_remote')"))
B.screenshot(path=SH + 'w_04_B_chat.png')
# 휴대폰 폭 연결 화면
cc, C = newpage(w=390, h=800, scale=2)
C.goto(SITE, wait_until='commit'); C.wait_for_timeout(1500); C.screenshot(path=SH + 'w_05_phone_setup.png')
print('phone overflow :', ev(C, "document.documentElement.scrollWidth>innerWidth"))
# 실제 기록 파일 형식 확인(다른 방에 가져오기)
C.fill('#setupIn', DB); click(C, '[data-act="setup-go"]', 1500)
with C.expect_file_chooser() as fc2:
    click(C, '[data-act="import-pick"]', 200)
fc2.value.set_files('/mnt/user-data/outputs/web/planner-data.json'); C.wait_for_timeout(2500)
r2 = ev(C, "JSON.parse(localStorage.getItem('gbb_remote')).room")
print('real file      :', ev(C, "[...document.querySelectorAll('#view-gate .person')].length+'명'"), '| lock kept', bool(get_at('/rooms/' + r2 + '/d/locks/m1')), '| days', list((get_at('/rooms/' + r2 + '/d/days') or {}).keys()))
C.evaluate("()=>{const b=[...document.querySelectorAll('[data-act=who]')][1];if(b)b.click();}");C.wait_for_timeout(800)
C.evaluate("()=>{const b=document.querySelector('.dialog [data-act=modal-close]');if(b)b.click();}");C.wait_for_timeout(500)
C.locator('#meBtn').click();C.wait_for_timeout(700)
with C.expect_download() as dl:
    C.locator('[data-act="export-data"]').click()
fn=dl.value.suggested_filename;pth=dl.value.path();ex=json.load(open(pth,encoding='utf-8'))
print('export       :',fn,'| roster',len(ex['d']['meta']['config']['roster']),'| days',len(ex['d']['days']),'| app',ex['app'])
print('sticker img  :',C.evaluate("()=>{const i=new Image();i.src='stickers/basic-01.webp';return new Promise(r=>{i.onload=()=>r(i.naturalWidth);i.onerror=()=>r('err');});}"))
print('manifest     :',C.evaluate("()=>fetch('manifest.webmanifest').then(r=>r.json()).then(j=>j.short_name)"))
print('methods        :', sorted(set(m for m, p in LOG)))
print('errors:', errors)
br.close(); pw.stop()
