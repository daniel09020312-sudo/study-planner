# ---------------------------------------------------------------- v36: 다른 방과 잉크 같이 쓰기는 연동 코드로만 (웹 판 지갑은 src/wallet.js)
sub("    case 'shop-cat':", r"""    case 'wal-open':S.walLinkOpen=!S.walLinkOpen;S.walCode=null;S.draft.walLink='';S.sync=true;break;
    case 'wal-code':if(WALH.code)WALH.code();break;
    case 'wal-copy':if(S.walCode&&typeof copyText==='function')copyText(S.walCode,'연동 코드를 복사했습니다.',document.getElementById('walCodeT'));break;
    case 'wal-link':{var wlc=String(S.draft.walLink||'');if(WALH.link)WALH.link(wlc);break;}
    case 'wal-unlink':if(prev!=='walun'){S.confirm='walun';break;}if(WALH.unlink)WALH.unlink();break;
    case 'shop-cat':""")
sub("  if(type==='shop'){S.giftOpen=false;S.admOpen=false;S.draft.admCode='';}", "  if(type==='shop'){S.giftOpen=false;S.admOpen=false;S.draft.admCode='';S.walLinkOpen=false;S.walCode=null;}")
