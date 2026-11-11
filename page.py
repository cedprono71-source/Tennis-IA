
:root{
  --bg:#101820;
  --card:#1b2733;
  --txt:#f1f5f9;
  --mut:#94a3b8;
  --acc:#22c55e;
  --bd:#2b3a49;
  --bar:#263747;
  --bar2:#22c55e;
}

*{box-sizing:border-box}

body{
  margin:0;
  font-family:Inter,system-ui,-apple-system,sans-serif;
  background:var(--bg);
  color:var(--txt);
  -webkit-font-smoothing:antialiased;
}

header{
  position:sticky;
  top:0;
  background:#141f2a;
  border-bottom:1px solid var(--bd);
  z-index:5;
  padding:13px 14px 10px;
  box-shadow:0 4px 18px rgba(0,0,0,.2);
}

h1{
  font-size:21px;
  font-weight:800;
  letter-spacing:-.6px;
  margin:0 0 12px;
  color:#fff;
}

h1:after{
  content:"ANALYSE & PRONOSTICS";
  display:block;
  font-size:9px;
  letter-spacing:2px;
  color:var(--acc);
  margin-top:3px;
  font-weight:700;
}

.days{
  display:flex;
  gap:7px;
  overflow-x:auto;
  padding:2px 0 9px;
  scrollbar-width:none;
}
.days::-webkit-scrollbar{display:none}

.day{
  flex:0 0 auto;
  min-width:51px;
  text-align:center;
  padding:7px 8px;
  border:1px solid var(--bd);
  border-radius:11px;
  font-size:11px;
  color:var(--mut);
  background:var(--card);
  transition:.2s;
}
.day b{
  display:block;
  font-size:17px;
  color:var(--txt);
  margin-top:2px;
}
.day.on{
  background:var(--acc);
  border-color:var(--acc);
  color:#07150b;
  box-shadow:0 3px 12px rgba(34,197,94,.2);
}
.day.on b{color:#07150b}

.tabs{
  display:flex;
  gap:7px;
  margin-top:5px;
  background:#0e1720;
  padding:4px;
  border-radius:12px;
}

.tab{
  flex:1;
  text-align:center;
  padding:10px 5px;
  border-radius:9px;
  font-size:13px;
  font-weight:750;
  color:var(--mut);
  background:transparent;
  border:1px solid transparent;
  cursor:pointer;
}

.tab.on{
  background:var(--acc);
  color:#07150b;
  border-color:var(--acc);
}

main{
  padding:12px 13px 45px;
  max-width:640px;
  margin:auto;
}

h2{
  font-size:11px;
  color:var(--acc);
  text-transform:uppercase;
  letter-spacing:1.2px;
  margin:20px 4px 9px;
  font-weight:800;
}

.m{
  background:linear-gradient(145deg,#1d2a37,#192530);
  border:1px solid var(--bd);
  border-radius:14px;
  margin-bottom:10px;
  overflow:hidden;
  box-shadow:0 3px 10px rgba(0,0,0,.12);
  transition:border-color .2s;
}

.m.open{border-color:#3b8c5a}

.row{
  display:flex;
  align-items:center;
  gap:10px;
  padding:13px 12px;
  cursor:pointer;
}

.t{
  width:43px;
  font-size:12px;
  color:var(--mut);
  flex:0 0 auto;
  font-weight:650;
}

.p{
  flex:1;
  min-width:0;
  font-size:14px;
  font-weight:550;
}
.p div{
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  padding:2px 0;
}

.p .w{
  color:var(--acc);
  font-weight:800;
}

.pr{
  flex:0 0 auto;
  text-align:right;
  font-size:14px;
  color:var(--mut);
  font-weight:650;
}
.pr div{white-space:nowrap;padding:2px 0}
.pr .fav{
  color:var(--acc);
  font-size:16px;
  font-weight:850;
}

.w{font-weight:800}

.sc{
  font-size:12px;
  color:var(--mut);
  text-align:right;
  flex:0 0 auto;
  line-height:1.7;
  font-weight:650;
}

.det{
  display:none;
  padding:13px 12px 14px;
  border-top:1px solid var(--bd);
  font-size:13px;
  background:#15212b;
}
.m.open .det{display:block}

.ctl{
  display:flex;
  gap:8px;
  margin:5px 0 12px;
}
.ctl select{
  flex:1;
  min-width:0;
  padding:10px;
  border-radius:9px;
  border:1px solid var(--bd);
  background:#202e3b;
  color:var(--txt);
  font-size:13px;
  outline:none;
}

.bar{
  display:flex;
  height:32px;
  border-radius:9px;
  overflow:hidden;
  margin:12px 0;
  background:var(--bar);
  font-size:12px;
  color:#07150b;
  font-weight:800;
}
.bar span{
  display:flex;
  align-items:center;
  padding:0 7px;
  white-space:nowrap;
  overflow:hidden;
}
.bar .a{background:var(--acc)}
.bar .b{
  margin-left:auto;
  color:#e2e8f0;
}

table{
  width:100%;
  border-collapse:collapse;
  margin-top:10px;
  background:#1b2935;
  border-radius:9px;
  overflow:hidden;
}
td,th{
  padding:9px 5px;
  text-align:center;
  border-bottom:1px solid var(--bd);
  font-size:12px;
}
th{
  color:var(--mut);
  font-weight:650;
  background:#202e3b;
}
td{color:var(--txt)}

.mut{
  color:var(--mut);
  font-size:11px;
  margin-top:9px;
  line-height:1.6;
}

.err{
  color:#f87171;
  padding:12px 0;
  font-size:13px;
}

.kpis{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:9px;
  margin-bottom:12px;
}

.kpi{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:13px;
  padding:13px;
}
.kpi b{
  display:block;
  font-size:24px;
  font-weight:850;
  color:var(--acc);
}
.kpi span{
  font-size:11px;
  color:var(--mut);
}

.ok{color:var(--acc)}
.ko{color:#f87171}

.empty{
  text-align:center;
  color:var(--mut);
  padding:45px 12px;
  font-size:13px;
}

@media(min-width:500px){
  main{padding-top:18px}
  .row{padding:15px}
  .p{font-size:15px}
}
