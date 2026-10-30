# v63: 관리자 무제한 끄기/다시 켜기. 시험용 열쇠를 만들어 site/index.html의 ADM_PUB만 바꿔서 시험(진짜 관리자 코드는 쓰지 않음)
import os, sys, json, subprocess
os.environ['LIGHT'] = '1'
PASS = '시험용 관리자 글'
key = json.loads(subprocess.check_output(['node', '-e', "const c=require('crypto');const d=c.pbkdf2Sync(Buffer.from(process.argv[1].normalize('NFC')),Buffer.from('gbb-adm-v2'),200000,32,'sha256');const e=c.createECDH('prime256v1');e.setPrivateKey(d);const P=e.getPublicKey();console.log(JSON.stringify({x:P.subarray(1,33).toString('base64url'),y:P.subarray(33).toString('base64url')}))", PASS]))
html = open('/home/claude/planner/web-light/index.html', encoding='utf-8').read()
import re
html2 = re.sub(r"var ADM_PUB=\{[^}]*\};", "var ADM_PUB={kty:'EC',crv:'P-256',x:'%s',y:'%s'};" % (key['x'], key['y']), html, count=1)
assert html2 != html
open('/home/claude/planner/site/index.html', 'w', encoding='utf-8').write(html2)
exec(open('/home/claude/planner/tools/t_wallet.py', encoding='utf-8').read().split('# ---- 기기 D')[0])
ok = True
def check(n, c, x=''):
    global ok
    print(('OK  ' if c else 'FAIL'), n, x)
    if not c: ok = False
cD, D = dev({RA: 'm1'}, RA)
w1 = prog(RA, 'm1').get('wal')
shop(D); click(D, '[data-act="adm-open"]', 400); D.fill('#admCode', PASS); click(D, '[data-act="adm-go"]', 3000)
check('unlimited on', bool((W().get(w1) or {}).get('unl')), flash(D))
# 무제한 동안 선물 5000
click(D, '[data-act="gift-open"]', 400); click(D, '#giftPanel [data-act="gift-to"][data-id="m2"]', 300); D.fill('#giftN', '5000'); D.wait_for_timeout(300)
click(D, '[data-act="gift-send"]', 300); click(D, '[data-act="gift-send"]', 1500)
check('gift sent', any(g.get('n')==5000 for g in (get_at('/rooms/%s/d/gifts' % RA) or {}).values()))
check('off button', ev(D, "!!document.querySelector('[data-act=\"adm-off\"]')"))
click(D, '[data-act="adm-off"]', 300); click(D, '[data-act="adm-off"]', 2000)
check('unl removed', not (W().get(w1) or {}).get('unl'), flash(D))
close(D)
t = wallet_text(D)
check('collected ink kept (gift while unlimited not counted)', '무제한' not in t and '150방울' in t, t)
# 산 물건 되돌리기: 잉크로 사고 되돌리면 잉크가 돌아옴
shop(D); click(D, '[data-act="shop-buy"][data-id="c:line"]', 300); click(D, '[data-act="shop-buy"][data-id="c:line"]', 1500); close(D)
t2 = wallet_text(D); print('after buy', t2)
shop(D); click(D, '[data-act="adm-rvlist"]', 400)
click(D, '[data-act="adm-rv1"][data-id="c:line"]', 300); click(D, '[data-act="adm-rv1"][data-id="c:line"]', 1200); close(D)
t3 = wallet_text(D)
check('revoked and refunded', '150방울' in t3 and 'c:line' not in json.dumps(prog(RA, 'm1').get('shop', {}).get('own', {})), t3)
# 관리자 잉크 더하기 80
shop(D); D.fill('#admInk', '80'); D.wait_for_timeout(200); click(D, '[data-act="adm-ink"]', 400); click(D, '[data-act="adm-ink"]', 1500); close(D)
t4 = wallet_text(D)
check('admin added 80 (not in collected)', '230방울' in t4 and '모은 잉크 150' in t4 and (W().get(w1) or {}).get('adj') == 80, t4)
go(D, RA); D.wait_for_timeout(8000)
check('added ink kept after reload', '230방울' in wallet_text(D))
check('not re-signed after reload', not (W().get(w1) or {}).get('unl'))
shop(D)
check('re-enable button', ev(D, "!!document.querySelector('[data-act=\"adm-on\"]')"))
click(D, '[data-act="adm-on"]', 2000)
check('unlimited back on', bool((W().get(w1) or {}).get('unl')), flash(D))
print('ALL OK' if ok else 'SOME FAILED')
