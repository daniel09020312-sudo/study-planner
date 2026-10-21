# 공부방 플래너 저장소

친구들과 쓰는 공유 공부 플래너. 한 파일짜리 HTML 앱이고 Firebase Realtime Database로 기록을 나눈다.
Cloudflare Pages가 `main`의 `public/` 폴더를 study-planner-2tk.pages.dev 로 배포한다.

## 사용자와 일하는 방식
- 한국어로 짧게 답하고 이모티콘은 쓰지 않는다.
- 고쳐 달라는 요청은 수정, 테스트, `main`에 push, 배포 확인까지 바로 한다.
- 같은 앱의 Claude 아티팩트 판(capabilities db, user)도 함께 맞춘다. 아티팩트 주소는 사용자에게 확인한다.

## 폴더
- `public/` 배포되는 파일(빌드 결과). index.html, manifest.webmanifest, 아이콘, stickers/
- `dev/src/` 원본: 바탕 HTML(planner_v9_backup.html), add.css, tt.js, school.js, wkdrag.js, icon.svg 등
- `dev/tools/` 빌드 스크립트, 수정 조각(timer_part.py, v10_part.py ~ v21_part.py), 브라우저 테스트(t_*.py, rig.py)
- 웹 판에만 들어가는 기능: `dev/tools/build_web.py`가 마지막에 `web_rooms_part.py`(방, 참여 코드)를 실행한다. JS는 `src/rooms.js`.

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
cp web-light/index.html <저장소>/public/index.html
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

## 기능별 원본 위치
- v16 wkdrag.js: 할 일 주간 달력 끌기 / v17 lapse.js: 게시판 타임랩스(영상을 장면 묶음으로 줄여 pics/<id>_c0.. 에 저장)
- v18 evview.js: 일정 보기(학교 행사·시험과 수행평가) / v19: 할 일 점수(NEWRULE부터 모두 끝내고 인증), 지난 날 할 일 보호(guardDay), 내 할 일 숨기기
- v20 award.js: 배지 등급과 점수, 주간 우승 점수, 최종 결과(END 다음 날 공개), 선물과 벌칙 룰렛 / v21 units.js: 단원별 진도

## 고치는 방법
- build.py는 바탕 HTML을 `sub(찾을 글, 바꿀 글)`로 고친다. 찾을 글이 정확히 한 번 있어야 한다.
- 새 기능은 새 `tools/vNN_part.py`를 만들고 build.py 끝의 exec 목록에 더한다. JS는 `src/*.js`, CSS는 `src/add.css`에 둔다.
- 테스트는 Playwright(`tools/rig.py`가 가짜 저장소를 붙인다). 요일에 따라 결과가 달라지는 테스트는 `R.open(..., now=날짜)`로 날짜를 고정한다.
- t_site.py, t_web.py의 기록 가져오기 시험은 실제 기록이 든 파일(tools/test-data-nolock.json)을 쓰므로 저장소에는 없다. 필요하면 가짜 데이터로 만든다.

## 올리면 안 되는 것 (공개 저장소)
- 기록 파일(planner-data*.json)과 실제 기록을 담은 테스트 데이터
- 친구들의 실제 이름, Firebase 주소, 초대 링크(#db=...&room=...)
