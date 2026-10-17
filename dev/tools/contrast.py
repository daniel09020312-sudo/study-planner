import json,sys
def lum(h):
    h=h.lstrip('#');r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c:c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    la,lb=lum(a),lum(b)
    if la<lb:la,lb=lb,la
    return (la+0.05)/(lb+0.05)
def mix(a,b,p):
    a=a.lstrip('#');b=b.lstrip('#')
    return '#'+''.join('%02X'%round(int(a[i:i+2],16)*p+int(b[i:i+2],16)*(1-p)) for i in (0,2,4))
A=json.load(open(sys.argv[1]))
bad=0
LS,DS='#FFFFFF','#191B20'
for a in A:
    l,d=a['l'],a['d']
    rows=[('L on/fill',cr(l['on'],l['a']),4.5),('L ink/white',cr(l['ink'],LS),4.5),('L ink/soft',cr(l['ink'],l['soft']),4.5),('L mark/white',cr(l['mark'],LS),1.5),
          ('D on/fill',cr(d['on'],d['a']),4.5),('D ink/surface',cr(d['ink'],DS),4.5),('D ink/soft',cr(d['ink'],d['soft']),4.5),('D mark/surface',cr(d['mark'],DS),3.0)]
    line=a['id'].ljust(9)+' '.join('%s %.1f%s'%(n.split(' ')[1][:9],v,'' if v>=t else '!!') for n,v,t in rows)
    bad+=sum(1 for n,v,t in rows if v<t)
    print(line)
# 강제 어두운 컨셉(칠판, 밤하늘) 위에서의 글자 대비
for name,surf,ink3,ink2 in (('board','#24443A','#9DB5A8','#C9D6CC'),('board-bg','#1E3A31','#9DB5A8','#C9D6CC'),('night','#151A3F','#8F98CC','#B9C0EC'),('night-bg','#0B0F2A','#8F98CC','#B9C0EC'),('grid-d','#1B1F26','#7C828D','#B3B8C2')):
    print(name.ljust(9),'ink3 %.1f ink2 %.1f'%(cr(ink3,surf),cr(ink2,surf)),'| accents:',' '.join('%s %.1f'%(a['id'][:4],cr(a['d']['ink'],mix(a['d']['a'],surf,0.2))) for a in A))
print('problems',bad)
