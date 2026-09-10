/* LionRose · green digital theme (shared behaviour) */
(function(){
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var GLYPHS='01<>/{}=;:+*[]#$_%|ABCDEF0123456789'.split('');
  function rg(){return GLYPHS[(Math.random()*GLYPHS.length)|0];}

  /* scroll reveals */
  var rev=document.querySelectorAll('.reveal');
  if(reduce||!('IntersectionObserver'in window)){rev.forEach(function(e){e.classList.add('in');});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}});},{threshold:0.1});rev.forEach(function(e){io.observe(e);});}

  /* decode-on-hover for .dc */
  document.querySelectorAll('.dc').forEach(function(el){
    var target=(el.textContent||'').replace(/\s+/g,' ').trim(); if(!target)return; el.setAttribute('data-text',target);
    var iv=null;
    function run(){ if(reduce)return; clearInterval(iv); var start=performance.now(),dur=460;
      iv=setInterval(function(){ var p=Math.min(1,(performance.now()-start)/dur),reveal=Math.floor(p*target.length),out='';
        for(var i=0;i<target.length;i++){var ch=target[i];out+=(ch===' '||i<reveal)?ch:rg();}
        el.textContent=out; if(p>=1){clearInterval(iv);el.textContent=target;} },26); }
    el.addEventListener('mouseenter',run);
    el.addEventListener('mouseleave',function(){clearInterval(iv);el.textContent=target;});
  });

  /* client logos: upgrade text -> logo image if it loads, else keep decode wordmark */
  document.querySelectorAll('.client[data-domain]').forEach(function(el){
    var dom=el.getAttribute('data-domain'), name=(el.textContent||'').trim();
    var img=new Image();
    img.onload=function(){ if(img.naturalWidth<8)return; el.textContent=''; img.alt=name; el.appendChild(img); };
    img.onerror=function(){/* keep wordmark */};
    img.src='https://logo.clearbit.com/'+dom;
  });

  /* decode hero canvas (any .hero canvas). data-words = comma list, else default services */
  document.querySelectorAll('.hero canvas').forEach(function(c){
    var ctx=c.getContext('2d');
    var W,H,dpr,coreX,charW,FONT=16,GREEN='51,255,156';
    var words=(c.getAttribute('data-words')||'AI SOLUTIONS,WEB DEVELOPMENT,HUMAN RESOURCES,MEDIA CONSULTING,PRODUCTION').split(',').map(function(s){return s.trim();});
    var speed=1.5, glow=1.5, density=1.35;
    var pts,lanes=[],last=performance.now(),running=false;
    function buildMesh(){var n=Math.round((W*H)/24000*density);pts=[];for(var i=0;i<n;i++)pts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-0.5)*9,vy:(Math.random()-0.5)*9});}
    function drawMesh(dt){
      for(var i=0;i<pts.length;i++){var p=pts[i];p.x+=p.vx*dt*speed;p.y+=p.vy*dt*speed;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;}
      for(var i=0;i<pts.length;i++){for(var j=i+1;j<pts.length;j++){var a=pts[i],b=pts[j],dx=a.x-b.x,dy=a.y-b.y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<125){var cf=1-Math.min(1,Math.abs(((a.x+b.x)/2)-coreX)/(W*0.28));var al=(1-d/125)*(0.10+cf*0.30);
          ctx.strokeStyle='rgba('+GREEN+','+al.toFixed(3)+')';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();}}}
      ctx.fillStyle='rgba('+GREEN+',0.8)';ctx.shadowColor='rgba('+GREEN+',0.7)';ctx.shadowBlur=7*glow;
      for(var i=0;i<pts.length;i++){ctx.beginPath();ctx.arc(pts[i].x,pts[i].y,1.6,0,6.28);ctx.fill();}ctx.shadowBlur=0;
    }
    function drawBeam(){var g=ctx.createLinearGradient(coreX-90,0,coreX+90,0);g.addColorStop(0,'rgba('+GREEN+',0)');g.addColorStop(0.5,'rgba('+GREEN+','+(0.05*glow)+')');g.addColorStop(1,'rgba('+GREEN+',0)');ctx.fillStyle=g;ctx.fillRect(coreX-90,0,180,H);ctx.fillStyle='rgba('+GREEN+','+(0.16*glow)+')';ctx.fillRect(coreX-0.5,H*0.30,1.5,H*0.44);}
    function newPacket(y,startX){var word=words[(Math.random()*words.length)|0],len=word.length,x=(startX!==undefined)?startX:-(len*charW)-40-Math.random()*W*0.25,scr=[];for(var i=0;i<len;i++)scr.push(rg());return{y:y,word:word,len:len,x:x,scr:scr,spd:40+Math.random()*22,seedT:0};}
    function buildLanes(){lanes=[];var top=H*0.42,bot=H*0.78,n=6;for(var i=0;i<n;i++){var y=top+(bot-top)*(i/(n-1));lanes.push(newPacket(y,Math.random()*W));}}
    function drawLanes(dt){
      ctx.font='700 '+FONT+'px '+"'JetBrains Mono',monospace";ctx.textBaseline='middle';
      for(var L=0;L<lanes.length;L++){var p=lanes[L];p.x+=p.spd*speed*dt;
        if(p.x>W+20){lanes[L]=newPacket(p.y);continue;}
        p.seedT+=dt;var reseed=p.seedT>0.05;if(reseed)p.seedT=0;
        for(var i=0;i<p.len;i++){var xi=p.x+i*charW;if(xi<-charW||xi>W+charW)continue;var ch;
          if(xi>=coreX){ch=p.word[i];if(ch===' ')continue;var a=xi>W*0.82?Math.max(0,1-(xi-W*0.82)/(W*0.18)):1;
            ctx.fillStyle='rgba(234,255,245,'+a+')';ctx.shadowColor='rgba('+GREEN+','+(0.55*glow*a)+')';ctx.shadowBlur=10*glow;ctx.fillText(ch,xi,p.y);ctx.shadowBlur=0;}
          else{var dist=coreX-xi;if(reseed){p.scr[i]=(dist<40&&Math.random()<0.85)?rg():(Math.random()<0.12?rg():p.scr[i]);}ch=p.scr[i];
            var near=dist<70?(1-dist/70):0,a2=0.34+near*0.5;ctx.fillStyle='rgba('+GREEN+','+a2.toFixed(3)+')';
            if(near>0.4){ctx.shadowColor='rgba('+GREEN+','+(0.4*glow)+')';ctx.shadowBlur=8*glow;}ctx.fillText(ch,xi,p.y);ctx.shadowBlur=0;}}}
    }
    function size(){dpr=Math.min(window.devicePixelRatio||1,2);W=c.clientWidth;H=c.clientHeight;c.width=W*dpr;c.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);coreX=W*0.5;ctx.font='700 '+FONT+'px '+"'JetBrains Mono',monospace";charW=ctx.measureText('M').width||9.6;buildMesh();buildLanes();}
    function frame(now){var dt=Math.min(0.05,(now-last)/1000);last=now;ctx.fillStyle='rgba(6,10,8,0.30)';ctx.fillRect(0,0,W,H);drawBeam();drawMesh(dt);drawLanes(dt);if(running)requestAnimationFrame(frame);}
    function play(){if(running||reduce)return;running=true;last=performance.now();requestAnimationFrame(frame);}
    function stop(){running=false;}
    function start(){size();window.addEventListener('resize',size);
      if(reduce){ctx.fillStyle='#060a08';ctx.fillRect(0,0,W,H);drawBeam();drawMesh(0.016);drawLanes(0.016);return;}
      var host=c.closest('.hero')||c;
      if('IntersectionObserver'in window){var ho=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?play():stop();});},{threshold:0.02});ho.observe(host);}
      play();
    }
    if(document.fonts&&document.fonts.ready){document.fonts.ready.then(start);setTimeout(function(){if(!W)start();},400);}else start();
  });
})();
