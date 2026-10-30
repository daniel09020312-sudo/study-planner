# ---------------------------------------------------------------- v63: 관리자 잉크 무제한 끄기/다시 켜기 (상점 맨 아래, 웹 판 wallet.js WALH.unlOff/unlOn)
sub("    case 'adm-go':", "    case 'adm-off':if(prev==='admoff'){if(WALH.unlOff)WALH.unlOff();}else S.confirm='admoff';break;\n    case 'adm-on':if(WALH.unlOn)WALH.unlOn();break;\n    case 'adm-go':")
