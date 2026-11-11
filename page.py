PAGE = r"""<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pronostics Tennis</title>
<style>
:root{--bg:#f4f6f8;--card:#fff;--txt:#111827;--mut:#6b7280;--acc:#16a34a;--bd:#e5e7eb;--bar:#dbeafe;--bar2:#16a34a}
@media (prefers-color-scheme:dark){:root{--bg:#0f1419;--card:#1a2129;--txt:#e5e7eb;--mut:#9ca3af;--acc:#22c55e;--bd:#2a333d;--bar:#1e3a5f;--bar2:#22c55e}}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;background:var(--bg);color:var(--txt)}
header{position:sticky;top:0;background:var(--card);border-bottom:1px solid var(--bd);z-index:5;padding:10px 12px 6px}
h1{font-size:18px;margin:0 0 8px}
.days{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px}
.day{flex:0 0 auto;min-width:52px;text-align:center;padding:6px 8px;border:1px solid var(--bd);border-radius:10px;font-size:12px;color:var(--mut);background:var(--card)}
.day b{display:block;font-size:16px;color:var(--txt)}
.day.on{background:var(--acc);border-color:var(--acc);color:#fff}.day.on b{color:#fff}
.tabs{display:flex;gap:8px;margin-top:6px}
.tab{flex:1;text-align:center;padding:8px;border:1px solid var(--bd);border-radius:10px;font-weight:600;background:var(--card)}
.tab.on{background:var(--txt);color:var(--bg);border-color:var(--txt)}
main{padding:10px 12px 40px;max-width:640px;margin:auto}
h2{font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;margin:16px 4px 6px}
.m{background:var(--card);border:1px solid var(--bd);border-radius:12px;margin-bottom:8px;overflow:hidden}
.row{display:flex;align-items:center;gap:10px;padding:10px 12px}
.t{width:44px;font-size:13px;color:var(--mut);flex:0 0 auto}
.p{flex:1;min-width:0;font-size:15px}.p div{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pr{flex:0 0 auto;text-align:right;font-size:14px;color:var(--mut)}.pr div{white-space:nowrap}.pr .fav{color:var(--acc);font-weight:700}
.w{font-weight:700}.sc{font-size:13px;color:var(--mut);text-align:right;flex:0 0 auto}
.det{display:none;padding:0 12px 12px;border-top:1px solid var(--bd);font-size:14px}.m.open .det{display:block}
.ctl{display:flex;gap:8px;margin:10px 0}.ctl select{flex:1;padding:8px;border-radius:8px;border:1px solid var(--bd);background:var(--bg);color:var(--txt);font-size:14px}
.bar{display:flex;height:26px;border-radius:8px;overflow:hidden;margin:6px 0;background:var(--bar);font-size:13px;color:#fff}
.bar span{display:flex;align-items:center;padding:0 8px;white-space:nowrap}.bar .a{background:var(--bar2)}.bar .b{margin-left:auto;color:var(--txt)}
table{width:100%;border-collapse:collapse;margin-top:6px}td,th{padding:5px 4px;text-align:center;border-bottom:1px solid var(--bd);font-size:13px}th{color:var(--mut);font-weight:500}
.mut{color:var(--mut);font-size:12px;margin-top:8px}.err{color:#dc2626;padding:8px 0}
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}.kpi{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:10px 12px}.kpi b{display:block;font-size:22px}.kpi span{font-size:12px;color:var(--mut)}
.ok{color:var(--acc)}.ko{color:#dc2626}.empty{text-align:center;color:var(--mut);padding:40px 10px}
</style></head><body>
<header><h1>🎾 Pronostics Tennis</h1><div class="days" id="days"></div>
<div class="tabs"><div class="tab on" data-t="atp">ATP</div><div class="tab" data-t="wta">WTA</div><div class="tab" data-t="suivi">Suivi</div></div></header>
<main id="list"><div class="empty">Chargement…</div></main>
<script>
var JOURS=["dim","lun","mar","mer","jeu","ven","sam"];
var etat={tour:"atp",jour:iso(new Date())};
function iso(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e}
function pct(x){return Math.round(x*100)+"%"}

function buildDays(){
  var box=document.getElementById("days");box.innerHTML="";
  for(var i=-3;i<=10;i++){
    var d=new Date();d.setDate(d.getDate()+i);var k=iso(d);
    var b=el("div","day"+(k===etat.jour?" on":""));
    b.appendChild(el("span","",i===0?"auj.":JOURS[d.getDay()]));b.appendChild(el("b","",String(d.getDate())));
    b.onclick=function(k){return function(){etat.jour=k;buildDays();charger()}}(k);
    box.appendChild(b);
    if(i===0&&k===etat.jour){setTimeout(function(){b.scrollIntoView({inline:"center",block:"nearest"})},50)}
  }
}
document.querySelectorAll(".tab").forEach(function(t){t.onclick=function(){
  document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("on")});t.classList.add("on");
  etat.tour=t.dataset.t;document.getElementById("days").style.display=(etat.tour==="suivi")?"none":"flex";charger()}});

function charger(){
  var main=document.getElementById("list");main.innerHTML="";main.appendChild(el("div","empty","Chargement…"));
  if(etat.tour==="suivi"){return chargerSuivi(main)}
  var tour=etat.tour,jour=etat.jour;
  fetch("/api/calendrier?tour="+tour+"&date="+jour).then(function(r){return r.json()}).then(function(d){
    if(tour!==etat.tour||jour!==etat.jour)return;
    main.innerHTML="";
    if(d.erreur){main.appendChild(el("div","err","Calendrier indisponible : "+d.erreur));return}
    if(!d.matchs.length){main.appendChild(el("div","empty","Aucun match ce jour-là."));return}
    var cur=null;
    d.matchs.forEach(function(m){
      if(m.tournoi!==cur){cur=m.tournoi;main.appendChild(el("h2","",cur))}
      main.appendChild(carte(m));
    });
  }).catch(function(e){main.innerHTML="";main.appendChild(el("div","err","Erreur réseau"))});
}

function kpi(valeur,libelle){var k=el("div","kpi");k.appendChild(el("b","",valeur));k.appendChild(el("span","",libelle));return k}
function chargerSuivi(main){
  fetch("/api/suivi").then(function(r){return r.json()}).then(function(d){
    if(etat.tour!=="suivi")return;
    main.innerHTML="";
    if(d.erreur){main.appendChild(el("div","err",d.erreur));return}
    var v=d.vainqueur,o=d.over_under;
    var g=el("div","kpis");
    g.appendChild(kpi(d.n?pct(v.reussite):"–","Vainqueur trouvé ("+d.n+" matchs)"));
    g.appendChild(kpi(v.forts_n?pct(v.forts_reussite):"–","Favoris ≥65% ("+v.forts_n+")"));
    g.appendChild(kpi(o.n?pct(o.reussite):"–","Plus/moins de jeux ("+o.n+")"));
    g.appendChild(kpi(o.n?(o.jeux_prevus+" / "+o.jeux_reels):"–","Jeux prévus / réels"));
    main.appendChild(g);
    main.appendChild(el("div","mut","En attente de résultat : "+d.en_attente+" · Dernier tour automatique : "+(d.cycle.dernier||"–")+" ("+d.cycle.resume+")"));
    if(!d.derniers.length){main.appendChild(el("div","empty","Pas encore de résultat. Les pronostics sont enregistrés automatiquement avant chaque match."));return}
    main.appendChild(el("h2","","Derniers résultats"));
    d.derniers.forEach(function(p){
      var c=el("div","m"),row=el("div","row");
      row.appendChild(el("div","t",p.jour.slice(5)));
      var n=el("div","p");n.appendChild(el("div",p.gagnant===0?"w":"",p.a));n.appendChild(el("div",p.gagnant===1?"w":"",p.b));row.appendChild(n);
      var q=el("div","pr");q.appendChild(el("div","",pct(p.p_a)+" / "+pct(1-p.p_a)));
      var l=el("div",p.ok_vainqueur?"ok":"ko",(p.ok_vainqueur?"✅ vainqueur":"❌ vainqueur"));q.appendChild(l);
      if(p.ok_over!==null&&p.ok_over!==undefined){q.appendChild(el("div",p.ok_over?"ok":"ko",(p.ok_over?"✅ ":"❌ ")+p.total_jeux+" jeux (sur "+p.ligne+")"))}
      row.appendChild(q);c.appendChild(row);main.appendChild(c);
    });
  }).catch(function(){main.innerHTML="";main.appendChild(el("div","err","Erreur réseau"))});
}

function devinerSurface(t){
  if(/french open|roland|monte.carlo|madrid|rome|italian|barcelona|hamburg|estoril|houston|bucharest|geneva|lyon|munich|marrakech|buenos|rio |santiago|bastad|gstaad|umag|kitzb|bogot|cordoba|parma|charleston|strasbourg|rabat|clay/i.test(t))return"Clay";
  if(/wimbledon|halle|queen|eastbourne|mallorca|hertogenbosch|newport|berlin|nottingham|birmingham|grass/i.test(t))return"Grass";
  return"Hard";
}
function devinerBo(t,tour){return(tour==="atp"&&/australian open|french open|roland|wimbledon|us open/i.test(t))?5:3}

function carte(m){
  var c=el("div","m");var row=el("div","row");
  row.appendChild(el("div","t",m.heure||"–"));
  var p=el("div","p");
  p.appendChild(el("div",m.gagnant===0?"w":"",m.a));p.appendChild(el("div",m.gagnant===1?"w":"",m.b));
  row.appendChild(p);
  if(m.p_a!==null&&m.p_a!==undefined){
    var pr=el("div","pr");
    pr.appendChild(el("div",m.p_a>=0.5?"fav":"",pct(m.p_a)+(m.ok===1?" ✅":m.ok===0?" ❌":"")));
    pr.appendChild(el("div",m.p_a<0.5?"fav":"",pct(1-m.p_a)));
    row.appendChild(pr);
  }
  var sc=el("div","sc");
  if(m.etat==="post"||m.etat==="in"){
    [0,1].forEach(function(i){sc.appendChild(el("div","",m.scores[i].join(" ")||"–"))});
  }else{sc.textContent=m.tour_tableau}
  row.appendChild(sc);c.appendChild(row);
  var det=el("div","det");c.appendChild(det);var charge=false;
  row.onclick=function(){
    c.classList.toggle("open");
    if(!charge){charge=true;formulaire(det,m)}
  };
  return c;
}

function formulaire(det,m){
  var ctl=el("div","ctl");
  var sf=el("select");[["auto","Surface auto"],["Hard","Dur"],["Clay","Terre"],["Grass","Gazon"]].forEach(function(s){var o=el("option","",s[1]);o.value=s[0];sf.appendChild(o)});
  var bo=el("select");[["0","Format auto"],["3","3 sets"],["5","5 sets"]].forEach(function(s){var o=el("option","",s[1]);o.value=s[0];bo.appendChild(o)});
  ctl.appendChild(sf);ctl.appendChild(bo);det.appendChild(ctl);
  var res=el("div");det.appendChild(res);
  function go(){
    res.innerHTML="";res.appendChild(el("div","mut","Calcul en cours…"));
    var u="/match?tour="+m.tour+"&a="+encodeURIComponent(m.a)+"&b="+encodeURIComponent(m.b)+"&surface="+sf.value+"&best_of="+bo.value+"&tournoi="+encodeURIComponent(m.tournoi||"");
    fetch(u).then(function(r){return r.json()}).then(function(d){afficher(res,d)}).catch(function(){res.innerHTML="";res.appendChild(el("div","err","Erreur réseau"))});
  }
  sf.onchange=go;bo.onchange=go;go();
}

function afficher(res,d){
  res.innerHTML="";
  if(d.erreur){res.appendChild(el("div","err",d.erreur));return}
  var noms=Object.keys(d.proba_victoire_elo);var pa=d.proba_victoire_elo[noms[0]],pb=d.proba_victoire_elo[noms[1]];
  var bar=el("div","bar");var a=el("span","a",noms[0].split(" ").pop()+" "+pct(pa));a.style.width=(pa*100)+"%";
  var b=el("span","b",pct(pb)+" "+noms[1].split(" ").pop());bar.appendChild(a);bar.appendChild(b);res.appendChild(bar);
  res.appendChild(el("div","mut","Surface : "+d.surface+" · "+d.format));
  res.appendChild(el("div","mut","Jeux attendus : "+d.jeux_attendus+" · Service (pts gagnés) : "+d.points_au_service[noms[0]]+" / "+d.points_au_service[noms[1]]));
  var t=el("table");var h=el("tr");["Jeux","Plus de","Moins de"].forEach(function(x){h.appendChild(el("th","",x))});t.appendChild(h);
  Object.keys(d.over).forEach(function(l){var r=el("tr");r.appendChild(el("td","",l));r.appendChild(el("td","",pct(d.over[l])));r.appendChild(el("td","",pct(1-d.over[l])));t.appendChild(r)});
  res.appendChild(t);
  var s=el("table");var hs=el("tr");hs.appendChild(el("th","","Score en sets"));hs.appendChild(el("th","","Proba"));s.appendChild(hs);
  Object.keys(d.sets).forEach(function(k){var r=el("tr");r.appendChild(el("td","",k));r.appendChild(el("td","",pct(d.sets[k])));s.appendChild(r)});
  res.appendChild(s);
  res.appendChild(el("div","mut","Basé sur l'Elo par surface et les statistiques de service. Les totaux de jeux ne sont pas encore calibrés."));
}
buildDays();charger();
</script></body></html>
"""
