// 한 입 화학: Claude에게 물어보기 (사이트의 /api/ask)
// 열쇠는 Cloudflare Pages 설정의 비밀 값 ANTHROPIC_API_KEY 에만 둔다(저장소·앱에는 없음).
// ASK_CODE 를 정해 두면 앱 설정에 같은 코드를 넣은 기기만 물어볼 수 있다(남이 주소로 마구 쓰는 것 막기).
import Anthropic from '@anthropic-ai/sdk';

const SYSTEM = `너는 고등학생이 쓰는 퀴즈 앱 '한 입 화학' 안의 화학 질문 도우미야.
범위는 '화학 반응의 세계' 수업의 Ⅲ. 탄소 화합물과 반응(탄소 화합물의 종류·화학 반응, 고분자 화합물, 탄소 화합물의 유용성)과 Ⅱ-05 우리 생활 속 산화-환원 반응이야.
- 한국어 해요체로, 휴대폰 화면에서 읽기 좋게 짧게 답해(보통 3~8문장). 필요할 때만 짧은 목록을 써.
- 수업 PPT와 탐구활동지 용어를 그대로 써(예: 하이드록시기, 카복실기, 알데하이드기(포밀기), 에스터기, 첨가 중합, 축합 중합, 시성식).
- 학생이 외우기 쉽게 핵심을 먼저 말하고, 왜 그런지 한 줄로 이어 줘. 헷갈리기 쉬운 짝이 있으면 함께 구별해 줘.
- 화학식은 C6H12O6, CH3COOH처럼 그대로 써.
- 모르는 것이나 수업 범위를 넘는 것은 그렇다고 말해.
- 문제 정보가 함께 오면 그 문제를 기준으로 설명해. 학생이 고른 답이 왜 틀렸는지도 짚어 줘.`;

const MAX_TURNS = 16, MAX_LEN = 2000, MAX_CTX = 4000;

function bad(msg, status) {
  return new Response(JSON.stringify({ error: msg }), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });
}

export async function onRequestPost({ request, env }) {
  if (!env.ANTHROPIC_API_KEY) return bad('no-key', 503);
  if (env.ASK_CODE && request.headers.get('x-ask-code') !== env.ASK_CODE) return bad('code', 401);
  let body;
  try { body = await request.json(); } catch (e) { return bad('bad-json', 400); }
  const msgs = Array.isArray(body.messages) ? body.messages.slice(-MAX_TURNS) : [];
  const messages = [];
  for (const m of msgs) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string') return bad('bad-msg', 400);
    const t = m.content.slice(0, MAX_LEN).trim();
    if (!t) continue;
    if (messages.length && messages[messages.length - 1].role === m.role) messages[messages.length - 1].content += '\n' + t;
    else messages.push({ role: m.role, content: t });
  }
  while (messages.length && messages[0].role !== 'user') messages.shift();
  if (!messages.length || messages[messages.length - 1].role !== 'user') return bad('no-question', 400);
  const ctx = typeof body.ctx === 'string' ? body.ctx.slice(0, MAX_CTX) : '';

  const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  const enc = new TextEncoder();
  const out = new ReadableStream({
    async start(controller) {
      try {
        const stream = client.beta.messages.stream({
          model: 'claude-opus-5-5',
          max_tokens: 4000,
          betas: ['server-side-fallback-2026-07-01'],
          fallbacks: 'default',
          output_config: { effort: 'low' },
          system: SYSTEM + (ctx ? '\n\n학생이 지금 보고 있는 문제:\n' + ctx : ''),
          messages,
        });
        stream.on('text', (t) => controller.enqueue(enc.encode(t)));
        const final = await stream.finalMessage();
        if (final.stop_reason === 'refusal') controller.enqueue(enc.encode('\n\n(이 질문에는 답할 수 없어요. 다르게 물어봐 주세요.)'));
        else if (final.stop_reason === 'max_tokens') controller.enqueue(enc.encode('\n\n(답이 길어서 여기서 끊겼어요. "이어서"라고 물어보세요.)'));
      } catch (e) {
        const st = e && e.status;
        controller.enqueue(enc.encode('\n\n(' + (st === 429 ? '질문이 많아서 잠깐 쉬어야 해요. 조금 뒤에 다시 물어봐 주세요.' : '지금은 답을 받지 못했어요. 잠시 뒤 다시 시도해 주세요.') + ')'));
      }
      controller.close();
    },
  });
  return new Response(out, { headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' } });
}
