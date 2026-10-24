# 공부방 플래너 저장소

친구들과 쓰는 공유 공부 플래너. 한 파일짜리 HTML 앱이고 Firebase Realtime Database로 기록을 나눈다.
Cloudflare Pages가 `main`의 `public/` 폴더를 study-planner-2tk.pages.dev 로 배포한다.

## 사용자와 일하는 방식
- 한국어로 짧게 답하고 이모티콘은 쓰지 않는다.
- 고쳐 달라는 요청은 수정, 테스트, `main`에 push, 배포 확인까지 바로 한다.
- 고칠 때는 웹사이트(GitHub, Cloudflare)만 반영한다. 같은 앱의 Claude 아티팩트 판(capabilities db, user)은 사용자가 말할 때만 맞춘다(올릴 때마다 허용을 눌러야 해서). 아티팩트 주소는 사용자에게 확인한다.
- Cloudflare 무료 요금제는 한 번에 하나씩 배포하고(20분 넘으면 실패), 한 달 500번까지다. 여러 수정은 모아서 한 번에 push한다.

## 폴더
- `public/` 배포되는 파일(빌드 결과). index.html, manifest.webmanifest, 아이콘, stickers/
- `dev/src/` 원본: 바탕 HTML(planner_v9_backup.html), add.css, tt.js, school.js, wkdrag.js, icon.svg 등
- `dev/tools/` 빌드 스크립트, 수정 조각(timer_part.py, v10_part.py ~ v30_part.py), 브라우저 테스트(t_*.py, rig.py)
- 웹 판에만 들어가는 기능: `dev/tools/build_web.py`가 마지막에 `web_rooms_part.py`(방, 참여 코드), `web_offline_part.py`(오프라인)를 실행한다. JS는 `src/rooms.js`, `src/offline.js`.
- `public/_headers`는 index.html, sw.js, version.txt를 늘 새로 받게 한다(Cloudflare Pages).
- `public/version.txt`는 빌드 번호(APP_BUILD). 열려 있는 앱이 이것과 비교해 새 판이면 창이나 입력 중이 아닐 때 저절로 다시 읽는다(web_offline_part.py). 배포할 때 index.html과 같이 올린다.
- `public/sw.js`는 `src/sw.js`를 그대로 복사한다(앱 화면을 저장해 오프라인에서도 열림). 아이콘처럼 미리 저장하는 파일을 바꾸면 sw.js의 캐시 이름(C)을 올린다.

## 작업 준비 (새 작업 공간마다)
빌드 스크립트는 `/home/claude/planner`를 기준 경로로 쓴다.
```
mkdir -p /home/claude/planner
cp -r dev/src dev/tools /home/claude/planner/
cp -r public/stickers /home/claude/planner/stickers
cd /home/claude/planner/tools/npm && npm ci
```

## 빌드와 반영
```
cd /home/claude/planner
python3 tools/build.py              # study-room-planner.html (Claude 아티팩트용)
python3 tools/build_web.py --light  # web-light/index.html (배포용, 이모티콘은 public/stickers에서 읽음)
cp web-light/index.html web-light/version.txt <저장소>/public/
cp src/sw.js <저장소>/public/sw.js   # sw.js를 바꿨을 때
```
바꾼 원본 파일은 `dev/`에도 다시 복사해서 같은 커밋에 넣는다.
push 뒤에는 `gh api repos/daniel09020312-sudo/study-planner/commits/<sha>/check-runs`로 Cloudflare Pages 성공을 확인한다.

## 방과 참여 코드 (웹 판)
- 참여 링크 `사이트#join=<저장소 이름>` -> 참여 코드 6자리 -> 이름 고르기. 평소 주소창은 `#j=<저장소 이름>`.
- 저장소 이름: `NAME-default-rtdb.REGION.firebasedatabase.app` 이면 `NAME.REGION`.
- 코드 연결은 `rooms/joincode-<코드>` = {r: 방 id, n: 방 이름}, 방 정보는 `rooms/<방>/d/meta/room` = {name, code}. Firebase 규칙은 바꾸지 않아도 된다.
- 예전 초대 링크 `#db=...&room=...`도 계속 들어와진다.
- 기기 저장 값 중 방마다 다른 것(gbb_me, gbb_auth 등)은 `키@방id`로 저장한다. 예전 판에서 쓰던 방(gbb_legacy_room)만 붙이지 않은 값을 이어서 읽는다.
- 다른 방에서 가져오기(`src/carry.js`, `web_carry_part.py`, 설정 > 방): 이 기기로 이름을 고른 적 있는 방(gbb_me@방)에서 내 일정, 오늘부터의 할 일과 마감 계획, 시간표, 과목 설정, 이 방에 없는 내 과목을 복사. 과목은 이름으로 맞추고 겹치면 건너뜀. 점수와 공부 기록(시간, 인증, 출석, 지난 할 일, reset, title)은 지금 방 방장만 보이는 따로 켜는 칸, 다시 가져와도 두 번 더해지지 않게 progress.crl[방][날짜]에 가져온 시간을 적어 둠. 가져오기와 그 되돌리기는 guardDay를 건너뜀(S.crRaw). 테스트 t_carry.py
- 이 기기에서 이 방 나가기: 목록에 다른 방이 있으면 그 방으로, 없으면 같은 저장소의 참여 코드 화면(#join=)으로
- 바뀐 것만 받기(`src/sync.js`, `web_sync_part.py`가 firebaseNet 전체를 바꿈): 쓸 때는 `rooms/<방>.json`에 PATCH 한 번으로 `d/<자리>`와 `x/<자리의 /를 |로>`=표(시각36진수.무작위)를 함께 쓴다(400이면 예전처럼 PUT). 읽을 때는 기기 저장(gbb_cache@방: t 기록, x 표, full 마지막 전체 받기, sy)으로 바로 열고 x만 실시간으로 받아 표가 다른 자리만 GET. 저장이 없거나 x가 없는 예전 저장, 이틀 넘게 못 받음, 마지막 전체 받기가 48시간(2026-10-26 전에는 1시간) 지났으면 d 전체를 한 번 받는다. 3일 지난 표는 지운다. 날마다 기록의 mid, date는 빼고 저장. 설정 > 방에 이 방 기록 크기와 이 기기의 이번 달 받은 양(gbb_dl). 테스트 t_sync.py, 가짜 Firebase는 PATCH(여러 자리)를 받는다. 테스트에서 STORE를 직접 고치면 x에도 표를 넣어야 새 판이 받는다
- 새 판 다시 읽기: 보는 중에는 다시 읽지 않고 다른 앱에서 돌아온 직후(20초 안)에 다시 읽는다. `FORCE=1 python3 tools/build_web.py --light`로 만들면 version.txt에 force가 붙어 예전처럼 쉬는 틈에 바로 다시 읽는다
- 테스트: `LIGHT=1 python3 tools/t_rooms.py` (먼저 `cp web-light/index.html site/index.html`).
- 오프라인: 받은 기록은 `gbb_cache@방`에 저장해 두고 다음에 열 때 먼저 보여 준다. 연결이 없을 때의 쓰기는 `gbb_outbox@방`에 모았다가 연결되면 올린다(사진, 영상은 막음). 테스트는 `t_offline.py`.

## 기능별 원본 위치
- v16 wkdrag.js: 할 일 주간 달력 끌기 / v17 lapse.js: 게시판 타임랩스(영상을 장면 묶음으로 줄여 pics/<id>_c0.. 에 저장)
- v18 evview.js: 일정 보기(학교 행사·시험과 수행평가) / v19: 할 일 점수(NEWRULE부터 모두 끝내고 인증), 지난 날 할 일 보호(guardDay), 내 할 일 숨기기
- v20 award.js: 배지 등급과 점수, 주간 우승 점수, 최종 결과(END 다음 날 공개), 선물과 벌칙 룰렛 / v21 units.js: 단원별 진도 / v23 calev.js: 달력 칸은 과목 줄임말 색 칩, 아래에 이번 달 수행평가 과목별 개수 / v24: 과목 줄임말 각자 정하기(progress.abbr, 설정 > 색과 줄임말) / v25 palette.js: 과목 색(기본은 과목 순서대로 무지개, 무지개·파스텔·원색·차분한, 직접 색상 코드) / v26: 처음 열 때 보이는 화면(splash): 아이콘 안 그림(달력, 고리, 체크)을 붓글씨 획순대로 한 획씩 그림. 다 그리고 앱이 준비되면(splashDone -> window.__sp.reveal) 달력 안쪽 구멍으로 앱 화면이 비치고 그림이 커지며 열림. 그리는 코드는 `<body>` 바로 뒤 작은 script(run). 앱을 새로 켤 때만 그리고, 같은 사용 중에 다시 읽힐 때(sessionStorage gbb_sp: 다른 앱에서 돌아오기, 방 옮기기)는 바로 엶. 설정 맨 아래 '앱 버전'은 빌드 시각 / v27 rules.js: 점수 규칙을 매일·매주·시험 끝나고 묶음으로 (RULE, TIERS, WEEK_BONUS 값을 그대로 읽음) / v28 (school.js + v28_part.py): 학교 시간표 칸에 선생님(tc)·장소(r), 같은 과목 두 선생님은 시간표와 알림에 선생님 이름 표시, 연달아 있는 같은 수업(쉬는 시간 20분 이하)은 이어 붙여 보이고 알림은 한 번. 수업 알림은 시작 전 정각부터 시작 10분 뒤까지 화면 위 줄(schNowHtml, 주말·쉬는 날 제외). 기본 교시 8:30 시작. 할 일 편집 > 상세 편집은 추가 창을 그 할 일로 채워 엶(goalParse, 새 할 일은 ct/ca/cu/cn 저장) / v29: 시간표 화면에 학교 수업을 교시마다(schItems, 고정 '학교' 덩어리는 그날 숨김, 빈 시간 채우기도 피함), APP_BUILD. Firebase는 열쇠가 숫자인 묶음(요일 1~5)을 배열로 돌려주므로 schW로 다시 묶음으로 읽는다. 시험용 가짜 Firebase(t_offline 등의 norm)도 같은 방식으로 배열을 돌려준다 / v30 lockscreen.js: 잠금 화면·알림창의 '지금 재생 중'에 과목과 타이머 시간(Media Session). 이 기기 설정 gbb_lock(기본 꺼짐, 공부방 타이머 아래 스위치). 켜면 타이머 동안 소리 없는 wav를 반복 재생해서 아이폰에서는 음악 앱이 멈춤. 소리는 누름 직후에만 시작할 수 있어서 앱의 누름 처리 뒤에 붙인 click 처리(lockGesture)에서 시작 / v31: 시간 고치기는 시작과 끝을 따로(시작을 바꿔도 끝은 그대로, 끝이 더 이르면 저장하지 않고 적은 값과 안내를 보여 줌, S.ttPend: 할 일 시간·그 날 고정 일정·학교 교시). 고정 일정(학원 등) 과목 여러 개: sid는 첫 과목, 두 개 이상이면 sids='s1,s3'(fxSids), 고정 일정은 과목 색 없이(할 일과 구분), 학교는 회색 빗금, 학원은 옅은 남보라 바탕에 왼쪽 점선(add.css k-academy), 칸에 과목 이름(1일 보기)이나 줄임말(3·7일) / 시간표 보기 범위는 새벽 5시 ~ 다음 날 새벽 5시(tt.js r0=5*60, r1=29*60, 시간 끝은 29*60까지) / 학교 시간표는 색 없이 회색(SGRAY): 시간표 칸, 교시 칸, 과목 고르기, 수업 알림 / v32: 과목 '후마니타스'(TEMPLATE에 더함, 이미 있는 방은 TEMPLATE 과목이 4개 이상이면 한 번만 subjects/shum 추가, meta/config migHum 표시로 다시 안 넣음) / v33: 시간표 잠금(이 기기 설정 gbb_ttlock, 시간표 도구 줄 맨 앞 단추). 잠그면 칸마다 c.lk: 끌기·길이·빈 곳 누르기·칩 놓기·채우기·창에서 시간 고치기 막힘, 블록 눌러 보기와 끝냄 표시는 됨 / v34 shop.js: 상점(왼쪽 줄 설정 바로 위 #shopBtn, 창 'shop'). 재화 '잉크'(방울): 이 방 공부 시간(타이머 + 직접 넣은 시간은 하루 RULE.manualMax까지) 10분마다 1, 남은 잉크 = 모은 잉크 - progress.shop.own 값의 합. 파는 것: 컨셉(c:), 대표 색(a:), 타이머 모양(t:), 이모티콘 팩(k:), 값은 SHOP_LOOK/SHOP_TIMER/SHOP_STK와 색 10·파스텔 15(예전에 산 것은 그때 값으로 남음). 지갑의 '오늘 +N' 표시는 .wtd(.wt는 하루별 점수 표라서 겹치면 안 됨), 기본(basic, blue, ring, 기본 팩)은 공짜. 처음 한 번 이 기기에서 쓰던 컨셉·색·타이머는 0방울로 줌(shop.gf). 설정 화면과 메시지 이모티콘에서 안 산 것은 자물쇠와 값, 누르면 상점(shopGo). 고른 모양은 예전처럼 이 기기에 저장. 새 이모티콘 팩: 그림을 stickers/와 public/stickers/에(팩이름-01.webp…), src/stickers_meta.json에 id·label·motion, build.py의 STK_PACKS에 [팩이름, 이름], shop.js SHOP_STK에 [값, 설명], build_web.py의 이모티콘 개수 assert(지금 72)도 고친다. 메시지 탭은 들어올 때마다 맨 아래(가장 최근)로 / v35: 잉크 선물(상점 지갑 > 잉크 선물하기): 방 기록 gifts/<id>={from,to,n,at}과 받는 사람에게 1:1 메시지 {gift:n}. 남은 잉크 = (공부한 분/10 + 받은 선물) - (산 값 + 보낸 선물). 모든 방 잉크(웹 판 `src/wallet.js`, `web_wallet_part.py`): 사람마다 지갑 rooms/wallet-<id>={name, own, rm:{<방>_<mid>:{e,gi,go,n,at}}, unl, to}, 방마다 progress.<me>.wal, 처음에는 방마다 따로 지갑. v36: 다른 방과 잇기는 연동 코드로만(이름으로 저절로 잇지 않음): 상점 > 다른 방과 같이 쓰기 > 연동 코드 만들기(8자, 한 번만 보임) -> rooms/walletcode-<SHA-256('gbb-link:'+코드) 앞 24자>={w}, 지갑 ck에 그 열쇠(다시 만들면 예전 것 지움). 다른 방에서 코드를 넣으면 그 방 지갑을 코드 지갑에 합치고(own, rm) 옛 지갑에 to, 다른 방도 따라옴. 이 방만 떼어 내기는 새 지갑(이 방 합계만, 산 것은 남김). 산 것은 지갑 own에도 적어 모든 방에서 씀. 관리자 무제한: 상점 맨 아래 '관리자 코드'(ECDSA P-256 비밀 열쇠, 사용자만 가짐, 저장소에 두지 않음)로 'gbb-wallet:<지갑 id>'에 서명해 unl에 두면, 누구나 wallet.js의 ADM_PUB로 확인해 무제한으로 본다(다른 지갑에 옮겨도 안 맞음). 관리자 기기는 gbb_adm에 코드, gbb_adm_w에 서명한 지갑들을 두고, 그 지갑이 합쳐져 새 지갑으로 가면 다시 서명. 관리자가 사면 0방울. 시험: t_v35.py, `ADM_CODE=<코드> LIGHT=1 python3 tools/t_wallet.py` / v37: 인증 마감 기본 29시(다음 날 새벽 5시), 예전 방은 한 번만 29로(meta/config migCert5), 설정에서 새벽 3~5시도 고름. 어제 할 일은 마감이 지나도 완료 표시를 바꿀 수 있고(doneLocked: 그제부터 막음, 할 일 더하기·빼기는 예전처럼 막음), 늦은 인증은 RULE.certLate·allLate 점수. 오늘 화면에 '어제 공부 인증 (마감 지남)' 안내와 어제 할 일 보기 / v38: 지난 날 모두(CAL_MIN부터) 할 일 완료 표시와 늦은 인증(달력에서 그 날을 눌러서, mode 'view'). doneLocked는 date<CAL_MIN만 / v39: 움직이는 이모티콘 팩 까만 고양이(cat), 하얀 강아지(dog), 냥댕이(nyang) 각 12개, 120방울. 아이폰 Safari는 움직이는 webp를 아주 느리게 돌려서, GIF 장면을 옆으로 이어 붙인 한 장(320 x 장면 수)으로 넣고 stickers_meta.json의 fr(장면마다 ms)을 STK 4번째 값으로 넘긴다. stkImg가 class sa와 @keyframes(stkSa, object-fit:cover로 한 칸, object-position을 step-end로)를 붙인다. motion은 'anim'. 숨은 팩 SHOP_HIDE={nyang:['cat','dog']}: 앞의 팩을 모두 사기 전에는 상점에 '비밀 팩'(물음표, 산 개수), 메시지 탭 이름 '비밀', 그림을 불러오지 않고 사기·보내기 막힘(shopShown, stkHid). 묶음 탭이 넘치면 옆으로 밀리고 고른 탭이 보이게. 숨은 팩이 열리면 상점에서 한 번 연출(stkReveal: 물음표 카드 흔들림, 빛줄기, 잉크·발자국·별 퍼짐, 카드 뒤집혀 이모티콘, 이 기기 gbb_rv_<팩>에 표시). 사자마자와 상점을 볼 때 매초(stkRevealTick) 확인. 시험 t_v38.py, t_v39.py, t_v39b.py(열리는 연출, 색 값) / v22: 달력 기간(CAL_MIN 2026-09 ~ CAL_MAX 2027-12, 점수 기간 START~END는 그대로)

## 고치는 방법
- build.py는 바탕 HTML을 `sub(찾을 글, 바꿀 글)`로 고친다. 찾을 글이 정확히 한 번 있어야 한다.
- 새 기능은 새 `tools/vNN_part.py`를 만들고 build.py 끝의 exec 목록에 더한다. JS는 `src/*.js`, CSS는 `src/add.css`에 둔다.
- 테스트는 Playwright(`tools/rig.py`가 가짜 저장소를 붙인다). 요일에 따라 결과가 달라지는 테스트는 `R.open(..., now=날짜)`로 날짜를 고정한다.
- t_site.py, t_web.py의 기록 가져오기 시험은 실제 기록이 든 파일(tools/test-data-nolock.json)을 쓰므로 저장소에는 없다. 필요하면 가짜 데이터로 만든다.

## 올리면 안 되는 것 (공개 저장소)
- 기록 파일(planner-data*.json)과 실제 기록을 담은 테스트 데이터
- 친구들의 실제 이름, Firebase 주소, 초대 링크(#db=...&room=...)
