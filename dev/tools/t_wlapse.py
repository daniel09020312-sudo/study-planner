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


import os,subprocess
VID='/tmp/planner-test-lapse.webm'  # 테스트용 세로 영상(12초)이 없으면 만든다
if not os.path.exists(VID):subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','testsrc2=size=720x1280:rate=30','-t','12','-c:v','libvpx-vp9','-b:v','600k',VID],check=True)
ca, A = newpage(ls={'gbb_remote': json.dumps({'url': DB, 'room': R1}), 'gbb_me': 'm1'})
A.goto(SITE + '#db=' + DB + '&room=' + R1, wait_until='commit'); A.wait_for_timeout(2200)
click(A, '[data-act="tab"][data-tab="board"]', 900)
click(A, '[data-act="open"][data-modal="lapse"]', 600)
with A.expect_file_chooser() as fc:
    A.evaluate("()=>document.querySelector('[data-act=\"lapse-pick\"]').click()")
fc.value.set_files(VID)
A.wait_for_function("()=>!!document.querySelector('#dlg-lapse .lapse.new img')", timeout=60000)
click(A, '[data-act="lapse-up"]', 4000)
q = [k for k in STORE['rooms'][R1]['p'].keys()] if 'p' in STORE['rooms'][R1] else []
print('web stored   :', sorted(q)[:3], len(q), '| post', [v.get('kind') for v in STORE['rooms'][R1]['d'].get('quiz', {}).values()])
cb, B = newpage(w=390, h=844, ls={'gbb_remote': json.dumps({'url': DB, 'room': R1}), 'gbb_me': 'm2'})
B.goto(SITE + '#db=' + DB + '&room=' + R1, wait_until='commit'); B.wait_for_timeout(2200)
B.evaluate("()=>{const b=document.querySelector('.dialog [data-act=\"modal-close\"]');if(b)b.click();}"); B.wait_for_timeout(600)
click(B, '[data-act="tab"][data-tab="board"]', 1500)
qid = B.evaluate("()=>(document.querySelector('.q .lpv')||{dataset:{}}).dataset.id")
print('B poster     :', B.evaluate("(id)=>{const i=document.getElementById('lpi-'+id);return i&&i.tagName==='IMG'?i.naturalWidth:'none'}", qid))
click(B, '.q .lpv', 2500)
print('B plays      :', B.evaluate("(id)=>document.getElementById('lpb-'+id).style.width", qid))
print('errors', errors)
br.close(); pw.stop()
