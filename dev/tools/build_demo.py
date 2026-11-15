# 최종 결과 3D 연출 예시 페이지(web-light/final-demo.html). 이름은 모두 지어낸 이름
import os,json
BASE='/home/claude/planner'
js=open(BASE+'/src/finrev3d.js',encoding='utf-8').read()
css=open(BASE+'/src/finrev3d.css',encoding='utf-8').read()
names=['한결','하늘','가온','나래','다온','라온','마루','바다','아라','해솔','여름','겨울','자람','차미','새봄']
scores=[1512,1386,1240,988,931,874,802,744,690,612,540,433,318,186,94]
data={'title':'최종 결과 발표','period':'11/2 ~ 12/8','cut':100,'people':[{'name':n,'total':s,'me':n=='다온'} for n,s in zip(names,scores)],'prizes':['치킨 기프티콘','편의점 상품권','음료수']}
html='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex"><title>최종 결과 연출 예시</title>
<style>html,body{margin:0;height:100%;background:#05060f;color:#fff;font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR",system-ui,sans-serif}
.demo{min-height:100%;display:grid;place-items:center;align-content:center;gap:14px;text-align:center;padding:24px}
.demo h1{margin:0;font-size:28px}.demo p{margin:0;opacity:.7;font-size:14px;line-height:1.6}
.demo button{min-height:52px;padding:0 30px;border:0;border-radius:999px;font:inherit;font-size:17px;font-weight:800;color:#1a1200;background:linear-gradient(90deg,#ffd76a,#fff1c2);cursor:pointer}
'''+css+'''</style></head><body><div class="demo"><h1>최종 결과 공개 연출 예시</h1><p>이름과 점수는 모두 예시입니다.<br>실제 앱에서는 방장이 승인하면 이 연출로 공개됩니다.</p><button id="go">연출 보기</button></div>
<script>'''+js+'''
var DATA='''+json.dumps(data,ensure_ascii=False)+''';
function go(man){FR3.play(JSON.parse(JSON.stringify(DATA)),{manual:!!man,onReplay:function(){setTimeout(go,500);},onFail:function(){alert('이 기기에서는 3D 연출을 열 수 없습니다.');}});}
document.getElementById('go').onclick=go;
if(location.hash==='#auto')setTimeout(go,300);
if(location.hash==='#rec')setTimeout(function(){go(true);},300);
</script></body></html>'''
os.makedirs(BASE+'/web-light',exist_ok=True)
open(BASE+'/web-light/final-demo.html','w',encoding='utf-8').write(html)
import shutil;os.makedirs(BASE+'/web-light/vendor',exist_ok=True);shutil.copy(BASE+'/vendor/three-r128.min.js',BASE+'/web-light/vendor/three-r128.min.js')
print('demo',len(html))
