# ---------------------------------------------------------------- v88: 할 일 모음 크게 보기(이 기기 gbb_ibbig, ib-big): 창을 화면 가득(.dialog.ibbig), 과목별 보기는 과목마다 세로 칸(.ibcols > .ibcol)으로 나란히, 아래 날짜·골고루 나누기는 옆으로 펼쳐 낮게
sub("function modalInbox(V){", "function ibBig(){return lsGet('gbb_ibbig')==='1';}\nfunction modalInbox(V){")
sub("return dlg('wide',{id:'inbox',t:'할 일 모음'},b,f);", "return dlg('wide'+(ibBig()?' ibbig':''),{id:'inbox',t:'할 일 모음<button class=\"btn small soft ibbigb\" data-act=\"ib-big\" aria-pressed=\"'+(ibBig()?'true':'false')+'\">'+(ibBig()?'작게 보기':'크게 보기')+'</button>'},b,f);")
sub("+(nsel===list.length?'모두 풀기':'모두 고르기')+'</button></div><ul class=\"iblist\">';\n    var ibg=ibBySub(),ibPrev=null,ibCnt={},ibOn={};",
    "+(nsel===list.length?'모두 풀기':'모두 고르기')+'</button></div>';\n    var ibg=ibBySub(),ibPrev=null,ibCnt={},ibOn={},ibCol=ibBig()&&ibg;\n    b+=ibCol?'<div class=\"ibcols\"><section class=\"ibcol\"><ul class=\"iblist\">':'<ul class=\"iblist'+(ibBig()?' ibflow':'')+'\">';")
sub("if(gk!==ibPrev){ibPrev=gk;var all=", "if(gk!==ibPrev){if(ibCol&&ibPrev!==null)b+='</ul></section><section class=\"ibcol\"><ul class=\"iblist\">';ibPrev=gk;var all=")
sub("    b+='</ul>';\n    var isubs={};", "    b+=ibCol?'</ul></section></div>':'</ul>';\n    var isubs={};")
sub("    case 'ib-view':", "    case 'ib-big':lsSet('gbb_ibbig',ibBig()?null:'1');break;\n    case 'ib-view':")
