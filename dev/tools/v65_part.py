# ---------------------------------------------------------------- v65: 관리자 코드 칸에 한글 입력(type=password는 아이폰에서 한글 자판이 안 나옴 -> text + 가림 CSS), 확인은 칸의 글을 바로 읽음
sub("case 'adm-go':{var acd=String(S.draft.admCode||'').trim();", "case 'adm-go':{var acdEl=document.getElementById('admCode'),acd=String((acdEl&&acdEl.value)||S.draft.admCode||'').trim();")
