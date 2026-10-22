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
- 테스트: `LIGHT=1 python3 tools/t_rooms.py` (먼저 `cp web-light/index.html site/index.html`).
- 오프라인: 받은 기록은 `gbb_cache@방`에 저장해 두고 다음에 열 때 먼저 보여 준다. 연결이 없을 때의 쓰기는 `gbb_outbox@방`에 모았다가 연결되면 올린다(사진, 영상은 막음). 테스트는 `t_offline.py`.

## 기능별 원본 위치
- v16 wkdrag.js: 할 일 주간 달력 끌기 / v17 lapse.js: 게시판 타임랩스(영상을 장면 묶음으로 줄여 pics/<id>_c0.. 에 저장)
- v18 evview.js: 일정 보기(학교 행사·시험과 수행평가) / v19: 할 일 점수(NEWRULE부터 모두 끝내고 인증), 지난 날 할 일 보호(guardDay), 내 할 일 숨기기
- v20 award.js: 배지 등급과 점수, 주간 우승 점수, 최종 결과(END 다음 날 공개), 선물과 벌칙 룰렛 / v21 units.js: 단원별 진도 / v23 calev.js: 달력 칸은 과목 줄임말 색 칩, 아래에 이번 달 수행평가 과목별 개수 / v24: 과목 줄임말 각자 정하기(progress.abbr, 설정 > 색과 줄임말) / v25 palette.js: 과목 색(기본은 과목 순서대로 무지개, 무지개·파스텔·원색·차분한, 직접 색상 코드) / v26: 처음 열 때 보이는 화면(splash): 아이콘 안 그림(달력, 고리, 체크)을 붓글씨 획순대로 한 획씩 그림. 다 그리고 앱이 준비되면(splashDone -> window.__sp.reveal) 달력 안쪽 구멍으로 앱 화면이 비치고 그림이 커지며 열림. 그리는 코드는 `<body>` 바로 뒤 작은 script(run). 앱을 새로 켤 때만 그리고, 같은 사용 중에 다시 읽힐 때(sessionStorage gbb_sp: 다른 앱에서 돌아오기, 방 옮기기)는 바로 엶. 설정 맨 아래 '앱 버전'은 빌드 시각 / v27 rules.js: 점수 규칙을 매일·매주·시험 끝나고 묶음으로 (RULE, TIERS, WEEK_BONUS 값을 그대로 읽음) / v28 (school.js + v28_part.py): 학교 시간표 칸에 선생님(tc)·장소(r), 같은 과목 두 선생님은 시간표와 알림에 선생님 이름 표시, 연달아 있는 같은 수업(쉬는 시간 20분 이하)은 이어 붙여 보이고 알림은 한 번. 수업 알림은 시작 전 정각부터 시작 10분 뒤까지 화면 위 줄(schNowHtml, 주말·쉬는 날 제외). 기본 교시 8:30 시작. 할 일 편집 > 상세 편집은 추가 창을 그 할 일로 채워 엶(goalParse, 새 할 일은 ct/ca/cu/cn 저장) / v29: 시간표 화면에 학교 수업을 교시마다(schItems, 고정 '학교' 덩어리는 그날 숨김, 빈 시간 채우기도 피함), APP_BUILD. Firebase는 열쇠가 숫자인 묶음(요일 1~5)을 배열로 돌려주므로 schW로 다시 묶음으로 읽는다. 시험용 가짜 Firebase(t_offline 등의 norm)도 같은 방식으로 배열을 돌려준다 / v30 lockscreen.js: 잠금 화면·알림창의 '지금 재생 중'에 과목과 타이머 시간(Media Session). 이 기기 설정 gbb_lock(기본 꺼짐, 공부방 타이머 아래 스위치). 켜면 타이머 동안 소리 없는 wav를 반복 재생해서 아이폰에서는 음악 앱이 멈춤. 소리는 누름 직후에만 시작할 수 있어서 앱의 누름 처리 뒤에 붙인 click 처리(lockGesture)에서 시작 / v22: 달력 기간(CAL_MIN 2026-09 ~ CAL_MAX 2027-12, 점수 기간 START~END는 그대로)

## 고치는 방법
- build.py는 바탕 HTML을 `sub(찾을 글, 바꿀 글)`로 고친다. 찾을 글이 정확히 한 번 있어야 한다.
- 새 기능은 새 `tools/vNN_part.py`를 만들고 build.py 끝의 exec 목록에 더한다. JS는 `src/*.js`, CSS는 `src/add.css`에 둔다.
- 테스트는 Playwright(`tools/rig.py`가 가짜 저장소를 붙인다). 요일에 따라 결과가 달라지는 테스트는 `R.open(..., now=날짜)`로 날짜를 고정한다.
- t_site.py, t_web.py의 기록 가져오기 시험은 실제 기록이 든 파일(tools/test-data-nolock.json)을 쓰므로 저장소에는 없다. 필요하면 가짜 데이터로 만든다.

## 올리면 안 되는 것 (공개 저장소)
- 기록 파일(planner-data*.json)과 실제 기록을 담은 테스트 데이터
- 친구들의 실제 이름, Firebase 주소, 초대 링크(#db=...&room=...)
