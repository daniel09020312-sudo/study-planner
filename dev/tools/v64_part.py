# ---------------------------------------------------------------- v64: 무제한이었던 동안 보낸 선물은 내 잉크에서 빼지 않음(지갑 uh), 관리자 산 물건 하나씩 되돌리기
sub("function inkLocal(V){", r"""function unlWin(at){if(!WAL.on)return false;var uh=obj(WAL.uh);return Object.keys(uh).some(function(k){var a=+k||0,b=+uh[k]||0;return at>=a&&(!b||at<=b);});}
function inkLocal(V){
  var r0=inkLocal0(V);if(!WAL.on||!Object.keys(obj(WAL.uh)).length)return r0;
  var g={},cut=false;Object.keys(obj(V.gifts)).forEach(function(k){var x=obj(V.gifts[k]);if(x.from===V.me&&unlWin(+x.at||0)){cut=true;return;}g[k]=V.gifts[k];});
  if(!cut)return r0;var V2=Object.create(V);V2.gifts=g;return {e:r0.e,gi:r0.gi,go:inkLocal0(V2).go};
}
function inkLocal0(V){""")
sub("    case 'adm-go':", "    case 'adm-rvlist':S.admRv=!S.admRv;break;\n    case 'adm-rv1':{if(prev!=='rv1:'+id){S.confirm='rv1:'+id;break;}var Vr1=view();if(!Vr1.me||!need())break;var it1=shopItem(id);if(shopRevokeOne(Vr1,id))flash(jos(it1.name,'을','를')+' 되돌렸습니다.');break;}\n    case 'adm-go':")
