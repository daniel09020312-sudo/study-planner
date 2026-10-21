# ---------------------------------------------------------------- 처음 열 때 잠깐 보이는 화면 (앱 아이콘이 떠오르고, 준비되면 사라짐)
import re as _re
_ic = open(BASE + '/src/icon.svg', encoding='utf-8').read().strip()
for _k in ['bg', 'hl', 'sh', 'hd', 'ck', 'cc', 'rg']:
    _ic = _ic.replace('id="%s"' % _k, 'id="sp-%s"' % _k).replace('url(#%s)' % _k, 'url(#sp-%s)' % _k)
_ic = _ic.replace('<svg ', '<svg class="spic" aria-hidden="true" ', 1)
sub("<body>", "<body>\n<div id=\"splash\" role=\"status\" aria-label=\"공부방을 여는 중\"><div class=\"spin\"><span class=\"spim\">" + _ic + "</span><b class=\"spt\">공부방</b><span class=\"spbar\"><i></i></span></div></div><script>window.__sp0=Date.now();</script>")
sub("  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);", """  if(S.ready||S.setup||S.join)splashDone();
  if(S.focusAfter){var fe=document.getElementById(S.focusAfter);""")
sub("/* ---------- 공부방 ---------- */", r"""/* ---------- 처음 화면 ---------- */
function splashDone(){
  var sp=document.getElementById('splash');if(!sp||sp.getAttribute('data-out'))return;
  sp.setAttribute('data-out','1');
  var wait=reduced?0:Math.max(0,750-(Date.now()-(window.__sp0||0)));
  setTimeout(function(){sp.classList.add('out');setTimeout(function(){if(sp.parentNode)sp.parentNode.removeChild(sp);},reduced?0:520);},wait);
}
setTimeout(function(){var sp=document.getElementById('splash');if(sp&&!sp.getAttribute('data-out'))splashDone();},8000);
/* ---------- 공부방 ---------- */""")
sub("</style>", """#splash{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:var(--bg);transition:opacity .45s ease,visibility .45s}
#splash.out{opacity:0;visibility:hidden}
#splash .spin{display:flex;flex-direction:column;align-items:center;gap:14px;transition:transform .5s cubic-bezier(.3,1.4,.5,1)}
#splash.out .spin{transform:scale(1.08)}
.spim{display:block;width:96px;height:96px;border-radius:24px;overflow:hidden;box-shadow:0 16px 30px -8px rgba(26,54,150,.38);animation:spPop .7s cubic-bezier(.3,1.5,.5,1) both,spFloat 2.6s ease-in-out .7s infinite}
.spic{display:block;width:100%;height:100%}
.spt{font-size:17px;font-weight:800;letter-spacing:.08em;color:var(--ink);animation:spUp .5s ease .25s both}
.spbar{position:relative;width:72px;height:4px;border-radius:2px;background:color-mix(in srgb,var(--accent) 16%,transparent);overflow:hidden;animation:spUp .5s ease .35s both}
.spbar i{position:absolute;top:0;bottom:0;width:40%;border-radius:2px;background:var(--accent);animation:spRun 1.1s ease-in-out infinite}
@keyframes spPop{from{transform:scale(.6);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes spFloat{0%,100%{translate:0 0}50%{translate:0 -5px}}
@keyframes spUp{from{transform:translateY(8px);opacity:0}to{transform:none;opacity:1}}
@keyframes spRun{0%{left:-40%}100%{left:100%}}
@media (prefers-reduced-motion:reduce){.spim,.spt,.spbar,.spbar i{animation:none}#splash,#splash .spin{transition:none}}
</style>""")
