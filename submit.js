/* MWSubmit: shared Submit button. Usage (Submit works at any point in a deck; sends answers so far, lists unanswered ids so they come back next deck):
   MWSubmit.button(el,{agent,app,deck,getResults:()=>obj,getNotes:()=>str})
   POSTs text/plain JSON (no-cors) to the shared Apps Script receiver. No token in client code. */
(function(w){
  var URL='https://script.google.com/macros/s/AKfycbwoYorVuS4ZQdlmPM0CAYQ5qOoeuR4GjMk5Myg7rLpurHxt_6iqyZgJgYaxuZqoQdv7/exec';
  var QK='mw-submit-queue',DB='https://webermanapps.github.io/branding-djqmb410/decks/';
  var CSS='.mws-wrap{display:flex;flex-direction:column;align-items:stretch;gap:.5rem;margin:1rem 0;max-width:28rem}'+
  '.mws-btn{font-family:Khand,Hind,system-ui,sans-serif;font-weight:700;font-size:1.25rem;letter-spacing:.12em;text-transform:uppercase;min-height:56px;min-width:44px;padding:.9rem 2rem;border:2px solid #171717;border-radius:0;background:#171717;color:#FAFAFA;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:.6rem;touch-action:manipulation;-webkit-tap-highlight-color:transparent;-webkit-appearance:none;appearance:none}'+
  '.mws-btn[disabled]{opacity:.7;cursor:default}.mws-btn.sent{background:#FFFFFF;color:#0A0A0A}.mws-btn.fail{background:#FFFFFF;color:#0A0A0A;border-style:dashed}'+
  '.mws-done{display:none;margin:.5rem 0 0;padding:1rem;border:2px solid #0B6E4F;background:#F2F8F5;font-family:Hind,system-ui,sans-serif}.mws-done.on{display:block}.mws-done p{margin:0 0 .75rem;font-size:1rem;color:#0A0A0A}'+
  '.mws-back{display:flex;align-items:center;justify-content:center;min-height:64px;padding:1rem 1.5rem;background:#0B6E4F;color:#fff;font-family:Khand,Hind,system-ui,sans-serif;font-weight:700;font-size:1.4rem;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;touch-action:manipulation}'+
  '.mws-msg{font-family:Hind,system-ui,sans-serif;font-size:.95rem;color:#737373;min-height:1.2em}'+
  '.mw-hover{transition:transform 180ms ease-out,box-shadow 180ms ease-out}.mw-hover:hover,.mw-hover:focus-visible{transform:translateY(-1px) scale(1.02);box-shadow:0 6px 18px rgba(10,10,10,.12)}'+
  '@media(hover:none){.mw-hover:hover{transform:none;box-shadow:none}}@media(prefers-reduced-motion:reduce){.mw-hover{transition:none}.mw-hover:hover{transform:none}}';
  var CHECK='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  function css(){if(document.getElementById('mws-css'))return;var s=document.createElement('style');s.id='mws-css';s.textContent=CSS;document.head.appendChild(s);}
  function q(){try{return JSON.parse(localStorage.getItem(QK)||'[]')}catch(_){return[]}}
  function setQ(a){try{localStorage.setItem(QK,JSON.stringify(a))}catch(_){}}
  function post(p){return fetch(URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(p)});}
  function flush(){var a=q();if(!a.length)return Promise.resolve(0);setQ([]);var left=[];
    return Promise.all(a.map(function(p){return post(p).catch(function(){left.push(p)})})).then(function(){if(left.length)setQ(q().concat(left));return a.length-left.length;});}
  function scan(){var a=[],u=[];document.querySelectorAll('.dk-card[data-id]').forEach(function(c){(c.querySelector('.dk-v.on,.dk-opt.on')?a:u).push(c.dataset.id)});return {answered:a,unanswered:u};}
  function button(el,o){css();o=o||{};var back=o.backUrl||DB;
    var wrap=document.createElement('div');wrap.className='mws-wrap';
    var b=document.createElement('button');b.type='button';b.className='mws-btn mw-hover';
    var m=document.createElement('div');m.className='mws-msg';m.setAttribute('role','status');m.setAttribute('aria-live','polite');
    var dn=document.createElement('div');dn.className='mws-done';dn.setAttribute('role','status');
    dn.innerHTML='<p class="mws-dt"></p><a class="mws-back mw-hover" href="'+back+'">Back to Deck Building</a>';
    wrap.appendChild(b);wrap.appendChild(m);wrap.appendChild(dn);el.appendChild(wrap);
    function state(s){b.classList.remove('sent','fail');b.disabled=false;
      if(s==='idle'){b.textContent='Submit';m.textContent='';}
      if(s==='sending'){b.textContent='Sending';b.disabled=true;m.textContent='';}
      dn.classList.toggle('on',s==='sent');
      if(s==='sent'){b.innerHTML=CHECK+'<span>Sent</span>';b.classList.add('sent');m.textContent='Sent. Tap again to send an update.';var k=scan();dn.firstChild.textContent='Sent '+k.answered.length+' answer'+(k.answered.length==1?'':'s')+'.'+(k.unanswered.length?' '+k.unanswered.length+' unanswered card'+(k.unanswered.length==1?'':'s')+' come back in the next deck.':'');}
      if(s==='fail'){b.textContent='Not Sent Yet';b.classList.add('fail');m.textContent='Saved on this device. Tap to retry; it also retries when you reopen.';}}
    b.addEventListener('click',function(){if(b.disabled)return;state('sending');
      var k=scan();try{localStorage.setItem('mw-carry-'+o.agent+'-'+o.deck,JSON.stringify(k.unanswered))}catch(_){}
      var p={answered:k.answered,unanswered:k.unanswered,partial:k.unanswered.length>0,agent:o.agent,app:o.app,deck:o.deck,results:o.getResults?o.getResults():null,notes:o.getNotes?o.getNotes():'',sentAt:new Date().toISOString(),ua:navigator.userAgent};
      post(p).then(function(){state('sent')},function(){setQ(q().concat([p]));state('fail')});});
    state(q().some(function(p){return p.agent===o.agent&&p.deck===o.deck})?'fail':'idle');
    flush().then(function(n){if(n&&!q().some(function(p){return p.agent===o.agent&&p.deck===o.deck}))state('sent')});
    return {el:wrap,state:state};}
  w.MWSubmit={button:button,flush:flush,url:URL};
  w.addEventListener('online',flush);
})(window);
