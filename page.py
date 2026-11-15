
PAGE = r"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Pronostics Tennis</title>
<meta name="theme-color" content="#080F20">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root{
--bg:#080F20;
--card:#111D35;
--card2:#162440;
--txt:#F0F5FF;
--mut:#899BB8;
--acc:#2785FF;
--acc2:#55B4FF;
--bd:#263B5E;
--bar:#263B5E;
--hard:#2785FF;
--clay:#E58A4B;
--grass:#42C98A;
--ok:#38D99A;
--ko:#FF647C;
--f1:'Barlow Condensed',sans-serif;
--f2:'Inter',sans-serif;
}

*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
margin:0;
background:var(--bg);
color:var(--txt);
font-family:var(--f2);
font-variant-numeric:tabular-nums;
-webkit-font-smoothing:antialiased;
}

header{
position:sticky;
top:0;
z-index:10;
background:rgba(8,15,32,.96);
backdrop-filter:blur(16px);
border-bottom:1px solid var(--bd);
padding:12px 12px 9px;
}

.top{
display:flex;
align-items:center;
justify-content:space-between;
max-width:700px;
margin:auto;
}

.brand{
display:flex;
align-items:center;
gap:9px;
font-family:var(--f1);
font-size:25px;
font-weight:800;
letter-spacing:.02em;
text-transform:uppercase;
}

.logo{
width:34px;
height:34px;
border-radius:50%;
display:flex;
align-items:center;
justify-content:center;
background:linear-gradient(135deg,#55B4FF,#1261D9);
box-shadow:0 0 20px #2785FF55;
font-size:19px;
}

.brand span{color:var(--acc2)}

.status{
font-size:10px;
color:#55B4FF;
border:1px solid #2785FF55;
padding:5px 8px;
border-radius:20px;
letter-spacing:.06em;
}

.days{
display:flex;
gap:7px;
overflow-x:auto;
padding:12px 0 8px;
scrollbar-width:none;
max-width:700px;
margin:auto;
}
.days::-webkit-scrollbar{display:none}

.day{
flex:0 0 auto;
min-width:54px;
text-align:center;
padding:7px 8px;
border:1px solid var(--bd);
border-radius:12px;
font-size:11px;
font-weight:600;
color:var(--mut);
background:var(--card);
text-transform:uppercase;
}

.day b{
display:block;
font-size:18px;
color:var(--txt);
}

.day.on{
background:var(--acc);
border-color:var(--acc);
color:white;
box-shadow:0 3px 14px #2785FF55;
}
.day.on b{color:white}

.tabs{
display:flex;
gap:7px;
max-width:700px;
margin:10px auto 0;
}

.tab{
flex:1;
text-align:center;
padding:10px 5px;
border:1px solid var(--bd);
border-radius:11px;
font-family:var(--f1);
font-size:17px;
font-weight:700;
letter-spacing:.04em;
text-transform:uppercase;
background:var(--card);
color:var(--mut);
cursor:pointer;
}

.tab.on{
background:linear-gradient(135deg,#2785FF,#1765D5);
border-color:var(--acc);
color:white;
box-shadow:0 3px 15px #2785FF44;
}

main{
padding:12px 12px 50px;
max-width:700px;
margin:auto;
}

/* ACCUEIL */

.hero{
position:relative;
overflow:hidden;
padding:26px 20px;
border-radius:20px;
margin:8px 0 16px;
background:
radial-gradient(circle at 85% 20%,#2785FF55,transparent 38%),
linear-gradient(135deg,#142B50,#0D1830 70%);
border:1px solid #31517C;
}

.hero:after{
content:"🎾";
position:absolute;
right:8px;
bottom:0;
font-size:105px;
opacity:.13;
transform:rotate(-20deg);
pointer-events:none;
}

.hero-label{
font-size:11px;
font-weight:700;
letter-spacing:.13em;
color:var(--acc2);
text-transform:uppercase;
}

.hero h2{
font-family:var(--f1);
font-size:43px;
line-height:1;
margin:13px 0;
color:white;
letter-spacing:.02em;
text-transform:uppercase;
}

.hero h2 span{color:var(--acc2)}

.hero p{
font-size:13px;
line-height:1.7;
color:#B8C9E2;
max-width:330px;
margin:0 0 20px;
}

.primary{
border:0;
border-radius:12px;
padding:13px 19px;
background:linear-gradient(135deg,#2785FF,#1765D5);
color:white;
font-family:var(--f2);
font-weight:700;
font-size:13px;
box-shadow:0 5px 20px #2785FF55;
cursor:pointer;
}

.section-title{
font-family:var(--f1);
font-size:22px;
font-weight:700;
text-transform:uppercase;
letter-spacing:.05em;
margin:22px 3px 10px;
}

.features{
display:grid;
grid-template-columns:repeat(2,minmax(0,1fr));
gap:10px;
}

.feature{
background:var(--card);
border:1px solid var(--bd);
border-radius:15px;
padding:15px;
}

.feature-icon{
font-size:23px;
margin-bottom:8px;
}

.feature b{
display:block;
font-size:13px;
margin-bottom:5px;
}

.feature span{
font-size:11px;
line-height:1.5;
color:var(--mut);
}

.home-links{
display:grid;
gap:9px;
margin-top:12px;
}

.home-link{
display:flex;
align-items:center;
justify-content:space-between;
padding:15px;
background:var(--card);
border:1px solid var(--bd);
border-radius:13px;
cursor:pointer;
}

.home-link b{font-size:14px}
.home-link span{color:var(--acc2);font-size:12px}

/* PRONOSTICS */

h2.tournament{
font-family:var(--f1);
font-size:19px;
letter-spacing:.06em;
text-transform:uppercase;
color:var(--txt);
margin:22px 4px 10px;
display:flex;
align-items:center;
gap:9px;
}

.dot{
display:inline-block;
width:9px;
height:9px;
border-radius:50%;
flex:0 0 auto;
}
.dot.Hard{background:var(--hard)}
.dot.Clay{background:var(--clay)}
.dot.Grass{background:var(--grass)}
.dot.Carpet{background:var(--mut)}

.m{
background:var(--card);
border:1px solid var(--bd);
border-radius:15px;
margin-bottom:10px;
overflow:hidden;
transition:border-color .2s;
}

.m.open{border-color:var(--acc)}

.row{
display:flex;
align-items:center;
gap:10px;
padding:14px 12px 12px;
cursor:pointer;
}

.t{
width:43px;
font-size:12px;
font-weight:600;
color:var(--mut);
flex:0 0 auto;
}

.p{
flex:1;
min-width:0;
font-size:14px;
font-weight:500;
line-height:1.8;
}

.p div{
white-space:nowrap;
overflow:hidden;
text-overflow:ellipsis;
}

.w{font-weight:800;color:white}

.pr{
flex:0 0 auto;
text-align:right;
font-size:14px;
font-weight:600;
color:var(--mut);
line-height:1.8;
}

.pr div{white-space:nowrap}
.pr .fav{color:var(--txt);font-weight:800}
.pr .hot{color:var(--acc2)}

.sc{
font-size:12px;
color:var(--mut);
text-align:right;
flex:0 0 auto;
line-height:1.8;
}

.mbar{
height:4px;
background:var(--bar);
}
.mbar i{
display:block;
height:100%;
background:linear-gradient(90deg,#1765D5,#55B4FF);
}

.det{
display:none;
padding:0 12px 14px;
border-top:1px solid var(--bd);
font-size:13px;
}
.m.open .det{display:block}

.ctl{
display:flex;
gap:8px;
margin:12px 0;
}

.ctl select{
flex:1;
min-width:0;
padding:10px;
border-radius:10px;
border:1px solid var(--bd);
background:#0B1529;
color:var(--txt);
font-family:var(--f2);
font-size:13px;
}

.bar{
display:flex;
height:32px;
border-radius:9px;
overflow:hidden;
margin:10px 0;
background:var(--bar);
font-size:12px;
font-weight:700;
}

.bar span{
display:flex;
align-items:center;
padding:0 8px;
white-space:nowrap;
}
.bar .a{
background:linear-gradient(90deg,#1765D5,#2785FF);
color:white;
}
.bar .b{
margin-left:auto;
color:var(--txt);
}

table{
width:100%;
border-collapse:collapse;
margin-top:10px;
}

td,th{
padding:9px 4px;
text-align:center;
border-bottom:1px solid var(--bd);
font-size:13px;
}

th{
color:var(--mut);
font-family:var(--f1);
font-size:14px;
letter-spacing:.06em;
text-transform:uppercase;
}

.mut{
color:var(--mut);
font-size:11px;
margin-top:8px;
line-height:1.6;
}

.err{color:var(--ko);padding:10px 0}

.kpis{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
margin:10px 0;
}

.kpi{
background:var(--card);
border:1px solid var(--bd);
border-radius:15px;
padding:13px;
}

.kpi b{
display:block;
font-family:var(--f1);
font-size:30px;
color:var(--acc2);
line-height:1.1;
}

.kpi span{
font-size:11px;
color:var(--mut);
}

.ok{color:var(--ok)}
.ko{color:var(--ko)}

.empty{
text-align:center;
color:var(--mut);
padding:45px 10px;
font-size:13px;
}

@media(min-width:550px){
.hero{padding:35px 30px}
.hero h2{font-size:52px}
.row{padding:16px}
.p{font-size:15px}
}
</style>
</head>

<body>

<header>
<div class="top">
<div class="brand">
<div class="logo">🎾</div>
<div>PRONOSTICS <span>TENNIS</span></div>
</div>
<div class="status">ANALYSE IA</div>
</div>

<div class="days" id="days"></div>

<div class="tabs">
<div class="tab" data-t="accueil">Accueil</div>
<div class="tab on" data-t="atp">ATP</div>
<div class="tab" data-t="wta">WTA</div>
<div class="tab" data-t="suivi">Suivi</div>
</div>
</header>

<main id="list">
<div class="empty">Chargement…</div>
</main>

<script>
var JOURS=["dim","lun","mar","mer","jeu","ven","sam"];
var etat={tour:"atp",jour:iso(new Date())};

function iso(d){
return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")
}

function el(tag,cls,txt){
var e=document.createElement(tag);
if(cls)e.className=cls;
if(txt!==undefined)e.textContent=txt;
return e;
}

function pct(x){return Math.round(x*100)+"%"}

function choisirTour(t){
etat.tour=t;
document.querySelectorAll(".tab").forEach(function(x){
x.classList.toggle("on",x.dataset.t===t);
});
document.getElementById("days").style.display=
(t==="atp"||t==="wta")?"flex":"none";
charger();
}

document.querySelectorAll(".tab").forEach(function(t){
t.onclick=function(){choisirTour(t.dataset.t)}
});

function buildDays(){
var box=document.getElementById("days");
box.innerHTML="";
for(var i=-3;i<=10;i++){
var d=new Date();
d.setDate(d.getDate()+i);
var k=iso(d);
var b=el("div","day"+(k===etat.jour?" on":""));
b.appendChild(el("span","",i===0?"auj.":JOURS[d.getDay()]));
b.appendChild(el("b","",String(d.getDate())));
b.onclick=function(k){
return function(){
etat.jour=k;
buildDays();
charger();
}
}(k);
box.appendChild(b);
if(i===0&&k===etat.jour){
setTimeout(function(){b.scrollIntoView({inline:"center",block:"nearest"})},50);
}
}
}

function accueil(main){
main.innerHTML="";

var hero=el("section","hero");
hero.appendChild(el("div","hero-label","Analyse • Prédictions • Performance"));
var titre=el("h2");
titre.appendChild(document.createTextNode("Pronostics "));
titre.appendChild(el("span","", "Tennis"));
hero.appendChild(titre);
hero.appendChild(el("p","","Retrouvez les analyses et probabilités des matchs ATP et WTA. Des données pour mieux comprendre chaque rencontre."));
var btn=el("button","primary","Voir les pronostics →");
btn.onclick=function(){choisirTour("atp")};
hero.appendChild(btn);
main.appendChild(hero);

main.appendChild(el("div","section-title","Votre espace tennis"));

var features=el("div","features");
[
["🎾","ATP","Les matchs et analyses du circuit masculin."],
["🏆","WTA","Les rencontres et probabilités du circuit féminin."],
["📊","Analyses IA","Probabilités de victoire et statistiques de match."],
["📈","Suivi","Retrouvez les résultats et les performances."]
].forEach(function(x){
var f=el("div","feature");
f.appendChild(el("div","feature-icon","",));
f.lastChild.textContent=x[0];
f.appendChild(el("b","",x[1]));
f.appendChild(el("span","",x[2]));
features.appendChild(f);
});
main.appendChild(features);

main.appendChild(el("div","section-title","Accès rapide"));
var links=el("div","home-links");

[
["🎾  Pronostics ATP","atp"],
["🏆  Pronostics WTA","wta"],
["📊  Suivi des résultats","suivi"]
].forEach(function(x){
var l=el("div","home-link");
l.appendChild(el("b","",x[0]));
l.appendChild(el("span","","Ouvrir →"));
l.onclick=function(){choisirTour(x[1])};
links.appendChild(l);
});
main.appendChild(links);
}

function charger(){
var main=document.getElementById("list");
main.innerHTML="";
main.appendChild(el("div","empty","Chargement…"));

if(etat.tour==="accueil"){
accueil(main);
return;
}

if(etat.tour==="suivi"){
return chargerSuivi(main);
}

var tour=etat.tour,jour=etat.jour;

fetch("/api/calendrier?tour="+tour+"&date="+jour)
.then(function(r){return r.json()})
.then(function(d){
if(tour!==etat.tour||jour!==etat.jour)return;
main.innerHTML="";

if(d.erreur){
main.appendChild(el("div","err","Calendrier indisponible : "+d.erreur));
return;
}

if(!d.matchs.length){
main.appendChild(el("div","empty","Aucun match ce jour-là."));
return;
}

var cur=null,surf={};
d.matchs.forEach(function(m){
if(m.surface&&!surf[m.tournoi])surf[m.tournoi]=m.surface;
});

d.matchs.forEach(function(m){
if(m.tournoi!==cur){
cur=m.tournoi;
var h=el("h2","tournament");
if(surf[cur])h.appendChild(el("span","dot "+surf[cur]));
h.appendChild(el("span","",cur));
main.appendChild(h);
}
main.appendChild(carte(m));
});
})
.catch(function(){
main.innerHTML="";
main.appendChild(el("div","err","Erreur réseau"));
});
}

function kpi(valeur,libelle){
var k=el("div","kpi");
k.appendChild(el("b","",valeur));
k.appendChild(el("span","",libelle));
return k;
}

function chargerSuivi(main){
fetch("/api/suivi")
.then(function(r){return r.json()})
.then(function(d){
if(etat.tour!=="suivi")return;
main.innerHTML="";

if(d.erreur){
main.appendChild(el("div","err",d.erreur));
return;
}

var v=d.vainqueur,o=d.over_under;
var g=el("div","kpis");

g.appendChild(kpi(d.n?pct(v.reussite):"–","Vainqueur trouvé ("+d.n+" matchs)"));
g.appendChild(kpi(v.forts_n?pct(v.forts_reussite):"–","Favoris ≥65% ("+v.forts_n+")"));
g.appendChild(kpi(o.n?pct(o.reussite):"–","Plus/moins de jeux ("+o.n+")"));
g.appendChild(kpi(o.n?(o.jeux_prevus+" / "+o.jeux_reels):"–","Jeux prévus / réels"));

main.appendChild(g);

main.appendChild(el("div","mut","En attente de résultat : "+d.en_attente+" · Dernier tour automatique : "+(d.cycle.dernier||"–")+" ("+d.cycle.resume+")"));

if(!d.derniers.length){
main.appendChild(el("div","empty","Pas encore de résultat. Les pronostics sont enregistrés automatiquement avant chaque match."));
return;
}

main.appendChild(el("h2","tournament","Derniers résultats"));

d.derniers.forEach(function(p){
var c=el("div","m"),row=el("div","row");
row.appendChild(el("div","t",p.jour.slice(5)));

var n=el("div","p");
n.appendChild(el("div",p.gagnant===0?"w":"",p.a));
n.appendChild(el("div",p.gagnant===1?"w":"",p.b));
row.appendChild(n);

var q=el("div","pr");
q.appendChild(el("div","",pct(p.p_a)+" / "+pct(1-p.p_a)));
q.appendChild(el("div",p.ok_vainqueur?"ok":"ko",p.ok_vainqueur?"✅ vainqueur":"❌ vainqueur"));

if(p.ok_over!==null&&p.ok_over!==undefined){
q.appendChild(el("div",p.ok_over?"ok":"ko",(p.ok_over?"✅ ":"❌ ")+p.total_jeux+" jeux (sur "+p.ligne+")"));
}

row.appendChild(q);
c.appendChild(row);
main.appendChild(c);
});
})
.catch(function(){
main.innerHTML="";
main.appendChild(el("div","err","Erreur réseau"));
});
}

function carte(m){
var c=el("div","m");
var row=el("div","row");

row.appendChild(el("div","t",m.heure||"–"));

var p=el("div","p");
p.appendChild(el("div",m.gagnant===0?"w":"",m.a));
p.appendChild(el("div",m.gagnant===1?"w":"",m.b));
row.appendChild(p);

if(m.p_a!==null&&m.p_a!==undefined){
var pr=el("div","pr");
function cl(p){
return(p>=0.5?"fav":"")+(p>=0.65?" hot":"");
}
pr.appendChild(el("div",cl(m.p_a),pct(m.p_a)+(m.ok===1?" ✅":m.ok===0?" ❌":"")));
pr.appendChild(el("div",cl(1-m.p_a),pct(1-m.p_a)));
row.appendChild(pr);
}

var sc=el("div","sc");
if(m.etat==="post"||m.etat==="in"){
[0,1].forEach(function(i){
sc.appendChild(el("div","",m.scores[i].join(" ")||"–"));
});
}else{
sc.textContent=m.tour_tableau;
}
row.appendChild(sc);
c.appendChild(row);

if(m.p_a!==null&&m.p_a!==undefined){
var mb=el("div","mbar");
var f=el("i");
f.style.width=(m.p_a*100)+"%";
mb.appendChild(f);
c.appendChild(mb);
}

var det=el("div","det");
c.appendChild(det);
var charge=false;

row.onclick=function(){
c.classList.toggle("open");
if(!charge){
charge=true;
formulaire(det,m);
}
};
return c;
}

function formulaire(det,m){
var ctl=el("div","ctl");
var sf=el("select");

[["auto","Surface auto"],["Hard","Dur"],["Clay","Terre"],["Grass","Gazon"]].forEach(function(s){
var o=el("option","",s[1]);
o.value=s[0];
sf.appendChild(o);
});

var bo=el("select");
[["0","Format auto"],["3","3 sets"],["5","5 sets"]].forEach(function(s){
var o=el("option","",s[1]);
o.value=s[0];
bo.appendChild(o);
});

ctl.appendChild(sf);
ctl.appendChild(bo);
det.appendChild(ctl);

var res=el("div");
det.appendChild(res);

function go(){
res.innerHTML="";
res.appendChild(el("div","mut","Calcul en cours…"));

var u="/match?tour="+m.tour+
"&a="+encodeURIComponent(m.a)+
"&b="+encodeURIComponent(m.b)+
"&surface="+sf.value+
"&best_of="+bo.value+
"&tournoi="+encodeURIComponent(m.tournoi||"");

fetch(u)
.then(function(r){return r.json()})
.then(function(d){afficher(res,d)})
.catch(function(){
res.innerHTML="";
res.appendChild(el("div","err","Erreur réseau"));
});
}

sf.onchange=go;
bo.onchange=go;
go();
}

function afficher(res,d){
res.innerHTML="";

if(d.erreur){
res.appendChild(el("div","err",d.erreur));
return;
}

var noms=Object.keys(d.proba_victoire_elo);
var pa=d.proba_victoire_elo[noms[0]];
var pb=d.proba_victoire_elo[noms[1]];

var bar=el("div","bar");
var a=el("span","a",noms[0].split(" ").pop()+" "+pct(pa));
a.style.width=(pa*100)+"%";
var b=el("span","b",pct(pb)+" "+noms[1].split(" ").pop());

bar.appendChild(a);
bar.appendChild(b);
res.appendChild(bar);

res.appendChild(el("div","mut","Surface : "+d.surface+" · "+d.format));

res.appendChild(el("div","mut","Jeux attendus : "+d.jeux_attendus+" · Service (pts gagnés) : "+d.points_au_service[noms[0]]+" / "+d.points_au_service[noms[1]]));

var t=el("table");
var h=el("tr");
["Jeux","Plus de","Moins de"].forEach(function(x){
h.appendChild(el("th","",x));
});
t.appendChild(h);

Object.keys(d.over).forEach(function(l){
var r=el("tr");
r.appendChild(el("td","",l));
r.appendChild(el("td","",pct(d.over[l])));
r.appendChild(el("td","",pct(1-d.over[l])));
t.appendChild(r);
});
res.appendChild(t);

var s=el("table");
var hs=el("tr");
hs.appendChild(el("th","","Score en sets"));
hs.appendChild(el("th","","Proba"));
s.appendChild(hs);

Object.keys(d.sets).forEach(function(k){
var r=el("tr");
r.appendChild(el("td","",k));
r.appendChild(el("td","",pct(d.sets[k])));
s.appendChild(r);
});
res.appendChild(s);

res.appendChild(el("div","mut","Basé sur l'Elo par surface et les statistiques de service. Les totaux de jeux ne sont pas encore calibrés."));
}

buildDays();
charger();
</script>
</body>
</html>
"""
