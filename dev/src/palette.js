/* ---------- 과목 색: 무지개 기본, 파스텔, 원색, 차분한 색, 직접 고르기 ---------- */
var DEF_RAINBOW=['#E5484D','#F08A3A','#E3B21B','#2FA36B','#2E9FD8','#3E6FE0','#5352C9','#8E54D9','#E0559B','#17A2A6','#7CB342','#B8642A'];
var PALS=[
  {n:'무지개',c:[['#E5484D','빨강'],['#F08A3A','주황'],['#E3B21B','노랑'],['#7CB342','연두'],['#2FA36B','초록'],['#17A2A6','청록'],['#2E9FD8','하늘'],['#3E6FE0','파랑'],['#5352C9','남색'],['#8E54D9','보라'],['#E0559B','분홍']]},
  {n:'파스텔',c:[['#F4A3A3','파스텔 빨강'],['#F8C39A','파스텔 주황'],['#F3DC8A','파스텔 노랑'],['#C5E3A0','파스텔 연두'],['#A6D9BD','파스텔 초록'],['#9DD9D8','파스텔 청록'],['#A6D1F2','파스텔 하늘'],['#A9BCF2','파스텔 파랑'],['#B6B2EC','파스텔 남색'],['#CDB1F0','파스텔 보라'],['#F2B1D2','파스텔 분홍']]},
  {n:'원색',c:[['#FF1F1F','원색 빨강'],['#FF7A00','원색 주황'],['#FFD000','원색 노랑'],['#7ED321','원색 연두'],['#00B050','원색 초록'],['#00B5B5','원색 청록'],['#00A2FF','원색 하늘'],['#1556FF','원색 파랑'],['#3A2BD6','원색 남색'],['#8A2BE2','원색 보라'],['#FF2D95','원색 분홍']]},
  {n:'차분한',c:[['#A63A3A','진한 빨강'],['#B8642A','진한 주황'],['#B08A1A','겨자'],['#5E7F2E','진한 연두'],['#2E7D57','진한 초록'],['#1F7A7A','진한 청록'],['#2D7AAE','진한 하늘'],['#2F4FA8','진한 파랑'],['#3B3A8C','진한 남색'],['#6A3FA0','진한 보라'],['#A33D6E','진한 분홍']]}
];
function hexOk(v){return typeof v==='string'&&/^#[0-9a-fA-F]{6}$/.test(v);}
function fgOn(c){if(!hexOk(c))return '#fff';var r=parseInt(c.slice(1,3),16)/255,g=parseInt(c.slice(3,5),16)/255,b=parseInt(c.slice(5,7),16)/255;function f(x){return x<=.03928?x/12.92:Math.pow((x+.055)/1.055,2.4);}var L=.2126*f(r)+.7152*f(g)+.0722*f(b);return L>.45?'#1F2328':'#FFFFFF';}
document.addEventListener('change',function(e){
  var t=e.target;if(!t||!t.classList||!(t.classList.contains('scpick')||t.classList.contains('hexin')))return;
  var v=String(t.value||'').trim(),id=t.getAttribute('data-id');if(v&&v[0]!=='#')v='#'+v;
  if(!hexOk(v)){if(t.classList.contains('hexin'))flash('색상 코드는 #과 6자리로 적어 주세요. 예: #4A86F0');return;}
  setTimeout(function(){editProg(function(p){var c=obj(p.scol);c[id]=v.toUpperCase();p.scol=c;});render();},0);
});
