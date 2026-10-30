# 찌르기 웹 푸시: 알림을 켠 기기는 구독을 progress.<나>.ps에 저장하고, 찌르면 api/push로 암호화된 요청이 간다
import os, sys, json, time, re
os.environ['LIGHT'] = '1'
_src = open('/home/claude/planner/tools/t_rooms.py', encoding='utf-8').read().split('\nimport datetime\nR1 = ')[0]
exec(_src)
TOK = 'fake-planner.asia-southeast1'
R = 'pushroomabcdef12'
STORE['rooms'] = {R: {'d': {
    'meta': {'config': {'certHour': 29, 'migCert5': 1, 'migHum': 1, 'roster': [{'id': 'm1', 'name': '민준'}, {'id': 'm2', 'name': '서연'}]}, 'room': {'name': '푸시 방', 'code': '565656'}},
    'subjects': {'s1': {'name': '국어', 'order': 1, 'items': [{'id': 'i1', 'label': '개념'}]}}}},
  'joincode-565656': {'r': R, 'n': '푸시 방'}}
ok = True
def check(n, c, x=''):
    global ok
    print(('OK  ' if c else 'FAIL'), n, x)
    if not c: ok = False
# 가짜 푸시: 구독은 진짜 P-256 열쇠로 만든다(암호화가 돌아가게)
STUB = """(()=>{window.Notification=function(){};Notification.permission='granted';Notification.requestPermission=()=>Promise.resolve('granted');
window.PushManager=function(){};window.__subs=0;
const pm={sub:null,getSubscription(){return Promise.resolve(this.sub);},subscribe(o){window.__subs++;window.__ask=o;return crypto.subtle.generateKey({name:'ECDH',namedCurve:'P-256'},true,['deriveBits']).then(k=>crypto.subtle.exportKey('raw',k.publicKey)).then(raw=>{
 const b=u=>btoa(String.fromCharCode(...new Uint8Array(u))).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'');const a=crypto.getRandomValues(new Uint8Array(16));
 const s={endpoint:'https://fcm.googleapis.com/fcm/send/'+localStorage.getItem('__who'),options:{applicationServerKey:o.applicationServerKey},toJSON(){return {endpoint:this.endpoint,keys:{p256dh:b(raw),auth:b(a)}};},unsubscribe(){pm.sub=null;window.__unsub=1;return Promise.resolve(true);}};pm.sub=s;return s;});}};
const reg={pushManager:pm,showNotification(){return Promise.resolve();}};
Object.defineProperty(navigator,'serviceWorker',{value:{ready:Promise.resolve(reg),register(){return Promise.resolve(reg);},getRegistration(){return Promise.resolve(reg);},addEventListener(){}},configurable:true});})();"""
def page(me):
    ls = {'gbb_remote': json.dumps({'url': DB, 'room': R}), 'gbb_legacy_room': '-', 'gbb_rooms': json.dumps([{'url': DB, 'room': R, 'name': '푸시 방', 'code': '565656'}]),
          'gbb_me@' + R: me, 'gbb_test': '1', 'gbb_pokenote': '1', '__who': me, 'gbb_pinask@' + R: json.dumps({'m1': 1, 'm2': 1})}
    cb, pg = newpage(w=390, h=844, ls=ls)
    pg.add_init_script(STUB)
    return cb, pg
sent = []
def on_push(route, req):
    sent.append(json.loads(req.post_data or '{}'))
    route.fulfill(status=200, content_type='application/json', body='{"status":201}')
cb2, B = page('m2')
B.goto(SITE + '#j=' + TOK, wait_until='commit'); B.wait_for_timeout(7000)
v = get_at('/rooms/webpush-vapid') or {}
check('vapid made once', bool(v.get('pub')) and bool((v.get('jwk') or {}).get('d')))
ps = (get_at('/rooms/' + R + '/d/progress/m2') or {}).get('ps') or {}
check('m2 subscription saved', ps.get('e', '').endswith('/m2') and len(ps.get('p', '')) > 80 and len(ps.get('a', '')) > 15, ps)
check('subscribed with vapid key', ev(B, "window.__ask&&window.__ask.userVisibleOnly===true&&window.__ask.applicationServerKey.length===65"))
cb1, A = page('m1')
A.route(re.compile(r'.*/api/push$'), on_push)
A.goto(SITE + '#j=' + TOK, wait_until='commit'); A.wait_for_timeout(7000)
check('vapid not replaced', (get_at('/rooms/webpush-vapid') or {}).get('pub') == v.get('pub'))
A.evaluate("()=>{const b=document.createElement('button');b.dataset.act='poke';b.dataset.id='m2';(document.querySelector('#app')||document.body).appendChild(b);b.click();}")
A.wait_for_timeout(300)
if not sent:
    A.evaluate("()=>{const s=document.querySelector('[data-act=\"poke\"]');window.__pk=s?s.outerHTML:'none';}")
    print('poke btn', ev(A, "window.__pk"))
A.wait_for_timeout(2500)
check('push request sent', len(sent) == 1, len(sent))
if sent:
    q = sent[0]
    check('to m2 endpoint', q.get('endpoint', '').endswith('/m2'), q.get('endpoint'))
    h = q.get('headers') or {}
    check('vapid auth header', h.get('Authorization', '').startswith('vapid t=') and ('k=' + v.get('pub', '')) in h.get('Authorization', ''))
    check('encrypted body', h.get('Content-Encoding') == 'aes128gcm' and len(q.get('body', '')) > 100)
# 끄면 구독 지움
B.evaluate("()=>{location.hash='#j=%s';}" % TOK)
click(B, '#meBtn', 800)
B.evaluate("()=>{const b=document.querySelector('[data-act=\"pn-toggle\"]');if(b)b.click();}"); B.wait_for_timeout(2500)
check('unsubscribed', ev(B, "window.__unsub===1") and not ((get_at('/rooms/' + R + '/d/progress/m2') or {}).get('ps')))
print('ALL OK' if ok else 'SOME FAILED')
