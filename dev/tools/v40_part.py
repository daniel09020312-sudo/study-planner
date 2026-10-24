# v40: 관리자(무제한 지갑)만 상점 맨 아래 '산 이모티콘 팩 되돌리기' (두 번 눌러서). 숨은 팩 연출 표시(gbb_rv_*)도 지운다
sub("    case 'stk-send':{", r"""    case 'adm-revoke':{
      var Var=view();if(!Var.me||!inkOf(Var).unl||!need())break;
      if(prev!=='admrv'){S.confirm='admrv';break;}
      var nrv=shopRevokeStk(Var);flash(nrv?'산 이모티콘 팩 '+nrv+'개를 되돌렸습니다. 다시 사면 열리는 연출을 볼 수 있습니다.':'되돌릴 이모티콘 팩이 없습니다.');break;
    }
    case 'stk-send':{""")
