/* 優健堂 UHealthFit × WiseQuest — 全站互動 */
(function(){
  // 手機選單
  var mb=document.querySelector('.menu-btn'), mm=document.querySelector('.mobile-menu');
  if(mb&&mm){mb.addEventListener('click',function(){var o=mm.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false');});}

  // 外站購買連結：加上 UTM、記錄事件（GA4 / Meta Pixel 若存在）
  var page=document.body.getAttribute('data-page')||'site';
  document.querySelectorAll('a[href^="https://zh.uhealthfit.com"]').forEach(function(a){
    try{
      var u=new URL(a.href);
      if(!u.searchParams.get('utm_source')){
        u.searchParams.set('utm_source','uhealthfit-site');
        u.searchParams.set('utm_medium','referral');
        u.searchParams.set('utm_campaign',page);
        a.href=u.toString();
      }
      a.setAttribute('rel','noopener'); a.setAttribute('target','_blank'); // 另開新分頁，保留本站
      a.addEventListener('click',function(){
        var label=a.getAttribute('data-product')||page;
        if(window.gtag){gtag('event','begin_checkout_redirect',{product:label,page:page});}
        if(window.fbq){fbq('trackCustom','ShopRedirect',{product:label,page:page});}
      });
    }catch(e){}
  });

  // 產品頁固定購買列：捲過主購買區後顯示
  var bar=document.querySelector('.buybar'), anchor=document.querySelector('.buybox');
  if(bar&&anchor&&'IntersectionObserver' in window){
    document.body.classList.add('has-buybar');
    new IntersectionObserver(function(es){es.forEach(function(e){bar.classList.toggle('show',!e.isIntersecting&&e.boundingClientRect.top<0);});},{threshold:0}).observe(anchor);
  }

  // 部落格篩選
  var chips=document.querySelectorAll('.chip[data-f]');
  if(chips.length){
    chips.forEach(function(c){c.addEventListener('click',function(){
      chips.forEach(function(x){x.classList.remove('on');});c.classList.add('on');
      var f=c.getAttribute('data-f');
      document.querySelectorAll('.post-card[data-series]').forEach(function(p){p.style.display=(f==='all'||p.getAttribute('data-series')===f)?'':'none';});
    });});
  }

  // 測驗
  var quiz=document.getElementById('quiz');
  if(quiz){
    var steps=[].slice.call(quiz.querySelectorAll('.qstep')), i=0, score={eye:0,dental:0,sleep:0,digestive:0,skin:0,vitality:0}, answers=[];
    var prog=quiz.querySelector('.qprog i'), result=quiz.querySelector('.qresult'), back=quiz.querySelector('.qback');
    function show(n){steps.forEach(function(s,k){s.classList.toggle('on',k===n);});prog.style.width=((n)/steps.length*100)+'%';if(back)back.style.visibility=n>0?'visible':'hidden';}
    quiz.querySelectorAll('.qopts button').forEach(function(b){b.addEventListener('click',function(){
      var w=JSON.parse(b.getAttribute('data-w')||'{}');answers[i]=w;
      i++; if(i<steps.length){show(i);} else {finish();}
    });});
    if(back){back.addEventListener('click',function(){if(i>0){i--;answers.length=i;show(i);}});}
    function finish(){
      Object.keys(score).forEach(function(k){score[k]=0;});
      answers.forEach(function(w){Object.keys(w).forEach(function(k){score[k]+=w[k];});});
      var ranked=Object.keys(score).sort(function(a,b){return score[b]-score[a];});
      var top=ranked[0], second=ranked[1];
      steps.forEach(function(s){s.classList.remove('on');});prog.style.width='100%';
      result.querySelectorAll('[data-r]').forEach(function(el){el.style.display=el.getAttribute('data-r')===top?'':'none';});
      result.querySelectorAll('[data-r2]').forEach(function(el){el.style.display=el.getAttribute('data-r2')===second?'':'none';});
      var hid=result.querySelector('input[name="quiz_result"]'); if(hid){hid.value=top+'|'+second;}
      result.classList.add('on'); if(back)back.style.visibility='hidden';
      result.scrollIntoView({behavior:'smooth',block:'start'});
      if(window.gtag){gtag('event','quiz_complete',{result:top});}
    }
    show(0);
  }

  // Klaviyo 名單訂閱（client API，公開金鑰）
  var form=document.querySelector('form[data-klaviyo-list]');
  if(form){
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var email=form.querySelector('input[type=email]').value.trim(); if(!email) return;
      var company=form.getAttribute('data-klaviyo-company'), list=form.getAttribute('data-klaviyo-list');
      var props={source:'uhealthfit-site/'+page}; var r=form.querySelector('input[name="quiz_result"]'); if(r&&r.value){props.quiz_result=r.value;}
      var body={data:{type:'subscription',attributes:{custom_source:'uhealthfit-site '+page,profile:{data:{type:'profile',attributes:{email:email,properties:props}}}},relationships:{list:{data:{type:'list',id:list}}}}};
      var btn=form.querySelector('button'); btn.disabled=true;
      fetch('https://a.klaviyo.com/client/subscriptions/?company_id='+encodeURIComponent(company),{method:'POST',headers:{'Content-Type':'application/json','revision':'2024-10-15'},body:JSON.stringify(body)})
      .then(function(res){ if(res.status===202||res.ok){done();} else {throw new Error('status '+res.status);} })
      .catch(function(){ btn.disabled=false; toast('暫時無法送出，請稍後再試，或來信 service@uhealthfit.com'); });
      function done(){form.style.display='none';var ok=form.parentNode.querySelector('.email-ok');if(ok){ok.style.display='block';}if(window.gtag){gtag('event','generate_lead',{method:'quiz_email'});}}
    });
  }
  function toast(msg){var t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';document.body.appendChild(t);}t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},3200);}
})();
