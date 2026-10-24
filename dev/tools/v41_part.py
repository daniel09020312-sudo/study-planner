# v41: 바뀐 칸만 저장하기. 예전 기록(이 기기에 저장해 둔 것, 아직 다 못 받은 것)으로 문서 전체를 덮어써서
# 다른 기기에서 바꾼 것(단원 등)이 사라지지 않도록, editProg·editDay·editDayOf·editSub는 고치기 전과 후를 비교해
# 바뀐 칸만 보낸다(S.net.patch가 있는 웹 판). 저절로 쓰는 일(certMig, humMig, shopGf, 지갑)은 새 기록을 다 받은 뒤에(netFresh)
sub("function wait(ms){return new Promise(function(r){setTimeout(r,ms);});}", r"""function wait(ms){return new Promise(function(r){setTimeout(r,ms);});}
function netFresh(){try{return !S.net||!S.net.fresh||!!S.net.fresh();}catch(e){return true;}}
/* 두 문서의 다른 칸: {'units/s1':[...], 'checks/a__b':null, ...}. 비교할 수 없거나 너무 많으면 null(문서 전체를 쓴다) */
function jdiff(a,b){
  function isO(x){return !!x&&typeof x==='object'&&!Array.isArray(x);}
  function emp(x){return x==null||(isO(x)&&!Object.keys(x).length)||(Array.isArray(x)&&!x.length);}
  if(!isO(a)||!isO(b))return null;
  var out={},n=0,bad=false;
  (function walk(x,y,p,dep){
    if(bad)return;
    if((isO(x)||x==null)&&isO(y)&&dep<5){var ks={};Object.keys(obj(x)).forEach(function(k){ks[k]=1;});Object.keys(y).forEach(function(k){ks[k]=1;});Object.keys(ks).forEach(function(k){walk(obj(x)[k],y[k],p?p+'/'+k:k,dep+1);});return;}
    if(isO(x)&&y==null&&dep<5&&dep>0){if(!emp(x)){if(++n>300){bad=true;return;}out[p]=null;}return;}
    if(emp(x)&&emp(y))return;
    if(JSON.stringify(x===undefined?null:x)===JSON.stringify(y===undefined?null:y))return;
    if(!p||/[.#$\[\]]/.test(p)){bad=true;return;}
    if(++n>300){bad=true;return;}
    out[p]=y===undefined||emp(y)?null:clone(y);
  })(a,b,'',0);
  return bad?null:out;
}
/* 바뀐 칸 묶음 합치기: 나중 것이 이긴다(조상 칸이 이미 있으면 그 안에 넣고, 자손 칸은 지운다) */
function opsMerge(a,b){
  Object.keys(b).forEach(function(k){
    Object.keys(a).forEach(function(x){if(x.indexOf(k+'/')===0)delete a[x];});
    var anc=Object.keys(a).filter(function(x){return k.indexOf(x+'/')===0;})[0];
    if(anc){var v=a[anc]&&typeof a[anc]==='object'?clone(a[anc]):{};a[anc]=setAt(v,k.slice(anc.length+1),b[k]==null?null:clone(b[k]));}
    else a[k]=b[k];
  });
  return a;
}
/* 고치기 전(base)과 후(data)를 비교해 바뀐 칸만 보낸다. 바뀐 칸만 보낼 수 없으면 예전처럼 문서 전체 */
function savePatch(path,base,data){
  if(!canWrite())return;
  data=guardDay(path,data);
  if(!S.net||!S.net.patch||BQ.has[path]){save(path,data);return;}
  var ops=jdiff(obj(base),data);
  if(ops===null){save(path,data);return;}
  if(!Object.keys(ops).length)return;
  O[path]=data;
  var w=W[path]||(W[path]={busy:false,has:false,next:null});
  if(w.has&&w.next&&w.next.__ops){opsMerge(w.next.__ops,ops);w.next.__doc=data;}
  else if(w.has){w.next=data;}
  else{w.next={__ops:ops,__doc:data};w.has=true;}
  if(!w.busy)pump(path);
}""")
sub("""    var d=w.next;w.has=false;
    try{await S.net.write(path,d);last=d;}
    catch(e){
      var code=e&&e.code;
      if(code==='unavailable'||!code){
        try{await wait(500+Math.random()*900);await S.net.write(path,d);last=d;continue;}catch(e2){code=e2&&e2.code;}
      }""", """    var d=w.next;w.has=false;
    var isOps=!!(d&&d.__ops),send=function(){return isOps?S.net.patch(path,d.__ops):S.net.write(path,d);};
    try{await send();last=isOps?d.__doc:d;w.lp=isOps;}
    catch(e){
      var code=e&&e.code;
      if(code==='unavailable'||!code){
        try{await wait(500+Math.random()*900);await send();last=isOps?d.__doc:d;w.lp=isOps;continue;}catch(e2){code=e2&&e2.code;}
      }""")
# 바뀐 칸만 보냈으면, 받아 둔 기록(다른 기기에서 바꾼 칸 포함)에 그 칸을 더한 것을 화면에 쓴다
sub("  if(ok){commit(path,last);}else{w.has=false;delete O[path];}\n  render();\n}",
    "  if(ok){var pk=w.lp&&S.net&&S.net.peek?S.net.peek(path):undefined;commit(path,pk!==undefined&&pk!==null?pk:last);}else{w.has=false;delete O[path];}\n  render();\n}")
sub("""  var d=clone(dayOf(V,V.me,date));fn(d,V);
  if(!d.certAt)delete d.certAt;if(!d.in)delete d.in;if(!d.focus)delete d.focus;
  save('days/'+V.me+'_'+date,d);""", """  var b0=clone(dayOf(V,V.me,date)),d=clone(b0);fn(d,V);
  if(!d.certAt)delete d.certAt;if(!d.in)delete d.in;if(!d.focus)delete d.focus;
  savePatch('days/'+V.me+'_'+date,b0,d);""")
sub("""  var d=clone(dayOf(V,mid,date));fn(d,V);
  if(!d.certAt)delete d.certAt;if(!d.in)delete d.in;if(!d.focus)delete d.focus;
  save('days/'+mid+'_'+date,d);""", """  var b0=clone(dayOf(V,mid,date)),d=clone(b0);fn(d,V);
  if(!d.certAt)delete d.certAt;if(!d.in)delete d.in;if(!d.focus)delete d.focus;
  savePatch('days/'+mid+'_'+date,b0,d);""")
sub("""  var p=clone(obj(V.progress[V.me]));p.checks=obj(p.checks);p.skip=obj(p.skip);p.solved=obj(p.solved);
  fn(p);save('progress/'+V.me,p);""", """  var b0=clone(obj(V.progress[V.me])),p=clone(b0);p.checks=obj(p.checks);p.skip=obj(p.skip);p.solved=obj(p.solved);
  fn(p);savePatch('progress/'+V.me,b0,p);""")
sub("  var s=clone(obj(V.subjects[sid]));s.items=arr(s.items);fn(s);save('subjects/'+sid,s);",
    "  var b0=clone(obj(V.subjects[sid])),s=clone(b0);s.items=arr(s.items);fn(s);savePatch('subjects/'+sid,b0,s);")
# 저절로 쓰는 일은 새 기록을 다 받은 뒤에
sub("  if(HUM_DONE)return;var V=view();\n  if(!S.ready||", "  if(HUM_DONE||!netFresh())return;var V=view();\n  if(!S.ready||")
sub("  if(CERT_MIG)return;var V=view();\n  if(!S.ready||", "  if(CERT_MIG||!netFresh())return;var V=view();\n  if(!S.ready||")
# 시험용 손잡이: 이 기기에 gbb_test=1 이 있을 때만
assert s.count("\ninit();\n") == 1
s = s.replace("\ninit();\n", "\ntry{if(localStorage.getItem('gbb_test')==='1')window.__gbb={S:S,view:view,editProg:editProg,editDay:editDay,jdiff:jdiff,opsMerge:opsMerge,unitsOf:unitsOf,dayOf:dayOf,today:today,netFresh:netFresh};}catch(e){}\ninit();\n")
