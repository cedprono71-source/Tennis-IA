
PAGE = r"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TENNIS-IA</title>
<meta name="theme-color" content="#030817">
<link href="https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,600;0,800;1,900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root{
--l:#a6ff00;
--bg:#030817;
--c:#0a1935;
--bd:#244b79;
--t:#fff;
--m:#a8bddb;
}
*{box-sizing:border-box}
body{
margin:0;background:var(--bg);color:var(--t);
font-family:Inter,system-ui,sans-serif;
-webkit-tap-highlight-color:transparent;
}
.hero{height:210px;position:relative;overflow:hidden;background:#030817 url('/tennis-ia-header.jpg') center center/100% 100% no-repeat;border-bottom:1px solid #174c81}
radial-gradient(ellipse at 15% 35%,#0874e755,transparent 45%),
radial-gradient(ellipse at 85% 25%,#0755c955,transparent 50%),
linear-gradient(180deg,#02091b,#061631 65%,#030817);
border-bottom:1px solid #174c81;
}
.hero:before{
content:"";position:absolute;left:-15%;top:90px;width:130%;height:4px;
background:linear-gradient(90deg,transparent,#a6ff00,transparent);
transform:rotate(-12deg);
box-shadow:0 0 18px #a6ff00,0 0 35px #00aaff;
}
.hero:after{
content:"";position:absolute;inset:0;
background:repeating-linear-gradient(115deg,transparent 0 35px,#168aff08 36px 38px);
pointer-events:none;
}
.hero svg{position:absolute;z-index:1}
.ball{left:3%;top:30px;filter:drop-shadow(0 0 18px #a6ff0088)}
.rk{right:0;top:0;filter:drop-shadow(0 0 16px #168aff77)}
.hero h1{
position:absolute;z-index:2;left:0;right:0;top:72px;
text-align:center;margin:0;
font:italic 900 51px/1 "Exo 2",Inter,sans-serif;
letter-spacing:-2px;text-shadow:0 4px 20px #000;
}
.hero h1 b{color:var(--l)}
.card{
background:linear-gradient(145deg,#10294c,#07162e 75%);
border:1px solid #3972a0;
border-radius:23px;
box-shadow:inset 0 1px 5px #83caff22,0 5px 20px #0007;
}
.kp{
margin:-27px 12px 22px;position:relative;z-index:3;
display:flex;padding:13px 5px;
border:1.5px solid #78caff;
background:linear-gradient(110deg,#0b2344,#020b1c);
box-shadow:0 0 16px #168aff55,inset 0 0 12px #168aff22;
}
.kp div{
flex:1;padding:2px 7px;
border-right:1px solid #315477;
font-size:11px;color:var(--m);
text-align:center;
}
.kp div:last-child{border:0}
.kp b{
display:block;font:800 23px "Exo 2";
color:white;margin-top:4px;
}
.kp b.g{color:var(--l);font-size:17px;white-space:nowrap}
.tabs{
display:flex;gap:9px;padding:0 12px;
}
.tab{
flex:1;padding:13px 4px;text-align:center;
border:1.5px solid #31577e;border-radius:22px;
background:linear-gradient(145deg,#102747,#07152c);
font:800 17px "Exo 2";
text-transform:uppercase;color:white;
box-shadow:inset 0 1px 5px #ffffff0b;
transition:.2s;
}
.tab.on{
background:linear-gradient(135deg,#c3ff21,#83df00);
color:#071509;border-color:#baff00;
box-shadow:0 0 15px #a6ff0099,0 0 30px #a6ff0033;
}
.days{
display:flex;gap:7px;overflow-x:auto;
padding:16px 12px;scrollbar-width:none;
}
.days::-webkit-scrollbar{display:none}
.d{
flex:0 0 auto;padding:7px 13px;
border-radius:14px;border:1px solid #294b70;
background:#0b1d39;font-size:12px;
color:var(--m);text-align:center;
}
.d b{display:block;font-size:17px;color:white;margin-top:3px}
.d.on{
border-color:var(--l);color:var(--l);
background:#192c28;box-shadow:0 0 12px #a6ff0055;
}
main{padding:0 12px}
h2{
display:flex;align-items:center;
font:800 25px "Exo 2";margin:17px 4px 17px;
position:relative;
}
h2:before{
content:"";width:6px;height:33px;
background:var(--l);border-radius:5px;
margin-right:12px;box-shadow:0 0 12px var(--l);
}
h2:after{
content:"";height:1px;flex:1;margin-left:12px;
background:linear-gradient(90deg,#376b9d,transparent);
}
.m{
position:relative;margin:18px 0 17px;
padding:14px 11px 13px;
border:1.5px solid #4385b6;
background:linear-gradient(140deg,#10294b 0%,#07172e 65%,#061126 100%);
box-shadow:0 0 12px #168aff22,inset 0 0 18px #168aff12;
border-radius:25px;
}
.top{
display:flex;align-items:center;justify-content:space-between;
gap:5px;font-size:14px;font-weight:700;
margin-bottom:13px;padding:0 2px;
}
.top span{color:#d0e3fa;text-align:right;font-size:12px}
.pick{
position:absolute;right:-4px;top:-16px;
background:linear-gradient(135deg,#caff22,#85df00);
color:#071509;font:800 15px "Exo 2";
padding:8px 15px;border-radius:18px;
box-shadow:0 0 18px #a6ff0099;
border:1px solid #e1ff72;
}
.tag{
background:#405c85;color:white;
padding:7px 13px;border-radius:15px;
font-size:12px;border:1px solid #789bc7;
}
.g3{
display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2.8fr) minmax(0,1fr);
gap:7px;align-items:center;
}
.pl{
text-align:center;font:800 15px/1.2 "Exo 2";
overflow-wrap:anywhere;
}
.av{
width:100%;max-width:76px;height:72px;
margin:0 auto 9px;border-radius:19px;
background:linear-gradient(145deg,#112c50,#07162e);
border:1px solid #31577e;
display:flex;align-items:center;justify-content:center;
color:#9cc5f0;font:800 23px "Exo 2";
box-shadow:inset 0 0 15px #168aff16;
}
.fl{font-size:24px;margin-top:7px}
.mid{
background:linear-gradient(145deg,#020a19,#061329);
border:1px solid #193c60;
border-radius:20px;padding:13px 8px;
box-shadow:inset 0 0 15px #0008;
}
.pc{display:flex}
.pc div{
flex:1;text-align:center;
font:800 clamp(27px,7vw,39px) "Exo 2";
}
.pc div+div{border-left:1px solid #375575}
.pc small{
display:block;font:600 13px Inter;color:#e2ebf8;
}
.pc .w{
color:var(--l);text-shadow:0 0 14px #a6ff0055;
}
.bar{
height:12px;border-radius:12px;
background:#294a73;margin-top:13px;
position:relative;overflow:hidden;
}
.bar i{
position:absolute;top:0;bottom:0;
background:linear-gradient(90deg,#baff19,#83e800);
border-radius:12px;
box-shadow:0 0 12px #a6ff00;
}
.res{
text-align:center;font-size:12px;
color:#b9cde5;margin-top:10px;
}
.det{
display:none;margin-top:13px;font-size:14px;
border-top:1px solid #315477;padding-top:10px;
}
.m.open .det{display:block}
.det table{
width:100%;border-collapse:collapse;margin-top:8px;
}
.det td,.det th{
padding:8px 5px;text-align:center;
border-bottom:1px solid #294665;
}
.det th{color:#a9bfd9;font-weight:600}
.hi{color:var(--l);font-weight:800}
.ban{
display:flex;align-items:center;gap:12px;
padding:15px;margin:17px 0 18px;
font-weight:700;
background:linear-gradient(110deg,#173d32,#092b42 65%,#06172e);
border:1.5px solid #9eff19;
box-shadow:0 0 17px #a6ff0044,0 0 20px #168aff33;
border-radius:23px;
}
.ban>span{font-size:30px}
.ban small{
display:block;color:#d3e5f8;
font-weight:500;margin-top:4px;
}
.mut{
color:var(--m);text-align:center;
padding:36px 10px;font-size:14px;
}
.kpis{
display:grid;grid-template-columns:1fr 1fr;
gap:10px;margin-bottom:12px;
}
.kpis .card{padding:14px}
.kpis b{
display:block;font:800 28px "Exo 2";
color:var(--l);text-shadow:0 0 12px #a6ff0044;
}
.kpis span{font-size:12px;color:var(--m)}
.sw{
display:flex;justify-content:space-between;
align-items:center;padding:16px;
}
.sw input{width:24px;height:24px}
@media(max-width:380px){
.hero{height:195px}
.hero h1{font-size:43px;top:75px}
.ball{width:115px;height:115px}
.rk{width:120px}
.kp div{font-size:10px;padding:2px 4px}
.kp b{font-size:20px}
.tab{font-size:15px}
.g3{grid-template-columns:minmax(0,.9fr) minmax(0,2.5fr) minmax(0,.9fr);gap:5px}
.pl{font-size:13px}
.av{height:60px}
.pc div{font-size:27px}
.pc small{font-size:11px}
.mid{padding:11px 5px}
}
</style>
</head>

<body>

<div class="hero">
<svg class="ball" width="150" height="150" viewBox="0 0 140 140">
<defs>
<radialGradient id="b" cx="36%" cy="30%" r="78%">
<stop offset="0" stop-color="#f6ff93"/>
<stop offset=".45" stop-color="#c8f500"/>
<stop offset="1" stop-color="#5a9400"/>
</radialGradient>
<clipPath id="cb"><circle cx="70" cy="70" r="58"/></clipPath>
<filter id="gl"><feGaussianBlur stdDeviation="7"/></filter>
</defs>
<circle cx="70" cy="70" r="62" fill="#a6ff1f" opacity=".5" filter="url(#gl)"/>
<circle cx="70" cy="70" r="58" fill="url(#b)"/>
<g clip-path="url(#cb)" fill="none" stroke-linecap="round">
<path d="M6 40C52 56 56 98 14 120" stroke="#fff" stroke-width="7" opacity=".95"/>
<path d="M134 22C86 52 92 96 132 118" stroke="#fff" stroke-width="7" opacity=".95"/>
<path d="M6 40C52 56 56 98 14 120" stroke="#9fc800" stroke-width="2" opacity=".5" transform="translate(4 3)"/>
</g>
<ellipse cx="48" cy="40" rx="22" ry="11" fill="#fff" opacity=".4" transform="rotate(-32 48 40)"/>
<circle cx="70" cy="70" r="58" fill="none" stroke="#2f5200" stroke-opacity=".45" stroke-width="2"/>
</svg>

<svg class="rk" width="150" height="230" viewBox="0 0 150 230">
<defs>
<linearGradient id="fr" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#f2f7ff"/>
<stop offset=".5" stop-color="#6f86c4"/>
<stop offset="1" stop-color="#dfe8ff"/>
</linearGradient>
<linearGradient id="hd" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#4f9a00"/>
<stop offset=".5" stop-color="#b6f21a"/>
<stop offset="1" stop-color="#4f9a00"/>
</linearGradient>
<clipPath id="cr"><ellipse cx="75" cy="70" rx="42" ry="56"/></clipPath>
<filter id="g2"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<g transform="rotate(18 75 120)">
<ellipse cx="75" cy="70" rx="46" ry="60" fill="none" stroke="#a6ff1f" stroke-width="8" opacity=".35" filter="url(#g2)"/>
<ellipse cx="75" cy="70" rx="42" ry="56" fill="#0a1636" fill-opacity=".45"/>
<g clip-path="url(#cr)" stroke="#cfe0ff" stroke-width="1.1" opacity=".7">
<path d="M45 10V130M55 10V130M65 10V130M75 10V130M85 10V130M95 10V130M105 10V130M30 30H120M30 42H120M30 54H120M30 66H120M30 78H120M30 90H120M30 102H120"/>
</g>
<ellipse cx="75" cy="70" rx="42" ry="56" fill="none" stroke="url(#fr)" stroke-width="9"/>
<ellipse cx="75" cy="70" rx="37.5" ry="51.5" fill="none" stroke="#a6ff1f" stroke-width="1.6" opacity=".8"/>
<path d="M52 118L72 160M98 118L78 160" stroke="url(#fr)" stroke-width="7" stroke-linecap="round"/>
<path d="M60 126L75 158L90 126Z" fill="#0a1636" opacity=".7"/>
<rect x="66" y="156" width="18" height="64" rx="7" fill="url(#hd)"/>
<path d="M66 166l18-6M66 178l18-6M66 190l18-6M66 202l18-6" stroke="#fff" stroke-opacity=".45" stroke-width="2"/>
<rect x="64" y="216" width="22" height="9" rx="4" fill="#0f1a3d"/>
</g>
</svg>

<h1>TENNIS-<b>IA</b></h1>
</div>

<div class="card kp">
<div>Taux de réussite<b id="k1">–</b></div>
<div>Meilleur pronostic<b class="g" id="k2">–</b></div>
<div>Matchs du jour<b id="k3">0</b></div>
</div>

<div class="tabs">
<div class="tab on" data-t="atp">ATP</div>
<div class="tab" data-t="wta">WTA</div>
<div class="tab" data-t="suivi">Suivi</div>
</div>

<div class="days" id="days"></div>
<main id="list"></main>

<script>
var J=["dim","lun","mar","mer","jeu","ven","sam"],S={tour:"atp",jour:iso(new Date())},IOC={ESP:"ES",RUS:"RU",USA:"US",ITA:"IT",FRA:"FR",GER:"DE",GBR:"GB",SRB:"RS",GRE:"GR",NOR:"NO",DEN:"DK",AUS:"AU",CAN:"CA",ARG:"AR",POL:"PL",CZE:"CZ",BUL:"BG",SUI:"CH",AUT:"AT",BEL:"BE",NED:"NL",JPN:"JP",CHN:"CN",BRA:"BR",CHI:"CL",KAZ:"KZ",CRO:"HR",TUN:"TN",SWE:"SE",FIN:"FI",UKR:"UA",HUN:"HU",POR:"PT",ROU:"RO",BLR:"BY",SVK:"SK",SLO:"SI",LAT:"LV",MON:"MC",CZ:"CZ",COL:"CO",MEX:"MX",PER:"PE",TPE:"TW",KOR:"KR",IND:"IN",RSA:"ZA",EGY:"EG",ISR:"IL",TUR:"TR",EST:"EE",LTU:"LT",GEO:"GE",BIH:"BA",IRL:"IE"};
var SF={Hard:"Dur",Clay:"Terre battue",Grass:"Gazon",Carpet:"Moquette"};

function iso(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function el(t,c,x){var e=document.createElement(t);if(c)e.className=c;if(x!==undefined)e.textContent=x;return e}
function pct(x){return Math.round(x*100)+"%"}
function flag(c){var k=IOC[c];return k?String.fromCodePoint.apply(null,k.split("").map(function(ch){return 127397+ch.charCodeAt(0)})):""}
function ini(n){return n.split(" ").map(function(w){return w[0]}).slice(0,2).join("")}

function days(){
var b=document.getElementById("days");b.innerHTML="";
for(var i=-3;i<=10;i++){
var d=new Date();d.setDate(d.getDate()+i);
var k=iso(d),e=el("div","d"+(k===S.jour?" on":""));
e.appendChild(el("span","",i===0?"auj.":J[d.getDay()]));
e.appendChild(el("b","",String(d.getDate())));
e.onclick=function(k){return function(){S.jour=k;days();go()}}(k);
b.appendChild(e)
}}

function api(t,j){
return fetch("/api/calendrier?tour="+t+"&date="+j).then(function(r){return r.json()})
}
function fav(m){return m.p_a>=0.5?0:1}

function card(m){
var c=el("div","card m"),t=el("div","top");
t.appendChild(el("div","","🕒 "+(m.heure||"–")));
var lieu=[m.ville,(SF[m.surface]||"")+(m.indoor===true?" Indoor":m.indoor===false?" Outdoor":"")].filter(function(x){return x&&x.trim()}).join(" • ");
t.appendChild(el("span","",lieu?"📍 "+lieu:""));
c.appendChild(t);
if(m.tour_tableau){c.appendChild(el("div","pick tag",m.tour_tableau))}
var g=el("div","g3");
function pl(n,p){
var d=el("div","pl"),a=el("div","av",ini(n));
d.appendChild(a);d.appendChild(el("div","",n));
d.appendChild(el("div","fl",flag(p)));
return d
}
g.appendChild(pl(m.a,m.pays_a));
var mid=el("div","mid");
if(m.p_a!=null){
var f=fav(m),pc=el("div","pc"),
x=el("div",f===0?"w":"",pct(m.p_a)),
y=el("div",f===1?"w":"",pct(1-m.p_a));
x.appendChild(el("small","","Victoire"));
y.appendChild(el("small","","Victoire"));
pc.appendChild(x);pc.appendChild(y);mid.appendChild(pc);
var bar=el("div","bar"),i=el("i");
i.style[f===0?"left":"right"]="0";
i.style.width=(Math.max(m.p_a,1-m.p_a)*100)+"%";
bar.appendChild(i);mid.appendChild(bar)
}else{
mid.appendChild(el("div","res","Pronostic à venir"))
}
g.appendChild(mid);g.appendChild(pl(m.b,m.pays_b));c.appendChild(g);
if(m.etat==="post"||m.etat==="in"){
c.appendChild(el("div","res",(m.etat==="in"?"En cours · ":"")+m.scores[0].join(" ")+" / "+m.scores[1].join(" ")+(m.ok===1?" ✅":m.ok===0?" ❌":"")))
}
var d=el("div","det");c.appendChild(d);var ok=false;
c.onclick=function(){c.classList.toggle("open");if(!ok){ok=true;detail(d,m)}};
return c
}

function detail(d,m){
d.appendChild(el("div","res","Calcul en cours…"));
var u="/match?tour="+m.tour+"&a="+encodeURIComponent(m.a)+"&b="+encodeURIComponent(m.b)+"&surface=auto&best_of=0&tournoi="+encodeURIComponent(m.tournoi||"");
if(m.lignes&&m.lignes.length)u+="&lignes="+m.lignes.join(",");
fetch(u).then(function(r){return r.json()}).then(function(r){
d.innerHTML="";
if(r.erreur){d.appendChild(el("div","res",r.erreur));return}
d.appendChild(el("div","res","Surface : "+r.surface+" · "+r.format+" · Jeux attendus : "+r.jeux_attendus));
var k=Object.keys(r.over);
if(m.lignes)k=m.lignes.map(function(l){return l.toFixed(1)}).filter(function(x){return r.over[x]!==undefined});
if(k.length){
var t=el("table"),h=el("tr");
["Jeux","Plus de","Moins de"].forEach(function(x){h.appendChild(el("th","",x))});
t.appendChild(h);
k.forEach(function(x){
var q=el("tr");
q.appendChild(el("td","",x));
q.appendChild(el("td",r.over[x]>.5?"hi":"",pct(r.over[x])));
q.appendChild(el("td",r.over[x]<.5?"hi":"",pct(1-r.over[x])));
t.appendChild(q)
});
d.appendChild(t)
}else{
d.appendChild(el("div","res","Plus/moins de jeux : non proposé en France pour ce match."))
}
})
}

function kpis(ms){
document.getElementById("k3").textContent=ms.length;
var best=null;
ms.forEach(function(m){
if(m.p_a!=null&&m.etat==="pre"){
var c=Math.max(m.p_a,1-m.p_a);
if(!best||c>best.c)best={c:c,m:m}
}
});
document.getElementById("k2").textContent=best?(best.m[fav(best.m)?"b":"a"].split(" ").pop()+" "+pct(best.c)):"–";
return best
}

function home(main){
api(S.tour,S.jour).then(function(d){
main.innerHTML="";
if(d.erreur){main.appendChild(el("div","mut",d.erreur));return}
var ms=d.matchs;kpis(d.matchs);
if(d.filtre===false)main.appendChild(el("div","mut","Cotes françaises pas encore chargées : tous les matchs sont affichés."));
if(!ms.length){
main.appendChild(el("div","mut",d.filtre?"Aucun match coté en France ce jour-là.":"Aucun match ce jour-là."));
return
}
var cur=null,op=null;
ms.forEach(function(m){
if(m.opp!=null&&m.etat==="pre"&&(!op||m.valeur>op.valeur))op=m
});
ms.forEach(function(m){
if(m.tournoi!==cur){
cur=m.tournoi;main.appendChild(el("h2","",cur))
}
main.appendChild(card(m))
});
if(op){
var b=el("div","card ban");
b.appendChild(el("span","","💡✅"));
var x=el("div","","Bonne opportunité sur "+(op.opp?op.b:op.a).split(" ").pop());
x.appendChild(el("small","","("+pct(op.opp?1-op.p_a:op.p_a)+" de chances de victoire)"));
b.appendChild(x);main.appendChild(b)
}
}).catch(function(){
main.innerHTML="";
main.appendChild(el("div","mut","Erreur réseau"))
})
}

function suivi(main){
fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){
main.innerHTML="";
if(d.erreur){main.appendChild(el("div","mut",d.erreur));return}
var v=d.vainqueur,o=d.over_under,g=el("div","kpis");
[
[d.n?pct(v.reussite):"–","Vainqueur trouvé ("+d.n+")"],
[v.forts_n?pct(v.forts_reussite):"–","Favoris ≥65% ("+v.forts_n+")"],
[o.n?pct(o.reussite):"–","Plus/moins de jeux ("+o.n+")"],
[o.n?o.jeux_prevus+" / "+o.jeux_reels:"–","Jeux prévus / réels"]
].forEach(function(a){
var c=el("div","card");
c.appendChild(el("b","",a[0]));
c.appendChild(el("span","",a[1]));
g.appendChild(c)
});
main.appendChild(g);
if(d.n)document.getElementById("k1").textContent=pct(v.reussite);
d.derniers.forEach(function(p){
var c=el("div","card m");
c.appendChild(el("div","top",p.jour.slice(5)+" · "+p.tournoi));
c.appendChild(el("div","res",p.a+" "+pct(p.p_a)+" — "+p.b+" "+pct(1-p.p_a)+" → "+(p.ok_vainqueur?"✅":"❌")+(p.ok_over!=null?"  |  "+p.total_jeux+" jeux "+(p.ok_over?"✅":"❌"):"")));
main.appendChild(c)
})
})
}

function go(){
var m=document.getElementById("list");
m.innerHTML="";
m.appendChild(el("div","mut","Chargement…"));
if(S.tour==="suivi")suivi(m);else home(m)
}

document.querySelectorAll(".tab").forEach(function(t){
t.onclick=function(){
document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("on")});
t.classList.add("on");
S.tour=t.dataset.t;
go()
}
});

days();go();

fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){
if(d.n)document.getElementById("k1").textContent=pct(d.vainqueur.reussite)
}).catch(function(){});
</script>
</body>
</html>
"""
