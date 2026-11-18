PAGE = r"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>TENNIS-IA</title>
<meta name="theme-color" content="#050B1E">
<link href="https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,600;0,800;1,900&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{--l:#A6FF1F;--bg:#050B1E;--c:#0E1B3A;--bd:#1F3566;--t:#fff;--m:#9FB0D0}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--t);font-family:Inter,system-ui,sans-serif;-webkit-tap-highlight-color:transparent}
.hero{height:200px;position:relative;overflow:hidden;background:radial-gradient(circle at 15% 20%,#1d4fd8 0,transparent 45%),radial-gradient(circle at 85% 10%,#1e3a8a 0,transparent 50%),linear-gradient(#060f2e,#050B1E)}
.hero:before{content:"";position:absolute;left:-20%;top:60px;width:140%;height:6px;background:linear-gradient(90deg,transparent,var(--l),transparent);transform:rotate(-12deg);filter:blur(2px);box-shadow:0 0 30px var(--l)}
.hero svg{position:absolute}.ball{left:5%;top:20px;filter:drop-shadow(0 0 14px #a6ff1f88)}.rk{right:0;top:-6px;filter:drop-shadow(0 6px 16px #000a)}
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
.mut{color:var(--m);text-align:center;padding:36px 10px;font-size:14px}.kpis{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}.kpis .card{padding:12px}.kpis b{display:block;font:800 28px "Exo 2";color:var(--l)}.kpis span{font-size:12px;color:var(--m)}
.sw{display:flex;justify-content:space-between;align-items:center;padding:16px}.sw input{width:24px;height:24px}
</style></head><body>
<div class="hero"><svg class="ball" width="150" height="150" viewBox="0 0 140 140"><defs>
<radialGradient id="b" cx="36%" cy="30%" r="78%"><stop offset="0" stop-color="#f6ff93"/><stop offset=".45" stop-color="#c8f500"/><stop offset="1" stop-color="#5a9400"/></radialGradient>
<clipPath id="cb"><circle cx="70" cy="70" r="58"/></clipPath><filter id="gl"><feGaussianBlur stdDeviation="7"/></filter></defs>
<circle cx="70" cy="70" r="62" fill="#a6ff1f" opacity=".5" filter="url(#gl)"/>
<circle cx="70" cy="70" r="58" fill="url(#b)"/>
<g clip-path="url(#cb)" fill="none" stroke-linecap="round"><path d="M6 40C52 56 56 98 14 120" stroke="#fff" stroke-width="7" opacity=".95"/><path d="M134 22C86 52 92 96 132 118" stroke="#fff" stroke-width="7" opacity=".95"/>
<path d="M6 40C52 56 56 98 14 120" stroke="#9fc800" stroke-width="2" opacity=".5" transform="translate(4 3)"/></g>
<ellipse cx="48" cy="40" rx="22" ry="11" fill="#fff" opacity=".4" transform="rotate(-32 48 40)"/>
<circle cx="70" cy="70" r="58" fill="none" stroke="#2f5200" stroke-opacity=".45" stroke-width="2"/></svg>
<svg class="rk" width="150" height="230" viewBox="0 0 150 230"><defs>
<linearGradient id="fr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f2f7ff"/><stop offset=".5" stop-color="#6f86c4"/><stop offset="1" stop-color="#dfe8ff"/></linearGradient>
<linearGradient id="hd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4f9a00"/><stop offset=".5" stop-color="#b6f21a"/><stop offset="1" stop-color="#4f9a00"/></linearGradient>
<clipPath id="cr"><ellipse cx="75" cy="70" rx="42" ry="56"/></clipPath><filter id="g2"><feGaussianBlur stdDeviation="5"/></filter></defs>
<g transform="rotate(18 75 120)"><ellipse cx="75" cy="70" rx="46" ry="60" fill="none" stroke="#a6ff1f" stroke-width="8" opacity=".35" filter="url(#g2)"/>
<ellipse cx="75" cy="70" rx="42" ry="56" fill="#0a1636" fill-opacity=".45"/>
<g clip-path="url(#cr)" stroke="#cfe0ff" stroke-width="1.1" opacity=".7"><path d="M45 10V130M55 10V130M65 10V130M75 10V130M85 10V130M95 10V130M105 10V130M30 30H120M30 42H120M30 54H120M30 66H120M30 78H120M30 90H120M30 102H120"/></g>
<ellipse cx="75" cy="70" rx="42" ry="56" fill="none" stroke="url(#fr)" stroke-width="9"/><ellipse cx="75" cy="70" rx="37.5" ry="51.5" fill="none" stroke="#a6ff1f" stroke-width="1.6" opacity=".8"/>
<path d="M52 118L72 160M98 118L78 160" stroke="url(#fr)" stroke-width="7" stroke-linecap="round"/><path d="M60 126L75 158L90 126Z" fill="#0a1636" opacity=".7"/>
<rect x="66" y="156" width="18" height="64" rx="7" fill="url(#hd)"/><path d="M66 166l18-6M66 178l18-6M66 190l18-6M66 202l18-6" stroke="#fff" stroke-opacity=".45" stroke-width="2"/><rect x="64" y="216" width="22" height="9" rx="4" fill="#0f1a3d"/></g></svg>
<h1>TENNIS-<b>IA</b></h1></div>
<div class="card kp"><div>Taux de réussite<b id="k1">–</b></div><div>Meilleur pronostic<b class="g" id="k2">–</b></div><div>Matchs du jour<b id="k3">0</b></div></div>
<div class="tabs"><div class="tab on" data-t="atp">ATP</div><div class="tab" data-t="wta">WTA</div><div class="tab" data-t="suivi">Suivi</div></div>
<div class="days" id="days"></div><main id="list"></main>
<script>
var J=["dim","lun","mar","mer","jeu","ven","sam"],S={tour:"atp",jour:iso(new Date())},IOC={ESP:"ES",RUS:"RU",USA:"US",ITA:"IT",FRA:"FR",GER:"DE",GBR:"GB",SRB:"RS",GRE:"GR",NOR:"NO",DEN:"DK",AUS:"AU",CAN:"CA",ARG:"AR",POL:"PL",CZE:"CZ",BUL:"BG",SUI:"CH",AUT:"AT",BEL:"BE",NED:"NL",JPN:"JP",CHN:"CN",BRA:"BR",CHI:"CL",KAZ:"KZ",CRO:"HR",TUN:"TN",SWE:"SE",FIN:"FI",UKR:"UA",HUN:"HU",POR:"PT",ROU:"RO",BLR:"BY",SVK:"SK",SLO:"SI",LAT:"LV",MON:"MC",CZ:"CZ",COL:"CO",MEX:"MX",PER:"PE",TPE:"TW",KOR:"KR",IND:"IN",RSA:"ZA",EGY:"EG",ISR:"IL",TUR:"TR",EST:"EE",LTU:"LT",GEO:"GE",BIH:"BA",IRL:"IE"};
var SF={Hard:"Dur",Clay:"Terre battue",Grass:"Gazon",Carpet:"Moquette"};
function iso(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function pct(x){return Math.round(x*100)+"%"}
function flag(c){var k=IOC[c];return k?String.fromCodePoint.apply(null,k.split("").map(function(ch){return 127397+ch.charCodeAt(0)})):""}
function ini(n){return n.split(" ").map(function(w){return w[0]}).slice(0,2).join("")}
function days(){var b=document.getElementById("days");b.innerHTML="";for(var i=-3;i<=10;i++){var d=new Date();d.setDate(d.getDate()+i);var k=iso(d),e=el("div","d"+(k===S.jour?" on":""));e.appendChild(el("span","",i===0?"auj.":J[d.getDay()]));e.appendChild(el("b","",String(d.getDate())));e.onclick=function(k){return function(){S.jour=k;days();go()}}(k);b.appendChild(e)}}
function api(t,j){return fetch("/api/calendrier?tour="+t+"&date="+j).then(function(r){return r.json()})}
function fav(m){return m.p_a>=0.5?0:1}
function card(m){
  var c=el("div","card m"),t=el("div","top");
  t.appendChild(el("div","","🕒 "+(m.heure||"–")));
  var lieu=[m.ville,(SF[m.surface]||"")+(m.indoor===true?" Indoor":m.indoor===false?" Outdoor":"")].filter(function(x){return x&&x.trim()}).join(" • ");
  t.appendChild(el("span","",lieu?"📍 "+lieu:""));c.appendChild(t);
  if(m.tour_tableau){c.appendChild(el("div","pick tag",m.tour_tableau))}
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
    var ms=d.matchs;kpis(d.matchs);
    if(d.filtre===false)main.appendChild(el("div","mut","Cotes françaises pas encore chargées : tous les matchs sont affichés."));
    if(!ms.length){main.appendChild(el("div","mut",d.filtre?"Aucun match coté en France ce jour-là.":"Aucun match ce jour-là."));return}
    var cur=null,op=null;ms.forEach(function(m){if(m.opp!=null&&m.etat==="pre"&&(!op||m.valeur>op.valeur))op=m});
    ms.forEach(function(m){if(m.tournoi!==cur){cur=m.tournoi;main.appendChild(el("h2","",cur))}main.appendChild(card(m))});
    if(op){var b=el("div","card ban");b.appendChild(el("span","","💡✅"));var x=el("div","","Bonne opportunité sur "+(op.opp?op.b:op.a).split(" ").pop());x.appendChild(el("small","","("+pct(op.opp?1-op.p_a:op.p_a)+" de chances de victoire)"));b.appendChild(x);main.appendChild(b)}
  }).catch(function(){main.innerHTML="";main.appendChild(el("div","mut","Erreur réseau"))})}
function suivi(main){fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){main.innerHTML="";if(d.erreur){main.appendChild(el("div","mut",d.erreur));return}
  var v=d.vainqueur,o=d.over_under,g=el("div","kpis");
  [[d.n?pct(v.reussite):"–","Vainqueur trouvé ("+d.n+")"],[v.forts_n?pct(v.forts_reussite):"–","Favoris ≥65% ("+v.forts_n+")"],[o.n?pct(o.reussite):"–","Plus/moins de jeux ("+o.n+")"],[o.n?o.jeux_prevus+" / "+o.jeux_reels:"–","Jeux prévus / réels"]].forEach(function(a){var c=el("div","card");c.appendChild(el("b","",a[0]));c.appendChild(el("span","",a[1]));g.appendChild(c)});
  main.appendChild(g);if(d.n)document.getElementById("k1").textContent=pct(v.reussite);
  d.derniers.forEach(function(p){var c=el("div","card m");c.appendChild(el("div","top",p.jour.slice(5)+" · "+p.tournoi));c.appendChild(el("div","res",p.a+" "+pct(p.p_a)+" — "+p.b+" "+pct(1-p.p_a)+" → "+(p.ok_vainqueur?"✅":"❌")+(p.ok_over!=null?"  |  "+p.total_jeux+" jeux "+(p.ok_over?"✅":"❌"):"")));main.appendChild(c)})})}
function go(){var m=document.getElementById("list");m.innerHTML="";m.appendChild(el("div","mut","Chargement…"));
  if(S.tour==="suivi")suivi(m);else home(m)}
document.querySelectorAll(".tab").forEach(function(t){t.onclick=function(){document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("on")});t.classList.add("on");S.tour=t.dataset.t;go()}});
days();go();
fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){if(d.n)document.getElementById("k1").textContent=pct(d.vainqueur.reussite)}).catch(function(){});
</script></body></html>
"""
