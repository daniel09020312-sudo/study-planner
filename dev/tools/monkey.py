# 원숭이 테스트: 화면의 단추를 무작위로 누르고 글을 써 넣으며 실행 중 예외(pageerror, console error)를 찾는다.
# 사용: python3 tools/monkey.py [실행 수=6] [단계 수=300] [시작 시드=1]
import sys, json, random, datetime
sys.path.insert(0, '/home/claude/planner/tools')
from rig import *

RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 6
STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
SEED0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1
SKIP = {'member-del', 'sub-del', 'score-reset', 'who', 'pin-set', 'pin-clear', 'pin-reset', 'pic-load', 'pick', 'lock-toggle', 'seed'}
WORDS = ['가', '수학 3단원', '<b>x</b>', '"따옴표"', '😀', 'a' * 120, '  ', '0', '-5', '99999', '한글과 english 123', "';alert(1);//"]

PICK = """()=>{
  const out=[];
  const els=document.querySelectorAll('[data-act]');
  for(const e of els){
    if(e.disabled||e.closest('[hidden]'))continue;
    const r=e.getBoundingClientRect();
    if(r.width<2||r.height<2)continue;
    const cs=getComputedStyle(e);
    if(cs.visibility==='hidden'||cs.display==='none'||cs.pointerEvents==='none')continue;
    out.push(e.getAttribute('data-act')+'|'+(e.getAttribute('data-id')||e.getAttribute('data-v')||e.getAttribute('data-tab')||e.getAttribute('data-modal')||''));
  }
  return out;
}"""

CLICK = """(sel)=>{
  const [act,key]=sel.split('|');
  const els=[...document.querySelectorAll('[data-act="'+act+'"]')].filter(e=>!e.disabled&&e.getBoundingClientRect().width>1);
  const e=els.find(x=>(x.getAttribute('data-id')||x.getAttribute('data-v')||x.getAttribute('data-tab')||x.getAttribute('data-modal')||'')===key)||els[0];
  if(!e)return false;
  e.scrollIntoView({block:'center'});
  const r=e.getBoundingClientRect();
  e.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+r.width/2,clientY:r.top+r.height/2}));
  return true;
}"""

FILL = """(txt)=>{
  const ins=[...document.querySelectorAll('input[data-draft],textarea[data-draft],input[type=date],input[type=time],select[data-chg]')].filter(e=>!e.disabled&&e.getBoundingClientRect().width>1);
  if(!ins.length)return null;
  const e=ins[Math.floor(Math.random()*ins.length)];
  if(e.tagName==='SELECT'){e.selectedIndex=Math.floor(Math.random()*e.options.length);e.dispatchEvent(new Event('change',{bubbles:true}));return 'select';}
  if(e.type==='date'){e.value='2026-11-0'+(1+Math.floor(Math.random()*9));e.dispatchEvent(new Event('change',{bubbles:true}));return 'date';}
  if(e.type==='time'){e.value='1'+Math.floor(Math.random()*9)+':'+(10+Math.floor(Math.random()*49));e.dispatchEvent(new Event('change',{bubbles:true}));return 'time';}
  e.focus();e.value=txt;e.dispatchEvent(new Event('input',{bubbles:true}));
  if(Math.random()<.5)e.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true}));
  return e.getAttribute('data-draft');
}"""

SEEDJS = """()=>{
  const S=window.__store, now=Date.now();
  const day=(d,n)=>{const a=d.split('-');const x=new Date(+a[0],+a[1]-1,+a[2]);x.setDate(x.getDate()+n);return x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0')+'-'+String(x.getDate()).padStart(2,'0');};
  const T=day(new Date().toISOString().slice(0,10),0);
  for(let i=-12;i<=6;i++){const d=day(T,i);
    S['days/m1_'+d]={goals:[{id:'k'+i+'a',text:'기출 풀이 '+i,sid:'s2',done:i%2==0},{id:'k'+i+'b',text:'오답 정리',sid:'s3',done:false,ts:600,te:660},{id:'k'+i+'c',text:'개념',sid:'s1',done:i<0}],mins:i<=0?{s2:60+i,s3:30}:{},in:i<=0?d+'T00:10:00.000Z':undefined,certAt:i<-4?d+'T13:00:00.000Z':undefined};
    if(S['days/m1_'+d].in===undefined)delete S['days/m1_'+d].in;if(S['days/m1_'+d].certAt===undefined)delete S['days/m1_'+d].certAt;}
  S['inbox/m1']={items:{a1:{t:'쎈 3단원',sid:'s2',at:1},a2:{t:'영어 단어',sid:'s4',at:2},a3:{t:'직접 쓴 할 일',at:3}}};
  S['reads/m2']={m1:now-60000,all:now-60000};
  S['plans/p1']={mid:'m1',sid:'s2',type:'문제집 풀이',unit:'문제',note:'',mode:'split',total:60,per:0,due:day(T,6),start:T,dows:'1111111',early:false,at:now};
  S['progress/m1']={units:{s2:[{id:'u1',n:'1. 지수와 로그'},{id:'u2',n:'2. 삼각함수'}]},checks:{'s2__u1__i1':true},tt:{b:[{id:'b1',k:'academy',t:'학원',sid:'s2',d:'0101010',s:1080,e:1200}],sch:{p:[{s:510,e:560},{s:570,e:620}],w:{1:{p0:{s:'s2'},p1:{t:'자습'}}}}}};
  S['events/e3']={mid:'m1',date:day(T,2),title:'수행평가',shared:true,kind:'수행평가',sid:'s2'};
  window.__fire&&window.__fire();
}"""


COV = set()


def run(seed, w, h, scheme, concept):
    rnd = random.Random(seed)
    R = Rig()
    trail = []
    errs_seen = 0
    try:
        ls = {'gbb_note': '9999999999999'}
        if concept: ls['gbb_concept'] = concept
        p = R.open(w, h, scheme=scheme, ls=ls)
        p.evaluate(SEEDJS); p.wait_for_timeout(400)
        close_dlg(p)
        for step in range(STEPS):
            try:
                r = rnd.random()
                if r < .07:
                    k = rnd.choice(WORDS); what = p.evaluate(FILL, k); trail.append('fill:%s:%r' % (what, k[:12]))
                elif r < .09:
                    p.keyboard.press('Escape'); trail.append('esc')
                elif r < .10:
                    p.evaluate("()=>window.__fire&&window.__fire()"); trail.append('fire')
                elif r < .11:
                    p.evaluate("()=>{const S=window.__store;S['msgs/r'+Date.now()]={from:'m2',to:Math.random()<.5?'all':'m1',text:'새 메시지',at:Date.now()};window.__fire();}"); trail.append('incoming-msg')
                else:
                    cands = [c for c in p.evaluate(PICK) if c.split('|')[0] not in SKIP]
                    if not cands:
                        p.keyboard.press('Escape'); trail.append('esc(empty)'); continue
                    c = rnd.choice(cands)
                    p.evaluate(CLICK, c); trail.append(c)
                p.wait_for_timeout(rnd.choice([30, 60, 120]))
            except Exception as ex:
                trail.append('EXC:' + str(ex)[:80])
            if len(R.errors) > errs_seen:
                new = R.errors[errs_seen:]; errs_seen = len(R.errors)
                return {'seed': seed, 'cfg': (w, h, scheme, concept), 'step': step, 'errors': new, 'trail': trail[-12:]}
        return None
    finally:
        COV.update(t.split('|')[0] for t in trail if '|' in t)
        R.close()


if __name__ == '__main__':
    bad = []
    cfgs = [(390, 844, 'light', None), (1180, 820, 'light', None), (390, 844, 'dark', 'night'), (820, 1100, 'light', 'paper'), (390, 844, 'light', 'news'), (1180, 820, 'dark', 'glass'), (390, 844, 'light', 'pop'), (820, 1100, 'dark', 'board')]
    for i in range(RUNS):
        cfg = cfgs[i % len(cfgs)]
        res = run(SEED0 + i, *cfg)
        print('run', SEED0 + i, cfg, 'FAIL' if res else 'ok', flush=True)
        if res:
            bad.append(res)
            print(json.dumps(res, ensure_ascii=False, indent=1)[:1800], flush=True)
    print('SUMMARY', len(bad), 'of', RUNS, 'runs hit errors; distinct actions clicked:', len(COV))
    print(sorted(COV))
