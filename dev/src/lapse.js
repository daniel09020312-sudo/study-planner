/* ---------- 게시판: 공부 타임랩스 ---------- */
// 영상 파일에서 장면을 고르게 뽑아 작은 사진 묶음으로 줄여 저장하고, 넘겨 보기로 재생한다.
// 저장: quiz/<id> = {kind:'lapse', q, sid, pic:true, vid:{n,c,fps,w,h,src}}, 첫 장면 pics/<id>, 장면 묶음 pics/<id>_c0..
var LAPSE_N=48,LAPSE_FPS=8,LAPSE_LONG=432,LAPSE_CHUNK=8;
S.lapse={};S.lup=null;
function isImgData(x){return typeof x==='string'&&x.indexOf('data:image/')===0;}
function lapseFrames(file,onProg){
  return new Promise(function(res,rej){
    var url=URL.createObjectURL(file),v=document.createElement('video'),done=false,cv=document.createElement('canvas'),cx=cv.getContext('2d'),out=[],q=.58,n=LAPSE_N,dur=0,W=0,H=0;
    v.muted=true;v.playsInline=true;v.setAttribute('playsinline','');v.setAttribute('muted','');v.preload='auto';
    function fin(err){if(done)return;done=true;try{URL.revokeObjectURL(url);}catch(e){}v.removeAttribute('src');try{v.load();}catch(e){}if(err)rej(err);else res({frames:out,w:W,h:H,dur:dur});}
    function waitEv(name,ms){return new Promise(function(ok,no){var t=setTimeout(function(){v.removeEventListener(name,h);no(new Error('timeout'));},ms);function h(){clearTimeout(t);v.removeEventListener(name,h);ok();}v.addEventListener(name,h);});}
    v.addEventListener('error',function(){fin(new Error('decode'));});
    v.src=url;
    waitEv('loadedmetadata',20000).then(function(){
      dur=v.duration;if(!isFinite(dur)||dur<=0)throw new Error('duration');
      var vw=v.videoWidth||0,vh=v.videoHeight||0;if(!vw||!vh)throw new Error('size');
      var sc=Math.min(1,LAPSE_LONG/Math.max(vw,vh));W=Math.max(2,Math.round(vw*sc/2)*2);H=Math.max(2,Math.round(vh*sc/2)*2);cv.width=W;cv.height=H;
      n=dur<6?Math.max(8,Math.min(LAPSE_N,Math.round(dur*8))):LAPSE_N;
      var p=Promise.resolve();try{var pl=v.play();if(pl&&pl.then)p=pl.then(function(){v.pause();}).catch(function(){});}catch(e){}
      return p;
    }).then(function(){
      var i=0;
      function step(){
        if(done)return;
        if(i>=n){fin();return;}
        var t=Math.min(Math.max(0,dur-0.05),dur*(i+0.5)/n);
        var w=waitEv('seeked',10000);v.currentTime=t;
        return w.then(function(){
          cx.drawImage(v,0,0,W,H);
          var d=cv.toDataURL('image/jpeg',q);
          if(i===0&&d.length>36000){q=Math.max(.36,q-.14);d=cv.toDataURL('image/jpeg',q);}
          out.push(d);i++;if(onProg)onProg(i,n);
          return step();
        });
      }
      return step();
    }).catch(function(e){fin(e||new Error('fail'));});
  });
}
function lapsePick(){
  var fi=document.getElementById('lapsePick');
  if(!fi){
    fi=document.createElement('input');fi.type='file';fi.id='lapsePick';fi.accept='video/*';fi.style.display='none';document.body.appendChild(fi);
    fi.addEventListener('change',function(){
      var f=fi.files&&fi.files[0];fi.value='';if(!f||!S.lup)return;
      lapseStop('_new');S.lup={frames:[],w:0,h:0,dur:0,busy:false,prep:true,got:0,n:LAPSE_N,err:'',up:0,upn:0};render();
      lapseFrames(f,function(i,n){if(!S.lup)return;S.lup.got=i;S.lup.n=n;var e=document.getElementById('lupProg');if(e)e.textContent='장면 고르는 중 '+i+' / '+n;var b=document.getElementById('lupBar');if(b)b.style.width=Math.round(i/n*100)+'%';})
        .then(function(r){if(!S.lup)return;S.lup.prep=false;S.lup.frames=r.frames;S.lup.w=r.w;S.lup.h=r.h;S.lup.dur=r.dur;S.lapse._new={frames:r.frames,i:0,on:false,fps:LAPSE_FPS};render();setTimeout(function(){lapsePlay('_new');},60);})
        .catch(function(){if(!S.lup)return;S.lup.prep=false;S.lup.err='이 영상을 열지 못했습니다. 휴대폰 사진 앱에 있는 영상(mp4, mov)을 골라 주세요. 컴퓨터에서 안 되면 휴대폰에서 올려 보세요.';render();});
    });
  }
  fi.click();
}
function lapseStop(id){var P=S.lapse[id];if(P){P.on=false;clearInterval(P.t);P.t=null;}}
function lapsePlay(id){
  var P=S.lapse[id];if(!P||!P.frames||!P.frames.length)return;
  Object.keys(S.lapse).forEach(function(k){if(k!==id)lapseStop(k);});
  clearInterval(P.t);P.on=true;
  P.t=setInterval(function(){
    var img=document.getElementById('lpi-'+id);
    if(!img||!P.on){lapseStop(id);var bt=document.getElementById('lpo-'+id);if(bt)bt.classList.remove('on');return;}
    P.i=(P.i+1)%P.frames.length;img.src=P.frames[P.i];
    var bar=document.getElementById('lpb-'+id);if(bar)bar.style.width=((P.i+1)/P.frames.length*100).toFixed(1)+'%';
  },Math.round(1000/(P.fps||LAPSE_FPS)));
  var bt=document.getElementById('lpo-'+id);if(bt)bt.classList.add('on');
}
function lapseLoad(id){
  var V=view(),q=V.quiz[id],c=+obj(obj(q).vid).c||0;if(!q||!c||!S.net||!S.net.read)return;
  var P=S.lapse[id]||(S.lapse[id]={frames:null,i:0,on:false,fps:+obj(q.vid).fps||LAPSE_FPS});
  if(P.frames||P.loading)return;
  P.loading=true;P.got=0;P.err=false;var parts=[];render();
  var jobs=[];
  for(var k=0;k<c;k++)(function(k){jobs.push(S.net.read('pics/'+id+'_c'+k).then(function(d){parts[k]=arr(obj(d).frames).filter(isImgData);P.got++;var e=document.getElementById('lpl-'+id);if(e)e.textContent='불러오는 중 '+Math.round(P.got/c*100)+'%';}));})(k);
  Promise.all(jobs).then(function(){P.loading=false;P.frames=[].concat.apply([],parts);if(!P.frames.length){P.frames=null;P.err=true;render();return;}render();lapsePlay(id);})
    .catch(function(){P.loading=false;P.err=true;render();});
}
function lapseBox(q){
  var id=q.id,P=S.lapse[id],vd=obj(q.vid),poster=S.pics[id],src=P&&P.frames?P.frames[P.i||0]:(isImgData(poster)?poster:'');
  var ar=(+vd.w&&+vd.h)?(+vd.w)+' / '+(+vd.h):'9 / 16',n=+vd.n||0,secs=n?Math.round(n/(+vd.fps||LAPSE_FPS)):0;
  var lab=P&&P.loading?'<span class="lpl" id="lpl-'+esc(id)+'">불러오는 중</span>':P&&P.err?'<span class="lpl">불러오지 못했습니다. 다시 누르세요.</span>':'';
  return '<div class="lapse"><button class="lpv" data-act="lapse-tap" data-id="'+esc(id)+'" style="aspect-ratio:'+ar+'" aria-label="타임랩스 '+(P&&P.on?'멈추기':'재생')+'">'+(src?'<img id="lpi-'+esc(id)+'" src="'+esc(src)+'" alt="공부 타임랩스">':'<span class="lpph" id="lpi-'+esc(id)+'"></span>')+'<span class="lpo'+(P&&P.on?' on':'')+'" id="lpo-'+esc(id)+'" aria-hidden="true"><i></i></span>'+lab+'</button><div class="lpbar" aria-hidden="true"><i id="lpb-'+esc(id)+'" style="width:'+(P&&P.frames?((P.i+1)/P.frames.length*100).toFixed(1):0)+'%"></i></div>'+(secs?'<small class="lpmeta">'+n+'장면, '+secs+'초</small>':'')+'</div>';
}
function modalLapse(V){
  var U=S.lup||{},b='';
  if(U.prep){
    b+='<div class="lupwait"><p id="lupProg">장면 고르는 중 '+(U.got||0)+' / '+(U.n||LAPSE_N)+'</p><div class="lpbar"><i id="lupBar" style="width:'+Math.round((U.got||0)/(U.n||LAPSE_N)*100)+'%"></i></div><p class="hint" style="margin-top:8px">영상 길이에 따라 몇십 초 걸릴 수 있습니다. 화면을 켜 두세요.</p></div>';
  }else if(U.frames&&U.frames.length){
    var P=S.lapse._new||{};
    b+='<div class="lapse new"><button class="lpv" data-act="lapse-tap" data-id="_new" style="aspect-ratio:'+U.w+' / '+U.h+'" aria-label="미리보기 재생"><img id="lpi-_new" src="'+esc(U.frames[P.i||0])+'" alt="타임랩스 미리보기"><span class="lpo'+(P.on?' on':'')+'" id="lpo-_new" aria-hidden="true"><i></i></span></button><div class="lpbar" aria-hidden="true"><i id="lpb-_new" style="width:0%"></i></div><small class="lpmeta">'+U.frames.length+'장면, '+Math.round(U.frames.length/LAPSE_FPS)+'초로 줄였습니다'+(U.dur?' (원래 '+Math.round(U.dur)+'초)':'')+'</small></div>';
    b+='<div class="row" style="margin-top:8px"><button class="btn small" data-act="lapse-pick"'+(U.busy?' disabled':'')+'>다른 영상 고르기</button></div>';
    b+='<div class="fld"><h3>과목<small>선택</small></h3><div class="chips">'+mySubs(V).map(function(s){return chipBtn('lapse-sid','sid',s.id,s.name,U.sid===s.id);}).join('')+'</div></div>';
    b+='<div class="fld"><h3>한마디<small>선택</small></h3><input type="text" data-draft="lapseCap" data-enter="lapse-up" maxlength="80" placeholder="예: 미적분 3시간, 기출 2회" aria-label="한마디"></div>';
  }else{
    b+='<p class="hint">휴대폰 카메라의 타임랩스로 공부하는 모습을 찍은 영상을 고르세요. 올릴 때 소리를 빼고 '+LAPSE_N+'장면(약 '+Math.round(LAPSE_N/LAPSE_FPS)+'초)으로 줄여서 저장합니다.</p>';
    b+='<div class="row" style="margin-top:12px"><button class="btn primary" data-act="lapse-pick">영상 고르기</button></div>';
  }
  if(U.err)b+='<p class="hint serr" role="status" style="margin-top:10px">'+esc(U.err)+'</p>';
  var foot='';
  if(U.frames&&U.frames.length&&!U.prep)foot='<span class="hint">'+(U.busy?'올리는 중 '+U.up+' / '+U.upn:'모두에게 보입니다.')+'</span><div class="df"><button class="btn primary" data-act="lapse-up"'+(U.busy?' disabled':'')+'>'+(U.busy?'올리는 중':'올리기')+'</button></div>';
  return dlg('wide',{id:'lapse',t:'타임랩스 올리기'},b,foot);
}
function lapseUpload(){
  var U=S.lup,V=view();if(!U||!U.frames||!U.frames.length||U.busy||!V.me||!need())return;
  var qid=rid('q'),fr=U.frames,chunks=[],i;
  for(i=0;i<fr.length;i+=LAPSE_CHUNK)chunks.push(fr.slice(i,i+LAPSE_CHUNK));
  U.busy=true;U.up=0;U.upn=chunks.length+1;U.err='';render();
  var k=0;
  function next(){
    if(k>=chunks.length)return Promise.resolve();
    var c=k++;
    return S.net.write('pics/'+qid+'_c'+c,{frames:chunks[c]}).then(function(){U.up++;render();return next();});
  }
  putPic(qid,fr[0]).then(function(){U.up++;render();return next();}).then(function(){
    save('quiz/'+qid,{kind:'lapse',mid:V.me,sid:U.sid||'',q:String(S.draft.lapseCap||'').trim().slice(0,80),a:'',at:Date.now(),pic:true,vid:{n:fr.length,c:chunks.length,fps:LAPSE_FPS,w:U.w,h:U.h,src:Math.round(U.dur||0)}});
    S.lapse[qid]={frames:fr,i:0,on:false,fps:LAPSE_FPS};
    lapseStop('_new');delete S.lapse._new;S.lup=null;S.draft.lapseCap='';S.filter='all';closeModal();flash('타임랩스를 올렸습니다.');render();
  }).catch(function(){
    U.busy=false;U.err='올리지 못했습니다. 인터넷 연결을 확인하고 다시 올려 주세요.';
    for(var j=0;j<chunks.length;j++)S.net.write('pics/'+qid+'_c'+j,null).catch(function(){});
    S.net.write('pics/'+qid,null).catch(function(){});
    render();
  });
}
