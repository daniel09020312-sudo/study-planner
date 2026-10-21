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
        ct={'.html':'text/html; charset=utf-8','.webp':'image/webp','.png':'image/png','.webmanifest':'application/manifest+json'}.get(os.path.splitext(fp)[1],'application/octet-stream')
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


def newpage(w=1180, h=820, scale=1, ls=None, ua=None):
    ctx = br.new_context(viewport={'width': w, 'height': h}, device_scale_factor=scale, **({'user_agent': ua} if ua else {}))
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


STORE['rooms']['joincode-482913'] = {'r': R1, 'n': '공부방', 'at': 1}
STORE['rooms'][R1]['d']['meta']['room'] = {'name': '공부방', 'code': '482913', 'at': 1}
UAS = {'pc': None,
       'ios-chrome': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/126.0.6478.54 Mobile/15E148 Safari/604.1',
       'android': 'Mozilla/5.0 (Linux; Android 14; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
       'kakao': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 10.8.0'}
def closeall(pg, keep='a2hs'):
    for _ in range(6):
        pg.wait_for_timeout(700)
        d = pg.evaluate("(k)=>{const d=[...document.querySelectorAll('.dialog')].filter(x=>x.id!=='dlg-'+k)[0];if(d){const b=d.querySelector('[data-act=\"modal-close\"]');if(b)b.click();return d.id;}return ''}", keep)
        if not d and pg.evaluate("()=>!!document.querySelector('#dlg-a2hs')"): return
for k, ua in UAS.items():
    c, P = newpage(w=390 if k != 'pc' else 1180, h=844 if k != 'pc' else 820, ua=ua)
    P.goto(SITE + '#join=' + TOK, wait_until='commit'); P.wait_for_timeout(1300)
    inapp = P.evaluate("()=>(document.querySelector('.jinapp')||{}).textContent||''")
    P.locator('#joinCode').type('482913', delay=30); P.wait_for_timeout(2200)
    P.locator('#view-gate .person').nth(1).click(); closeall(P)
    P.wait_for_timeout(2200); closeall(P)
    t = P.evaluate("()=>{const d=document.querySelector('#dlg-a2hs');return d?d.querySelector('h2').textContent+' / '+[...d.querySelectorAll('.a2steps li')].map(l=>l.textContent).join(' > ')+' / '+((d.querySelector('.db > .hint:last-of-type')||{}).textContent||''):'none'}")
    print(k.ljust(10), '| join note:', inapp[:30] or '-', '|', t)
    if k == 'ios-chrome': P.screenshot(path=SH + 'a2hs_ios.png')
    P.evaluate("()=>{const b=document.querySelector('#dlg-a2hs [data-act=\"modal-close\"]');if(b)b.click();}"); P.wait_for_timeout(600)
    P.reload(wait_until='commit'); P.wait_for_timeout(2500); closeall(P, keep='none')
    P.wait_for_timeout(1800)
    print(' '*10, '| again after reload:', P.evaluate("()=>!!document.querySelector('#dlg-a2hs')"), '| flag', P.evaluate("()=>localStorage.getItem('gbb_a2hs')"), '| settings btn', (P.locator('#meBtn').click(), P.wait_for_timeout(600), P.evaluate("()=>!!document.querySelector('[data-modal=\"a2hs\"]')"))[2])
print('errors', errors)
br.close(); pw.stop()
