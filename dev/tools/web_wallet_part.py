# ---------------------------------------------------------------- 웹 판: 모든 방 잉크와 산 것, 관리자 무제한 (src/wallet.js)
WALLET_JS = open(BASE + '/src/wallet.js', encoding='utf-8').read()
sub("/* ---------- 공부방 ---------- */", WALLET_JS + "\n/* ---------- 공부방 ---------- */")
sub("  try{shopGf();}catch(e){}\n", "  try{shopGf();}catch(e){}\n  try{walTick();}catch(e){}\n")
