/* R104 Back helper: return to wherever the user came from.
   Order: history.back() if history.length>1, else same-origin document.referrer,
   else same-origin ?from= param, else the link's own href (fixed fallback).
   Usage: <a href="FALLBACK" onclick="return window.mwBack?mwBack(event,this.href):true">. */
(function(){
  function same(u){try{var x=new URL(u,location.href);return (x.protocol==='https:'||x.protocol==='http:')&&x.origin===location.origin?x.href:null}catch(_){return null}}
  function target(fallback){
    if(history.length>1)return {back:true};
    var r=document.referrer&&same(document.referrer);
    if(r&&r!==location.href)return {url:r};
    var f=null;try{f=new URLSearchParams(location.search).get('from')}catch(_){}
    f=f&&same(f);if(f&&f!==location.href)return {url:f};
    return {url:fallback};
  }
  window.mwBackTarget=target;
  window.mwBack=function(ev,fallback){
    if(ev&&(ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.altKey||(ev.button&&ev.button!==0)))return true;
    var t=target(fallback);
    if(ev&&ev.preventDefault)ev.preventDefault();
    if(t.back)history.back();else location.href=t.url;
    return false;
  };
})();
