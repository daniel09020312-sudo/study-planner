# v63: 관리자 무제한 끄기/다시 켜기. 시험용 열쇠를 만들어 site/index.html의 ADM_PUB만 바꿔서 시험(진짜 관리자 코드는 쓰지 않음)
import os, sys, json, subprocess
os.environ['LIGHT'] = '1'
key = json.loads(subprocess.check_output(['node', '-e', "crypto.subtle.generateKey({name:'ECDSA',namedCurve:'P-256'},true,['sign','verify']).then(k=>crypto.subtle.exportKey('jwk',k.privateKey)).then(j=>console.log(JSON.stringify(j)))"]))
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
shop(D); click(D, '[data-act="adm-open"]', 400); D.fill('#admCode', key['d']); click(D, '[data-act="adm-go"]', 2000)
check('unlimited on', bool((W().get(w1) or {}).get('unl')), flash(D))
check('off button', ev(D, "!!document.querySelector('[data-act=\"adm-off\"]')"))
click(D, '[data-act="adm-off"]', 300); click(D, '[data-act="adm-off"]', 2000)
check('unl removed', not (W().get(w1) or {}).get('unl'), flash(D))
close(D)
t = wallet_text(D)
check('wallet shows normal ink', '무제한' not in t and '150' in t, t)
go(D, RA); D.wait_for_timeout(8000)
check('not re-signed after reload', not (W().get(w1) or {}).get('unl'))
shop(D)
check('re-enable button', ev(D, "!!document.querySelector('[data-act=\"adm-on\"]')"))
click(D, '[data-act="adm-on"]', 2000)
check('unlimited back on', bool((W().get(w1) or {}).get('unl')), flash(D))
print('ALL OK' if ok else 'SOME FAILED')
