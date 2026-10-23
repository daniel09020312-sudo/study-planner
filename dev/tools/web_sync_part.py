# ---------------------------------------------------------------- 웹 판: 바뀐 것만 받기 (src/sync.js)
# build_web.py 안에서 web_offline_part.py 다음에 exec 된다. firebaseNet 전체를 sync.js의 것으로 바꾼다.
SYNC_JS = open(BASE + '/src/sync.js', encoding='utf-8').read()
_a = s.index("function firebaseNet(base,room){")
_b = s.index("\nfunction localNet(){", _a)
assert s.count("function firebaseNet(base,room){") == 1
s = s[:_a] + SYNC_JS.rstrip('\n') + s[_b:]
