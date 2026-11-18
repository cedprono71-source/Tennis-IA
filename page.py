PAGE = r"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>TENNIS-IA</title>
<meta name="theme-color" content="#050B1E">
<link href="https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,600;0,800;1,900&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{--l:#A6FF1F;--bg:#050B1E;--c:#0E1B3A;--bd:#1F3566;--t:#fff;--m:#9FB0D0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--t);font-family:Inter,system-ui,sans-serif;padding-bottom:84px;-webkit-tap-highlight-color:transparent}
.hero{height:200px;position:relative;overflow:hidden;background:radial-gradient(circle at 15% 20%,#1d4fd8 0,transparent 45%),radial-gradient(circle at 85% 10%,#1e3a8a 0,transparent 50%),linear-gradient(#060f2e,#050B1E)}
.hero:before{content:"";position:absolute;left:-20%;top:60px;width:140%;height:6px;background:linear-gradient(90deg,transparent,var(--l),transparent);transform:rotate(-12deg);filter:blur(2px);box-shadow:0 0 30px var(--l)}
.hero svg{position:absolute}.ball{left:8%;top:22px}.rk{right:2%;top:6px}
.hero h1{position:absolute;left:0;right:0;top:62px;text-align:center;margin:0;font:italic 900 52px/1 "Exo 2",Inter,sans-serif;text-shadow:0 4px 18px #000}.hero h1 b{color:var(--l)}
.card{background:linear-gradient(180deg,#112147,#0A1530);border:1.5px solid var(--bd);border-radius:22px}
.kp{margin:-34px 12px 14px;position:relative;display:flex;padding:12px 8px}.kp div{flex:1;padding:0 8px;border-right:1px solid var(--bd);font-size:12px;color:var(--m)}.kp div:last-child{border:0}
.kp b{display:block;font:800 22px "Exo 2";color:var(--t)}.kp b.g{color:var(--l);font-size:17px;white-space:nowrap}
.tabs{display:flex;gap:8px;padding:0 12px}.tab{flex:1;padding:12px 4px;text-align:center;border:1.5px solid var(--bd);border-radius:18px;background:var(--c);font:800 17px "Exo 2";text-transform:uppercase}
.tab.on{background:var(--l);color:#06210a;border-color:var(--l);box-shadow:0 0 22px #a6ff1f88}
.days{display:flex;gap:6px;overflow-x:auto;padding:12px;scrollbar-width:none}.days::-webkit-scrollbar{display:none}
.d{flex:0 0 auto;padding:6px 12px;border-radius:14px;border:1px solid var(--bd);background:var(--c);font-size:12px;color:var(--m);text-align:center}.d b{display:block;font-size:16px;color:var(--t)}.d.on{border-color:var(--l);box-shadow:0 0 12px #a6ff1f66}
main{padding:0 12px}h2{display:flex;align-items:center;font:800 24px "Exo 2";margin:14px 4px 12px}h2:before{content:"";width:5px;height:30px;background:var(--l);border-radius:3px;margin-right:12px}
.m{position:relative;margin:16px 0 14px;padding:14px 12px 12px}.top{display:flex;align-items:center;justify-content:space-between;font-size:15px;font-weight:600;margin-bottom:10px;padding-right:0}.top span{color:var(--m)}
.pick{position:absolute;right:-4px;top:-18px;background:var(--l);color:#06210a;font:800 15px "Exo 2";padding:8px 14px;border-radius:16px;box-shadow:0 0 22px #a6ff1f99}.tag{background:#2a3a5f;color:#cfd9ee;padding:7px 14px;border-radius:14px;font-size:14px}
.g3{display:grid;grid-template-columns:1fr 1.7fr 1fr;gap:6px;align-items:center}.pl{text-align:center;font:800 17px/1.15 "Exo 2"}.av{width:64px;height:64px;margin:0 auto 8px;border-radius:16px;background:#0b1633;border:1px solid var(--bd);display:flex;align-items:center;justify-content:center;color:#2e4478;font-weight:800}.fl{font-size:24px;margin-top:6px}
.mid{background:#07102a;border-radius:18px;padding:12px 10px}.pc{display:flex}.pc div{flex:1;text-align:center;font:800 34px "Exo 2"}.pc div+div{border-left:1px solid var(--bd)}.pc small{display:block;font:600 15px Inter;color:#dbe5ff}.pc .w{color:var(--l)}
.bar{height:12px;border-radius:8px;background:#22305a;margin-top:10px;position:relative;overflow:hidden}.bar i{position:absolute;top:0;bottom:0;background:var(--l);border-radius:8px;box-shadow:0 0 12px var(--l)}
.res{text-align:center;font-size:13px;color:var(--m);margin-top:8px}.det{display:none;margin-top:12px;font-size:14px;border-top:1px solid var(--bd);padding-top:8px}.m.open .det{display:block}
.det table{width:100%;border-collapse:collapse;margin-top:6px}.det td,.det th{padding:6px;text-align:center;border-bottom:1px solid var(--bd)}.det th{color:var(--m);font-weight:600}.hi{color:var(--l);font-weight:700}
.ban{display:flex;align-items:center;gap:12px;padding:14px;margin:0 0 14px;font-weight:600}.ban small{display:block;color:var(--m);font-weight:500}
.nav{position:fixed;left:0;right:0;bottom:0;display:flex;background:#08122c;border-top:1px solid var(--bd);padding:8px 6px 14px;z-index:9}.nav a{flex:1;text-align:center;font-size:14px;font-weight:700;color:var(--m);padding:6px 0;border-radius:16px;position:relative}.nav a.on{color:var(--l);background:#11260f55;box-shadow:inset 0 2px 0 var(--l)}.nav a span{display:block;font-size:24px}
.bdg{position:absolute;top:0;left:55%;background:#e11d48;color:#fff;border-radius:10px;font-size:12px;min-width:20px;padding:1px 5px}
.mut{color:var(--m);text-align:center;padding:36px 10px;font-size:14px}.kpis{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}.kpis .card{padding:12px}.kpis b{display:block;font:800 28px "Exo 2";color:var(--l)}.kpis span{font-size:12px;color:var(--m)}
.sw{display:flex;justify-content:space-between;align-items:center;padding:16px}.sw input{width:24px;height:24px}
</style></head><body>
<div class="hero"><svg class="ball" width="120" height="120" viewBox="0 0 120 120"><defs><radialGradient id="b" cx="35%" cy="30%"><stop offset="0" stop-color="#e8ff6a"/><stop offset="1" stop-color="#7fc400"/></radialGradient></defs><circle cx="60" cy="60" r="56" fill="url(#b)"/><path d="M12 38C45 55 45 85 14 98M108 22C78 50 82 78 106 94" stroke="#fff" stroke-width="5" fill="none" opacity=".85"/></svg>
<svg class="rk" width="130" height="190" viewBox="0 0 130 190"><g transform="rotate(18 65 95)"><ellipse cx="65" cy="62" rx="40" ry="54" fill="none" stroke="#cfe0ff" stroke-width="5"/><path d="M65 8V116M30 40H100M26 62H104M30 84H100M45 14V110M85 14V110" stroke="#8fb0ff" stroke-width="1.2" opacity=".6"/><rect x="58" y="116" width="14" height="62" rx="6" fill="#6ec800"/></g></svg>
<h1>TENNIS-<b>IA</b></h1></div>
<div class="card kp"><div>Taux de réussite<b id="k1">–</b></div><div>Meilleur pronostic<b class="g" id="k2">–</b></div><div>Matchs du jour<b id="k3">0</b></div></div>
<div class="tabs"><div class="tab on" data-t="atp">ATP</div><div class="tab" data-t="wta">WTA</div><div class="tab" data-t="suivi">Suivi</div></div>
<div class="days" id="days"></div><main id="list"></main>
<div class="nav"><a class="on" data-n="home"><span>🏠</span>Accueil</a><a data-n="stats"><span>📊</span>Stats</a><a data-n="alert"><span>🔔</span>Alertes<i class="bdg" id="bd" hidden>0</i></a><a data-n="set"><span>⚙️</span>Réglages</a></div>
<script>
var J=["dim","lun","mar","mer","jeu","ven","sam"],S={tour:"atp",jour:iso(new Date()),nav:"home"},IOC={ESP:"ES",RUS:"RU",USA:"US",ITA:"IT",FRA:"FR",GER:"DE",GBR:"GB",SRB:"RS",GRE:"GR",NOR:"NO",DEN:"DK",AUS:"AU",CAN:"CA",ARG:"AR",POL:"PL",CZE:"CZ",BUL:"BG",SUI:"CH",AUT:"AT",BEL:"BE",NED:"NL",JPN:"JP",CHN:"CN",BRA:"BR",CHI:"CL",KAZ:"KZ",CRO:"HR",TUN:"TN",SWE:"SE",FIN:"FI",UKR:"UA",HUN:"HU",POR:"PT",ROU:"RO",BLR:"BY",SVK:"SK",SLO:"SI",LAT:"LV",MON:"MC",CZ:"CZ",COL:"CO",MEX:"MX",PER:"PE",TPE:"TW",KOR:"KR",IND:"IN",RSA:"ZA",EGY:"EG",ISR:"IL",TUR:"TR",EST:"EE",LTU:"LT",GEO:"GE",BIH:"BA",IRL:"IE"};
var SF={Hard:"Dur",Clay:"Terre battue",Grass:"Gazon",Carpet:"Moquette"};
function iso(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function pct(x){return Math.round(x*100)+"%"}
function flag(c){var k=IOC[c];return k?String.fromCodePoint.apply(null,k.split("").map(function(ch){return 127397+ch.charCodeAt(0)})):""}
function ini(n){return n.split(" ").map(function(w){return w[0]}).slice(0,2).join("")}
function noHide(){return localStorage.getItem("hideDone")==="1"}
function days(){var b=document.getElementById("days");b.innerHTML="";for(var i=-3;i<=10;i++){var d=new Date();d.setDate(d.getDate()+i);var k=iso(d),e=el("div","d"+(k===S.jour?" on":""));e.appendChild(el("span","",i===0?"auj.":J[d.getDay()]));e.appendChild(el("b","",String(d.getDate())));e.onclick=function(k){return function(){S.jour=k;days();go()}}(k);b.appendChild(e)}}
function api(t,j){return fetch("/api/calendrier?tour="+t+"&date="+j).then(function(r){return r.json()})}
function fav(m){return m.p_a>=0.5?0:1}
function card(m,top){
  var c=el("div","card m"),t=el("div","top");
  t.appendChild(el("div","","🕒 "+(m.heure||"–")));
  var lieu=[m.ville,(SF[m.surface]||"")+(m.indoor===true?" Indoor":m.indoor===false?" Outdoor":"")].filter(function(x){return x&&x.trim()}).join(" • ");
  t.appendChild(el("span","",lieu?"📍 "+lieu:""));c.appendChild(t);
  if(top){c.appendChild(el("div","pick","★ TOP PICK"))}else if(m.tour_tableau){c.appendChild(el("div","pick tag",m.tour_tableau))}
  var g=el("div","g3");
  function pl(n,p){var d=el("div","pl"),a=el("div","av",ini(n));d.appendChild(a);d.appendChild(el("div","",n));d.appendChild(el("div","fl",flag(p)));return d}
  g.appendChild(pl(m.a,m.pays_a));
  var mid=el("div","mid");
  if(m.p_a!=null){var f=fav(m),pc=el("div","pc"),x=el("div",f===0?"w":"",pct(m.p_a)),y=el("div",f===1?"w":"",pct(1-m.p_a));x.appendChild(el("small","","Victoire"));y.appendChild(el("small","","Victoire"));pc.appendChild(x);pc.appendChild(y);mid.appendChild(pc);
    var bar=el("div","bar"),i=el("i");i.style[f===0?"left":"right"]="0";i.style.width=(Math.max(m.p_a,1-m.p_a)*100)+"%";bar.appendChild(i);mid.appendChild(bar)}
  else{mid.appendChild(el("div","res","Pronostic à venir"))}
  g.appendChild(mid);g.appendChild(pl(m.b,m.pays_b));c.appendChild(g);
  if(m.etat==="post"||m.etat==="in"){c.appendChild(el("div","res",(m.etat==="in"?"En cours · ":"")+m.scores[0].join(" ")+" / "+m.scores[1].join(" ")+(m.ok===1?" ✅":m.ok===0?" ❌":"")))}
  var d=el("div","det");c.appendChild(d);var ok=false;
  c.onclick=function(){c.classList.toggle("open");if(!ok){ok=true;detail(d,m)}};
  return c}
function detail(d,m){
  d.appendChild(el("div","res","Calcul en cours…"));
  var u="/match?tour="+m.tour+"&a="+encodeURIComponent(m.a)+"&b="+encodeURIComponent(m.b)+"&surface=auto&best_of=0&tournoi="+encodeURIComponent(m.tournoi||"");
  if(m.lignes&&m.lignes.length)u+="&lignes="+m.lignes.join(",");
  fetch(u).then(function(r){return r.json()}).then(function(r){
    d.innerHTML="";if(r.erreur){d.appendChild(el("div","res",r.erreur));return}
    d.appendChild(el("div","res","Surface : "+r.surface+" · "+r.format+" · Jeux attendus : "+r.jeux_attendus));
    var k=Object.keys(r.over);if(m.lignes)k=m.lignes.map(function(l){return l.toFixed(1)}).filter(function(x){return r.over[x]!==undefined});
    if(k.length){var t=el("table"),h=el("tr");["Jeux","Plus de","Moins de"].forEach(function(x){h.appendChild(el("th","",x))});t.appendChild(h);
      k.forEach(function(x){var q=el("tr");q.appendChild(el("td","",x));q.appendChild(el("td",r.over[x]>.5?"hi":"",pct(r.over[x])));q.appendChild(el("td",r.over[x]<.5?"hi":"",pct(1-r.over[x])));t.appendChild(q)});d.appendChild(t)}
    else d.appendChild(el("div","res","Plus/moins de jeux : non proposé en France pour ce match."))})}
function kpis(ms){document.getElementById("k3").textContent=ms.length;
  var best=null;ms.forEach(function(m){if(m.p_a!=null&&m.etat==="pre"){var c=Math.max(m.p_a,1-m.p_a);if(!best||c>best.c)best={c:c,m:m}}});
  document.getElementById("k2").textContent=best?(best.m[fav(best.m)?"b":"a"].split(" ").pop()+" "+pct(best.c)):"–";return best}
function home(main){
  api(S.tour,S.jour).then(function(d){main.innerHTML="";if(d.erreur){main.appendChild(el("div","mut",d.erreur));return}
    var ms=d.matchs.filter(function(m){return!(noHide()&&m.etat==="post")}),best=kpis(d.matchs);
    if(d.filtre===false)main.appendChild(el("div","mut","Cotes françaises pas encore chargées : tous les matchs sont affichés."));
    if(!ms.length){main.appendChild(el("div","mut",d.filtre?"Aucun match coté en France ce jour-là.":"Aucun match ce jour-là."));return}
    var cur=null,op=null;ms.forEach(function(m){if(m.opp!=null&&m.etat==="pre"&&(!op||m.valeur>op.valeur))op=m});
    ms.forEach(function(m){if(m.tournoi!==cur){cur=m.tournoi;main.appendChild(el("h2","",cur))}main.appendChild(card(m,best&&best.m===m))});
    if(op){var b=el("div","card ban");b.appendChild(el("span","","💡✅"));var x=el("div","","Bonne opportunité sur "+(op.opp?op.b:op.a).split(" ").pop());x.appendChild(el("small","","("+pct(op.opp?1-op.p_a:op.p_a)+" de chances de victoire)"));b.appendChild(x);main.appendChild(b)}
  }).catch(function(){main.innerHTML="";main.appendChild(el("div","mut","Erreur réseau"))})}
function suivi(main){fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){main.innerHTML="";if(d.erreur){main.appendChild(el("div","mut",d.erreur));return}
  var v=d.vainqueur,o=d.over_under,g=el("div","kpis");
  [[d.n?pct(v.reussite):"–","Vainqueur trouvé ("+d.n+")"],[v.forts_n?pct(v.forts_reussite):"–","Favoris ≥65% ("+v.forts_n+")"],[o.n?pct(o.reussite):"–","Plus/moins de jeux ("+o.n+")"],[o.n?o.jeux_prevus+" / "+o.jeux_reels:"–","Jeux prévus / réels"]].forEach(function(a){var c=el("div","card");c.appendChild(el("b","",a[0]));c.appendChild(el("span","",a[1]));g.appendChild(c)});
  main.appendChild(g);if(d.n)document.getElementById("k1").textContent=pct(v.reussite);
  d.derniers.forEach(function(p){var c=el("div","card m");c.appendChild(el("div","top",p.jour.slice(5)+" · "+p.tournoi));c.appendChild(el("div","res",p.a+" "+pct(p.p_a)+" — "+p.b+" "+pct(1-p.p_a)+" → "+(p.ok_vainqueur?"✅":"❌")+(p.ok_over!=null?"  |  "+p.total_jeux+" jeux "+(p.ok_over?"✅":"❌"):"")));main.appendChild(c)})})}
function stats(main){var t=S.tour==="wta"?"wta":"atp";fetch("/top/"+t+"?n=15").then(function(r){return r.json()}).then(function(l){main.innerHTML="";main.appendChild(el("h2","","Classement Elo "+t.toUpperCase()));l.forEach(function(x,i){var c=el("div","card sw");c.appendChild(el("span","",(i+1)+". "+x.joueur));c.appendChild(el("b","hi",String(x.note)));main.appendChild(c)})})}
function alerts(main){Promise.all([api("atp",S.jour),api("wta",S.jour)]).then(function(r){main.innerHTML="";var l=[];r.forEach(function(d){(d.matchs||[]).forEach(function(m){if(m.etat==="pre"&&m.p_a!=null&&(Math.max(m.p_a,1-m.p_a)>=0.65||m.opp!=null))l.push(m)})});
  setBadge(l.length);if(!l.length){main.appendChild(el("div","mut","Aucune alerte pour ce jour."));return}main.appendChild(el("h2","","Alertes du jour"));l.forEach(function(m){main.appendChild(card(m,false))})})}
function setBadge(n){var b=document.getElementById("bd");b.textContent=n;b.hidden=!n}
function reglages(main){main.appendChild(el("h2","","Réglages"));var c=el("div","card sw");c.appendChild(el("span","","Masquer les matchs terminés"));var i=el("input");i.type="checkbox";i.checked=noHide();i.onchange=function(){localStorage.setItem("hideDone",i.checked?"1":"0")};c.appendChild(i);main.appendChild(c)}
function go(){var m=document.getElementById("list");m.innerHTML="";m.appendChild(el("div","mut","Chargement…"));
  if(S.nav==="stats")return stats(m);if(S.nav==="alert")return alerts(m);if(S.nav==="set"){m.innerHTML="";return reglages(m)}
  if(S.tour==="suivi")suivi(m);else home(m)}
document.querySelectorAll(".tab").forEach(function(t){t.onclick=function(){document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("on")});t.classList.add("on");S.tour=t.dataset.t;S.nav="home";nav("home");go()}});
function nav(n){document.querySelectorAll(".nav a").forEach(function(a){a.classList.toggle("on",a.dataset.n===n)})}
document.querySelectorAll(".nav a").forEach(function(a){a.onclick=function(){S.nav=a.dataset.n;nav(S.nav);go()}});
days();go();
Promise.all([api("atp",iso(new Date())),api("wta",iso(new Date()))]).then(function(r){var n=0;r.forEach(function(d){(d.matchs||[]).forEach(function(m){if(m.etat==="pre"&&m.p_a!=null&&(Math.max(m.p_a,1-m.p_a)>=0.65||m.opp!=null))n++})});setBadge(n)}).catch(function(){});
fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){if(d.n)document.getElementById("k1").textContent=pct(d.vainqueur.reussite)}).catch(function(){});
</script></body></html>
"""
