# ---------------------------------------------------------------- v83: 찌르기 알림 기본으로 켜짐. 끈 기기만 gbb_pnoff='1'. 알림 허용을 아직 안 물었으면 이름을 고른 뒤 처음 누를 때 한 번 물음(gbb_pnask)
sub("function pnOn(){try{return typeof Notification!=='undefined'&&Notification.permission==='granted'&&lsGet('gbb_pokenote')==='1';}catch(e){return false;}}",
    r"""function pnOn(){try{return typeof Notification!=='undefined'&&Notification.permission==='granted'&&lsGet('gbb_pnoff')!=='1';}catch(e){return false;}}
function pnAutoAsk(){
  try{
    if(typeof Notification==='undefined'||Notification.permission!=='default'||lsGet('gbb_pnoff')==='1'||lsGet('gbb_pnask')==='1'||!S.ready)return;
    var V=view();if(!V.me)return;
    lsSet('gbb_pnask','1');
    var r=Notification.requestPermission(function(){});
    if(r&&r.then)r.then(function(pm){if(pm==='granted'){pnApply();lsSet('gbb_pokenote','1');if(typeof pushSubscribe==='function')pushSubscribe();flash('찌르기 알림이 켜졌습니다. 설정에서 끌 수 있습니다.');S.sync=true;render();}});
  }catch(e){}
}
setTimeout(function(){document.addEventListener('click',pnAutoAsk);},0);""")
sub("flash('찌르기 알림을 껐습니다.');break;}", "lsSet('gbb_pnoff','1');flash('찌르기 알림을 껐습니다.');break;}")
sub("flash('찌르기 알림을 켰습니다.');", "lsSet('gbb_pnoff',null);flash('찌르기 알림을 켰습니다.');")
