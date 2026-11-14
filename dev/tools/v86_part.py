# ---------------------------------------------------------------- v86: 할 일 모음 적기 칸을 창 위에 붙여 늘 보이게(.ibadd sticky), 과목 묶음 머리에 '+ 추가'(ib-addsub: 그 과목으로 적기 칸에)
sub("+(all?'풀기':'모두 고르기')+'</button></li>';", "+(all?'풀기':'모두 고르기')+'</button>'+(gk?'<button class=\"linkbtn ibgadd\" data-act=\"ib-addsub\" data-v=\"'+esc(gk)+'\">+ 추가</button>':'')+'</li>';")
sub("    case 'ib-view':", "    case 'ib-addsub':{if(!S.ib)break;S.ib.sid=el.getAttribute('data-v')||'';S.focusAfter='ibText';var ibdb=document.querySelector('#dlg-inbox .db');if(ibdb)ibdb.scrollTop=0;break;}\n    case 'ib-view':")
