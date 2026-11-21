# ---------------------------------------------------------------- v101: 노동요 칸 정리(한 줄 목록, 더 보기, 펼치기), 노동요 댓글(progress.scm), 방장 노동요 기록 창(songadm) (src/v101.js)
V101_JS = open(BASE + '/src/v101.js', encoding='utf-8').read()
sub("function songsCard(V,k){\n  var likes={},hear={}", "function songsCard0(V,k){\n  var likes={},hear={}")
sub("/* ---------- 공부방 ---------- */", V101_JS + "\n/* ---------- 공부방 ---------- */")
sub("  if(t==='egg7')return modalEgg(V);", "  if(t==='egg7')return modalEgg(V);\n  if(t==='songadm')return modalSongAdm(V);")
sub("    case 'song-adm':S.songAdm=!S.songAdm;break;", r"""    case 'song-adm':S.songAdmTab='people';S.songAdmP=null;S.modal={type:'songadm'};S.closing=false;break;
    case 'songadm-tab':S.songAdmTab=id;break;
    case 'songadm-p':S.songAdmP=S.songAdmP===id?null:id;break;
    case 'song-x':S.songOpen=S.songOpen===id?null:id;S.songTagEdit=null;break;
    case 'song-lim':{var lim0=Math.max(SONG_LIM,+S.songLim||0);S.songLim=id==='more'?lim0+10:SONG_LIM;if(id!=='more'){var scx=document.getElementById('c-songs');if(scx&&scx.scrollIntoView)setTimeout(function(){scx.scrollIntoView({block:'start'});},30);}break;}
    case 'song-cadd':songCAdd(id);break;
    case 'song-cdel':{var cp=String(id).split('|'),cm0=cp[0],cid=cp[1],Vc=view();if(!cid||!need())break;if(cm0!==Vc.me&&adminId(Vc)!==Vc.me)break;if(prev!=='scm:'+cid){S.confirm='scm:'+cid;break;}if(cm0===Vc.me)editProg(function(p){if(p.scm)delete p.scm[cid];});else{var pb=clone(obj(Vc.progress[cm0])),pa=clone(pb);if(pa.scm)delete pa.scm[cid];savePatch('progress/'+cm0,pb,pa);}break;}""")
sub("S.songFilter='';S.songRoll=null;S.songShow={};", "S.songFilter='';S.songRoll=null;S.songShow={};S.songLim=0;S.songOpen=null;")
sub("</style>", open(BASE + '/src/v101.css', encoding='utf-8').read() + "</style>")
