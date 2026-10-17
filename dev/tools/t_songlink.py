import sys
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
SH='/home/claude/planner/shots/'
R=Rig();p=R.open(ls={'gbb_note':'1'});close_dlg(p)
st=lambda expr:p.evaluate('()=>'+expr)
click(p,'[data-tab="room"]',900)
p.evaluate("()=>document.getElementById('c-songs').scrollIntoView()");p.wait_for_timeout(300)
p.screenshot(path=SH+'l_00_empty_form.png')
hint=lambda: st("(document.querySelector('#songNew .hint')||{}).textContent||''")
dis=lambda: st("document.getElementById('songAdd').disabled")
# 이름만
p.fill('#songIn','새벽 감성 플리');p.wait_for_timeout(250);print('name only  :',hint(),'| disabled',dis(),'| focus',st('document.activeElement.id'))
# 이름 + 링크
p.fill('#songUrl','https://youtu.be/xyz987');p.wait_for_timeout(250);print('name + link:',hint(),'| disabled',dis(),'| focus',st('document.activeElement.id'),'| name kept',repr(st("document.getElementById('songIn').value")))
click(p,'[data-act="song-mood"][data-id="잔잔한"]');p.screenshot(path=SH+'l_01_both.png')
# 잘못된 링크
p.fill('#songUrl','유튜브에 있음');p.wait_for_timeout(250);print('bad link   :',hint(),'| disabled',dis())
# 주소 앞부분 없이
p.fill('#songUrl','youtu.be/xyz987');p.wait_for_timeout(250);print('no scheme  :',hint(),'| disabled',dis())
p.focus('#songUrl');p.keyboard.press('Enter');p.wait_for_timeout(500)
print('saved      :',st("JSON.stringify(Object.values(window.__store).filter(x=>x&&x.title==='새벽 감성 플리').map(x=>({title:x.title,url:x.url,mood:x.mood}))[0])"),'| inputs',repr(st("document.getElementById('songIn').value")),repr(st("document.getElementById('songUrl').value")))
# 링크만
p.fill('#songUrl','https://open.spotify.com/playlist/abc');p.wait_for_timeout(250);print('link only  :',hint(),'| disabled',dis())
p.fill('#songUrl','');p.wait_for_timeout(200)
# 이름 칸에 링크까지 같이 붙여넣기
p.fill('#songIn','집중 재즈 https://music.youtube.com/watch?v=jazz');p.wait_for_timeout(250);print('pasted both:',hint())
p.fill('#songIn','');p.wait_for_timeout(250)
# 이름 누르면 링크로 이동
a=p.locator('.song a.st',has_text='새벽 감성 플리')
print('anchor     :',a.get_attribute('href'),a.get_attribute('target'),'| underline:',a.evaluate("e=>getComputedStyle(e).textDecorationLine"))
with p.expect_popup() as pop:
    a.click()
pg=pop.value
p.wait_for_timeout(500)
print('popup url  :',pg.url or '(열림)')
print('listening  :',st("JSON.stringify(window.__store['progress/m1'].now&&window.__store['songs/'+window.__store['progress/m1'].now.id].title)"),'|',st("[...document.querySelectorAll('.song')].filter(e=>e.textContent.includes('새벽'))[0].querySelector('.snow span').textContent"))
pg.close()
# 예전에 올린 곡(이름과 링크)
a2=p.locator('.song a.st',has_text='빗소리 3시간')
with p.expect_popup() as pop2:
    a2.click()
print('old song   :',a2.get_attribute('href'),'-> popup opened');pop2.value.close()
p.evaluate("()=>document.getElementById('c-songs').scrollIntoView()");p.wait_for_timeout(400);p.screenshot(path=SH+'l_02_list.png')
print('errors:',R.errors);R.close()
# 휴대폰 폭
R=Rig();p=R.open(w=390,h=800,scale=2,ls={'gbb_note':'1'});close_dlg(p)
click(p,'[data-tab="room"]',900)
p.fill('#songIn','새벽 감성 플리');p.fill('#songUrl','https://youtu.be/xyz987');p.wait_for_timeout(300)
p.evaluate("()=>document.getElementById('c-songs').scrollIntoView()");p.wait_for_timeout(300);p.screenshot(path=SH+'l_03_phone.png')
print('phone overflow:',p.evaluate("()=>document.documentElement.scrollWidth>innerWidth"),'errors:',R.errors);R.close()
