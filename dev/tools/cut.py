import json,sys,os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
src,dst,shots=sys.argv[1],sys.argv[2],sys.argv[3]
items=json.load(open(os.path.join(src,'stickers.json'),encoding='utf-8'))
packs={}
out=[]
total=0
for it in items:
    p=it['pack']
    if p not in packs: packs[p]=Image.open(os.path.join(src,p+'.png')).convert('RGBA')
    x,y,w,h=it['crop']
    im=packs[p].crop((x,y,x+w,y+h))
    # 옆 칸에서 넘어온 조각 지우기: 칸 가장자리에 닿아 있고 본체보다 훨씬 작은 덩어리만 제거
    arr=np.array(im);mask=arr[:,:,3]>24
    lab,n=ndimage.label(mask,structure=np.ones((3,3)))
    if n>1:
        areas=ndimage.sum(mask,lab,range(1,n+1));big=areas.max();removed=0
        edge=set(np.unique(np.concatenate([lab[0,:],lab[-1,:],lab[:,0],lab[:,-1]])))-{0}
        for k in edge:
            if areas[k-1]<big*0.12:
                arr[lab==k]=0;removed+=1
        if removed: print(it['id'],'removed',removed,'edge fragments')
        im=Image.fromarray(arr,'RGBA')
    a=im.split()[3].point(lambda v:255 if v>24 else 0)
    bb=a.getbbox()
    pad=6
    bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(w,bb[2]+pad),min(h,bb[3]+pad))
    im=im.crop(bb)
    # 정사각형 캔버스 가운데에 배치 (표시 크기를 고르게)
    side=max(im.size)
    cv=Image.new('RGBA',(side,side),(0,0,0,0))
    cv.paste(im,((side-im.size[0])//2,(side-im.size[1])//2))
    if side>320: cv=cv.resize((320,320),Image.LANCZOS)
    fn=os.path.join(dst,it['id']+'.webp')
    cv.save(fn,'WEBP',quality=86,method=6)
    sz=os.path.getsize(fn);total+=sz
    out.append((it['id'],it['label'],it['motion'],cv.size,sz,cv))
print('files',len(out),'total KB',round(total/1024),'max KB',round(max(o[4] for o in out)/1024,1))
for bg,name in (((255,255,255),'light'),((25,27,32),'dark')):
    sheet=Image.new('RGB',(6*170,6*170),bg)
    for i,o in enumerate(out):
        t=o[5].resize((150,150),Image.LANCZOS)
        sheet.paste(t,((i%6)*170+10,(i//6)*170+10),t)
    sheet.save(os.path.join(shots,'stickers_'+name+'.png'))
json.dump([{'id':o[0],'label':o[1],'motion':o[2]} for o in out],open(os.path.join(dst,'..','src','stickers_meta.json'),'w',encoding='utf-8'),ensure_ascii=False)
