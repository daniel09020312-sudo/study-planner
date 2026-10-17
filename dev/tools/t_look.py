# 컨셉별 화면 캡처
import sys,json,base64
sys.path.insert(0,'/home/claude/planner/tools')
from rig import *
from PIL import Image
SH='/home/claude/planner/shots/'
pic='data:image/jpeg;base64,'+base64.b64encode(open(SH+'small.jpg','rb').read()).decode()
combos=json.loads(sys.argv[1])   # [[concept, theme, accent], ...]
screens=sys.argv[2].split(',')
w,h=(int(x) for x in (sys.argv[3] if len(sys.argv)>3 else '1180x820').split('x'))
R=Rig();made=[]
for concept,theme,accent in combos:
    ls={'gbb_concept':concept,'gbb_theme':theme,'gbb_accent':accent,'gbb_note':str(9999999999999)}
    p=R.open(w=w,h=h,ls=ls,sample_pic=pic,scheme='light');close_dlg(p)
    tag=f'{concept}_{theme}_{accent}'
    if concept=='basic' and theme=='light' and accent=='blue':
        print('font attr:',p.evaluate("()=>document.documentElement.getAttribute('data-font')"))
    else:
        print(tag,'font:',p.evaluate("()=>document.documentElement.getAttribute('data-font')"),'| h1 font:',p.evaluate("()=>getComputedStyle(document.querySelector('.vhead h1')).fontFamily.split(',')[0]"))
    for sc in screens:
        if sc=='cal': click(p,'[data-tab="cal"]',700)
        elif sc=='room': click(p,'[data-tab="room"]',900)
        elif sc=='chat':
            click(p,'[data-tab="chat"]',600);click(p,'[data-act="chan"][data-id="m2"]',900)
            p.evaluate("()=>{const e=document.querySelector('#msgList .mrowx.mine [data-act=\"msg-pick\"]');if(e)e.click();}");p.wait_for_timeout(300)
        elif sc=='set': 
            click(p,'#meBtn',700)
        elif sc=='play': click(p,'[data-tab="play"]',900)
        elif sc=='rank': click(p,'[data-tab="rank"]',900)
        elif sc=='report': click(p,'[data-tab="report"]',900)
        elif sc=='prog':
            click(p,'[data-tab="prog"]',700);click(p,'[data-act="prog-toggle"]',400)
        p.wait_for_timeout(2700 if sc=='chat' else 500)
        fn=SH+f'k_{tag}_{sc}.png';p.screenshot(path=fn);made.append(fn)
        if sc=='set': close_dlg(p)
    p.close()
print('errors:',R.errors);R.close()
# 묶음 이미지
cols=len(screens)
tw=int(sys.argv[4]) if len(sys.argv)>4 else 590
ims=[Image.open(f).convert('RGB') for f in made]
th=int(ims[0].height*tw/ims[0].width)
rows=len(combos)
sheet=Image.new('RGB',(cols*tw+(cols-1)*8,rows*th+(rows-1)*8),(120,120,120))
for i,im in enumerate(ims):
    sheet.paste(im.resize((tw,th),Image.LANCZOS),((i%cols)*(tw+8),(i//cols)*(th+8)))
out=SH+'sheet_'+(sys.argv[5] if len(sys.argv)>5 else 'x')+'.png';sheet.save(out);print(out,sheet.size)
