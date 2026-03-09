#!/usr/bin/env python3
"""
PrettyScan - Framework visual para escaneos de red
Requisitos: pip install -r requirements.txt
Ejecutar:   python app.py
Acceder:    http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
import subprocess
import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PrettyScan</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
:root{--bg:#0a0e1a;--s:#111827;--s2:#1a2235;--a:#00d4ff;--a2:#7c3aed;--ok:#10b981;--warn:#f59e0b;--err:#ef4444;--tx:#e2e8f0;--mt:#64748b;--bd:#1e293b}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--tx);min-height:100vh}
header{background:linear-gradient(135deg,#0d1b2a,#1a0533);border-bottom:1px solid var(--bd);padding:0 2rem;display:flex;align-items:center;justify-content:space-between;height:64px;position:sticky;top:0;z-index:100;box-shadow:0 4px 20px #0008}
.logo{display:flex;align-items:center;gap:.75rem;font-size:1.3rem;font-weight:700;letter-spacing:.05em}
.logo-icon{width:36px;height:36px;background:linear-gradient(135deg,var(--a),var(--a2));border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1rem}
.logo span{color:var(--a)}
.header-right{display:flex;align-items:center;gap:1rem}
.hm{font-size:.8rem;color:var(--mt)}
.lang-toggle{display:flex;align-items:center;background:var(--s2);border:1px solid var(--bd);border-radius:8px;overflow:hidden}
.lang-btn{padding:.35rem .75rem;font-size:.78rem;font-weight:700;letter-spacing:.05em;border:none;background:transparent;color:var(--mt);cursor:pointer;transition:all .2s}
.lang-btn.active{background:linear-gradient(135deg,var(--a),var(--a2));color:#0a0e1a}
.wrap{max-width:1400px;margin:0 auto;padding:2rem}
.panel{background:var(--s);border:1px solid var(--bd);border-radius:16px;padding:1.5rem 2rem;margin-bottom:2rem}
.panel h2{font-size:.9rem;color:var(--a);margin-bottom:1rem;letter-spacing:.05em;text-transform:uppercase}
.presets{display:grid;grid-template-columns:repeat(auto-fill,minmax(145px,1fr));gap:.5rem;margin-bottom:1rem}
.pb{background:var(--s2);border:1px solid var(--bd);color:var(--tx);padding:.4rem .9rem;border-radius:8px;cursor:pointer;font-size:.82rem;transition:all .2s;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:100%}
.pb:hover{border-color:var(--a);color:var(--a)}
.sf{display:grid;grid-template-columns:1fr auto auto;gap:.75rem;align-items:end}
.fg{display:flex;flex-direction:column;gap:.4rem}
.fg label{font-size:.8rem;color:var(--mt)}
.fi{background:var(--bg);border:1px solid var(--bd);color:var(--tx);padding:.65rem 1rem;border-radius:10px;font-size:.9rem;outline:none;transition:border-color .2s;font-family:'Courier New',monospace}
.fi:focus{border-color:var(--a)}
.bs{background:linear-gradient(135deg,var(--a),#0099bb);border:none;color:#0a0e1a;font-weight:700;padding:.65rem 1.8rem;border-radius:10px;cursor:pointer;font-size:.9rem;transition:opacity .2s;white-space:nowrap}
.bs:hover{opacity:.85}.bs:disabled{opacity:.5;cursor:not-allowed}
#loader{display:none;text-align:center;padding:3rem}
.spin{width:50px;height:50px;border:3px solid var(--bd);border-top-color:var(--a);border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 1rem}
.lt{color:var(--mt);font-size:.9rem}
.sg{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem}
.sc{background:var(--s);border:1px solid var(--bd);border-radius:12px;padding:1.2rem;text-align:center;transition:transform .2s}
.sc:hover{transform:translateY(-2px)}
.sv{font-size:2rem;font-weight:700;line-height:1}
.sl{font-size:.75rem;color:var(--mt);margin-top:.4rem;text-transform:uppercase;letter-spacing:.05em}
.hs h2{font-size:.9rem;color:var(--a);text-transform:uppercase;letter-spacing:.05em;margin-bottom:1rem}
.hcard{background:var(--s);border:1px solid var(--bd);border-radius:14px;margin-bottom:1.5rem;overflow:hidden}
.hh{background:linear-gradient(90deg,var(--s2),transparent);padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;border-bottom:1px solid var(--bd)}
.hip{font-size:1.1rem;font-weight:700;font-family:'Courier New',monospace;color:var(--a)}
.hi{display:flex;gap:.75rem;align-items:center;flex-wrap:wrap}
.tag{display:inline-flex;align-items:center;gap:.3rem;padding:.25rem .75rem;border-radius:6px;font-size:.78rem;font-weight:600}
.up{background:rgba(16,185,129,.15);color:var(--ok);border:1px solid rgba(16,185,129,.3)}
.dn{background:rgba(239,68,68,.15);color:var(--err);border:1px solid rgba(239,68,68,.3)}
.os{background:rgba(0,212,255,.1);color:var(--a);border:1px solid rgba(0,212,255,.2)}
.pw{padding:1.2rem 1.5rem;overflow-x:auto}
.pt{width:100%;border-collapse:collapse;font-size:.85rem}
.pt th{text-align:left;padding:.6rem .8rem;color:var(--mt);font-size:.75rem;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid var(--bd)}
.pt td{padding:.6rem .8rem;border-bottom:1px solid rgba(30,41,59,.5);font-family:'Courier New',monospace}
.pt tr:last-child td{border-bottom:none}
.pt tr:hover td{background:rgba(0,212,255,.03)}
.open{color:var(--ok);font-weight:700}.closed{color:var(--err)}.filtered{color:var(--warn)}
.rc{background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.3)}
.rh{background:rgba(245,158,11,.15);color:#f59e0b;border:1px solid rgba(245,158,11,.3)}
.rm{background:rgba(59,130,246,.15);color:#3b82f6;border:1px solid rgba(59,130,246,.3)}
.rl{background:rgba(100,116,139,.15);color:#94a3b8;border:1px solid rgba(100,116,139,.3)}
.card-actions{display:flex;gap:.5rem;align-items:center}
.card-btn{background:transparent;border:1px solid var(--bd);color:var(--mt);padding:.28rem .65rem;border-radius:6px;cursor:pointer;font-size:.75rem;transition:all .2s;white-space:nowrap}
.card-btn:hover{border-color:var(--a);color:var(--a)}
.card-btn.copy:hover{border-color:var(--a2);color:#a78bfa}
.dc{background:rgba(239,68,68,.12);color:#f87171;border:1px solid rgba(239,68,68,.35);font-weight:700}
.scripts-cell{font-size:.75rem;line-height:1.6;max-width:400px}
.script-id{color:var(--a);font-weight:700;font-family:'Courier New',monospace;display:block}
.script-out{color:#94a3b8;white-space:pre-wrap;word-break:break-word;display:block;padding-left:.5rem;border-left:2px solid var(--bd);margin-bottom:.4rem}
.eb{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:#fca5a5;padding:1rem 1.5rem;border-radius:12px;font-size:.88rem;display:none;margin-bottom:1rem}
#toast{position:fixed;bottom:2rem;right:2rem;background:#10b981;color:#fff;padding:.8rem 1.4rem;border-radius:10px;font-size:.88rem;font-weight:600;opacity:0;transform:translateY(10px);transition:all .3s;z-index:999;pointer-events:none}
#toast.show{opacity:1;transform:translateY(0)}
#cap-overlay{display:none;position:fixed;inset:0;background:#0a0e1aee;z-index:500;align-items:center;justify-content:center;flex-direction:column;gap:1rem}
#cap-overlay.show{display:flex}
.cap-spin{width:48px;height:48px;border:3px solid #1e293b;border-top-color:var(--a);border-radius:50%;animation:spin 1s linear infinite}
.cap-text{color:var(--mt);font-size:.9rem}
@keyframes spin{to{transform:rotate(360deg)}}
@media(max-width:800px){
  .sf{grid-template-columns:1fr}
  .sf .bs{width:100%}
  header{padding:0 1rem}
  .wrap{padding:1rem}
  .hm{display:none}
}
</style>
</head>
<body>
<div id="toast"></div>
<div id="cap-overlay"><div class="cap-spin"></div><p class="cap-text" id="txt-generating">Generando imagen...</p></div>

<header>
  <div class="logo"><div class="logo-icon">🔍</div>Pretty<span>Scan</span></div>
  <div class="header-right">
    <div class="hm" id="st">Framework Visual de Reconocimiento de Red</div>
    <div class="lang-toggle">
      <button class="lang-btn active" id="btn-es" onclick="setLang('es')">ES</button>
      <button class="lang-btn" id="btn-en" onclick="setLang('en')">EN</button>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="panel">
    <h2 id="txt-new-scan">⚡ Nuevo Escaneo</h2>
    <div class="presets">
      <button class="pb" onclick="sp('localhost','-sV -p 1-1000')" id="pre-localhost">🖥 Localhost</button>
      <button class="pb" onclick="sp('','-sV -sC -p 22,80,443,3306,8080')" id="pre-common">🔍 Puertos comunes</button>
      <button class="pb" onclick="sp('','-sV -p-')" id="pre-full">🌐 Full port scan</button>
      <button class="pb" onclick="sp('','-sV --script vuln')" id="pre-vuln">⚠️ Vuln scan</button>
      <button class="pb" onclick="sp('','-O')" id="pre-os">💻 OS Detection</button>
      <button class="pb" onclick="sp('','-sU -p 53,123,161')" id="pre-udp">📡 UDP común</button>
      <button class="pb" onclick="sp('','-sV -sC --script=banner')" id="pre-banner">🏷 Banners</button>
    </div>
    <div class="sf">
      <div class="fg">
        <label id="txt-target-label">TARGET — IP, hostname o rango CIDR</label>
        <input id="tgt" class="fi" placeholder="192.168.1.1 | 10.0.0.0/24 | scanme.nmap.org"/>
      </div>
      <div class="fg">
        <label id="txt-options-label">OPCIONES DE ESCANEO</label>
        <input id="opt" class="fi" value="-sV -p 1-1000" style="min-width:200px"/>
      </div>
      <button class="bs" id="bsc" onclick="run()">▶ <span id="txt-scan-btn">Escanear</span></button>
    </div>
  </div>

  <div class="eb" id="eb"></div>
  <div id="loader"><div class="spin"></div><p class="lt" id="lt">Iniciando escaneo...</p></div>

  <div id="res" style="display:none">
    <div class="sg" id="sg"></div>
    <div class="hs"><h2 id="txt-hosts-title">🖧 Hosts Descubiertos</h2><div id="hc"></div></div>
  </div>
</div>

<script>
const T={
  es:{newScan:'⚡ Nuevo Escaneo',targetLabel:'TARGET — IP, hostname o rango CIDR',optionsLabel:'OPCIONES DE ESCANEO',scanBtn:'Escanear',hostsTitle:'🖧 Hosts Descubiertos',statActive:'Hosts activos',statTotal:'Total hosts',statOpen:'Puertos abiertos',statDur:'Duración',generating:'Generando imagen...',downloaded:'✅ Imagen descargada',copied:'✅ Copiada al portapapeles',clipFail:'⚠️ Portapapeles no disponible',noHosts:'No se encontraron hosts.',errEmpty:'Introduce un target válido.',errConn:'Error de conexión con el servidor.',ports:'puertos',imgBtn:'Imagen',copyBtn:'Copiar',thPort:'PUERTO',thProto:'PROTO',thState:'ESTADO',thSvc:'SERVICIO',thVer:'VERSIÓN',thRisk:'RIESGO',thScripts:'SCRIPTS',stOpen:'ABIERTO',stClosed:'CERRADO',stFiltered:'FILTRADO',rc:'CRÍTICO',rh:'ALTO',rm:'MEDIO',rl:'BAJO',online:'● ONLINE',offline:'● OFFLINE',loaderMsgs:['Resolviendo objetivo...','Enviando paquetes...','Esperando respuestas...','Procesando resultados...'],preCommon:'🔍 Puertos comunes',preUdp:'📡 UDP común',scanLabel:'Escaneo: '},
  en:{newScan:'⚡ New Scan',targetLabel:'TARGET — IP, hostname or CIDR range',optionsLabel:'SCAN OPTIONS',scanBtn:'Scan',hostsTitle:'🖧 Discovered Hosts',statActive:'Active hosts',statTotal:'Total hosts',statOpen:'Open ports',statDur:'Duration',generating:'Generating image...',downloaded:'✅ Image downloaded',copied:'✅ Copied to clipboard',clipFail:'⚠️ Clipboard unavailable',noHosts:'No hosts found.',errEmpty:'Please enter a valid target.',errConn:'Connection error. Is app.py running?',ports:'ports',imgBtn:'Image',copyBtn:'Copy',thPort:'PORT',thProto:'PROTO',thState:'STATE',thSvc:'SERVICE',thVer:'VERSION',thRisk:'RISK',thScripts:'SCRIPTS',stOpen:'OPEN',stClosed:'CLOSED',stFiltered:'FILTERED',rc:'CRITICAL',rh:'HIGH',rm:'MEDIUM',rl:'LOW',online:'● ONLINE',offline:'● OFFLINE',loaderMsgs:['Resolving target...','Sending packets...','Waiting for responses...','Processing results...'],preCommon:'🔍 Common ports',preUdp:'📡 Common UDP',scanLabel:'Scan: '}
};
let lang='es';

function setLang(l){
  lang=l;const t=T[l];
  document.getElementById('btn-es').classList.toggle('active',l==='es');
  document.getElementById('btn-en').classList.toggle('active',l==='en');
  document.getElementById('txt-new-scan').textContent=t.newScan;
  document.getElementById('txt-target-label').textContent=t.targetLabel;
  document.getElementById('txt-options-label').textContent=t.optionsLabel;
  document.getElementById('txt-scan-btn').textContent=t.scanBtn;
  document.getElementById('txt-hosts-title').textContent=t.hostsTitle;
  document.getElementById('txt-generating').textContent=t.generating;
  document.getElementById('pre-common').textContent=t.preCommon;
  document.getElementById('pre-udp').textContent=t.preUdp;
  document.querySelectorAll('.txt-ports').forEach(e=>e.textContent=t.ports);
  document.querySelectorAll('.txt-img-btn').forEach(e=>e.textContent=t.imgBtn);
  document.querySelectorAll('.txt-copy-btn').forEach(e=>e.textContent=t.copyBtn);
  if(window._lastData) render(window._lastData);
}

function sp(t,o){if(t)document.getElementById('tgt').value=t;document.getElementById('opt').value=o}

function toast(msg,ok=true){
  const el=document.getElementById('toast');
  el.textContent=msg;el.style.background=ok?'#10b981':'#ef4444';
  el.classList.add('show');setTimeout(()=>el.classList.remove('show'),3200);
}

function err(m){const e=document.getElementById('eb');e.textContent='❌ '+m;e.style.display='block'}

function risk(p){
  const t=T[lang];
  // Critical: remote access, exposed DBs, dangerous services
  const c=[21,22,23,3389,5900,5901,6379,27017,9200,5432,1521,2049];
  // High: web, mail, DNS, SMB, MSSQL, AD
  const h=[25,53,80,110,143,443,445,8080,8443,8888,1433,3306,389,636,3268,3269];
  // Medium: other known ports below 1024
  const n=parseInt(p);
  if(c.includes(n))return`<span class="tag rc">${t.rc}</span>`;
  if(h.includes(n))return`<span class="tag rh">${t.rh}</span>`;
  if(n<1024)return`<span class="tag rm">${t.rm}</span>`;
  return`<span class="tag rl">${t.rl}</span>`;
}

function stateLabel(s){
  const t=T[lang];
  if(s==='open')return t.stOpen;
  if(s==='closed')return t.stClosed;
  return t.stFiltered;
}

async function exportCard(cardId,mode,ip){
  const el=document.getElementById(cardId);
  const overlay=document.getElementById('cap-overlay');
  overlay.classList.add('show');
  const actions=el.querySelectorAll('.card-actions');
  actions.forEach(a=>a.style.visibility='hidden');
  await new Promise(r=>setTimeout(r,60));
  try{
    const canvas=await html2canvas(el,{backgroundColor:'#111827',scale:2,useCORS:true,logging:false});
    actions.forEach(a=>a.style.visibility='visible');
    overlay.classList.remove('show');
    const safeIp=ip.replace(/[^0-9a-zA-Z._-]/g,'_');
    if(mode==='download'){
      const link=document.createElement('a');
      link.download='prettyscan_'+safeIp+'_'+Date.now()+'.png';
      link.href=canvas.toDataURL('image/png');link.click();
      toast(T[lang].downloaded+' — '+ip);
    }else{
      canvas.toBlob(async blob=>{
        try{await navigator.clipboard.write([new ClipboardItem({'image/png':blob})]);toast(T[lang].copied+' — '+ip);}
        catch(e){const link=document.createElement('a');link.download='prettyscan_'+safeIp+'_'+Date.now()+'.png';link.href=canvas.toDataURL('image/png');link.click();toast(T[lang].clipFail,false);}
      },'image/png');
    }
  }catch(e){actions.forEach(a=>a.style.visibility='visible');overlay.classList.remove('show');}
}

async function run(){
  const t=document.getElementById('tgt').value.trim();
  const o=document.getElementById('opt').value.trim();
  if(!t){err(T[lang].errEmpty);return}
  document.getElementById('bsc').disabled=true;
  document.getElementById('res').style.display='none';
  document.getElementById('eb').style.display='none';
  document.getElementById('loader').style.display='block';
  const msgs=T[lang].loaderMsgs;
  let mi=0,iv=setInterval(()=>{document.getElementById('lt').textContent=msgs[mi++%msgs.length]},1800);
  try{
    const r=await fetch('/scan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:t,options:o})});
    const d=await r.json();
    clearInterval(iv);document.getElementById('loader').style.display='none';document.getElementById('bsc').disabled=false;
    if(d.error){err(d.error);return}
    window._lastData=d;render(d);
  }catch(e){
    clearInterval(iv);document.getElementById('loader').style.display='none';document.getElementById('bsc').disabled=false;
    err(T[lang].errConn);
  }
}

function render(d){
  const t=T[lang];
  document.getElementById('st').textContent='📅 '+new Date().toLocaleString(lang==='es'?'es-ES':'en-GB')+' | '+t.scanLabel+d.target;
  const op=d.hosts.reduce((a,h)=>a+(h.ports?.filter(p=>p.state==='open').length||0),0);
  document.getElementById('sg').innerHTML=[
    {v:d.hosts.filter(h=>h.state==='up').length,l:t.statActive,c:'var(--ok)'},
    {v:d.hosts.length,l:t.statTotal,c:'var(--a)'},
    {v:op,l:t.statOpen,c:'var(--warn)'},
    {v:d.duration+'s',l:t.statDur,c:'var(--mt)'}
  ].map(s=>`<div class="sc"><div class="sv" style="color:${s.c}">${s.v}</div><div class="sl">${s.l}</div></div>`).join('');
  document.getElementById('txt-hosts-title').textContent=t.hostsTitle;
  const hc=document.getElementById('hc');
  hc.innerHTML=d.hosts.length?'':` <p style="color:var(--mt);text-align:center;padding:2rem">${t.noHosts}</p>`;
  d.hosts.forEach((h,i)=>{
    const cardId='hcard-'+i;
    const stTag=h.state==='up'?`<span class="tag up">${t.online}</span>`:`<span class="tag dn">${t.offline}</span>`;
    const os=h.os?`<span class="tag os">💻 ${h.os}</span>`:'';
    const hn=h.hostname?`<span style="color:var(--mt);font-size:.85rem">${h.hostname}</span>`:'';
    const dcBadge=h.is_dc?`<span class="tag dc">🏛 DC${h.domain?' · '+h.domain:''}</span>`:'';
    const actions=`<div class="card-actions">
      <button class="card-btn" onclick="exportCard('${cardId}','download','${h.ip}')">⬇ <span class="txt-img-btn">${t.imgBtn}</span></button>
      <button class="card-btn copy" onclick="exportCard('${cardId}','copy','${h.ip}')">📋 <span class="txt-copy-btn">${t.copyBtn}</span></button>
    </div>`;
    let pt='';
    if(h.ports&&h.ports.length){
      const hasScripts=h.ports.some(p=>p.scripts&&p.scripts.length>0);
      pt=`<div class="pw"><table class="pt">
        <thead><tr>
          <th>${t.thPort}</th><th>${t.thProto}</th><th>${t.thState}</th>
          <th>${t.thSvc}</th><th>${t.thVer}</th><th>${t.thRisk}</th>
          ${hasScripts?`<th>${t.thScripts}</th>`:''}
        </tr></thead>
        <tbody>${h.ports.map(p=>{
          const scriptsHtml=(p.scripts&&p.scripts.length&&hasScripts)
            ?`<td><div class="scripts-cell">${p.scripts.map(s=>`<span class="script-id">${s.id}</span><span class="script-out">${s.output}</span>`).join('')}</div></td>`
            :(hasScripts?'<td>-</td>':'');
          return`<tr>
            <td>${p.port}</td><td>${p.protocol||'tcp'}</td>
            <td class="${p.state}">${stateLabel(p.state)}</td>
            <td>${p.service||'-'}</td>
            <td style="color:var(--mt)">${p.version||'-'}</td>
            <td>${risk(p.port)}</td>
            ${scriptsHtml}
          </tr>`;
        }).join('')}</tbody>
      </table></div>`;
    }
    const div=document.createElement('div');
    div.className='hcard';div.id=cardId;
    div.innerHTML=`<div class="hh"><div><div class="hip">${h.ip}</div>${hn}</div><div class="hi">${stTag}${os}${dcBadge}<span style="color:var(--mt);font-size:.8rem">${h.ports?h.ports.length:0} <span class="txt-ports">${t.ports}</span></span>${actions}</div></div>${pt}`;
    hc.appendChild(div);
  });
  document.getElementById('res').style.display='block';
  document.getElementById('res').scrollIntoView({behavior:'smooth'});
}

['tgt','opt'].forEach(id=>document.getElementById(id).addEventListener('keydown',e=>{if(e.key==='Enter')run()}));
</script>
</body>
</html>"""


def parse_xml(xml):
    # AD/DC indicator ports
    AD_PORTS = {'88', '389', '636', '3268', '3269', '464'}

    hosts = []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return hosts

    for h in root.findall('host'):
        st = h.find('status')
        state = st.get('state', 'unknown') if st is not None else 'unknown'

        ip = ''
        for a in h.findall('address'):
            if a.get('addrtype') == 'ipv4':
                ip = a.get('addr', '')

        hostname = ''
        hns = h.find('hostnames')
        if hns is not None:
            hn = hns.find('hostname')
            if hn is not None:
                hostname = hn.get('name', '')

        os_name = ''
        os_el = h.find('os')
        if os_el is not None:
            osm = os_el.find('osmatch')
            if osm is not None:
                os_name = osm.get('name', '')

        ports = []
        open_port_ids = set()
        pe = h.find('ports')
        if pe is not None:
            for p in pe.findall('port'):
                pid = p.get('portid')
                proto = p.get('protocol', 'tcp')
                sp2 = p.find('state')
                pstate = sp2.get('state', '') if sp2 is not None else ''

                if pstate == 'open':
                    open_port_ids.add(pid)

                # --- Version: build full string from all service attributes ---
                svc = p.find('service')
                service = version = ''
                if svc is not None:
                    service = svc.get('name', '')
                    parts = []
                    for attr in ('product', 'version', 'extrainfo', 'ostype'):
                        val = svc.get(attr, '').strip()
                        if val:
                            parts.append(val)
                    version = ' '.join(parts)

                # --- Scripts: collect key/value from each script element ---
                scripts = []
                for script in p.findall('script'):
                    sid = script.get('id', '')
                    sout = script.get('output', '').strip()
                    if sid and sout:
                        # Truncate very long outputs for display
                        if len(sout) > 200:
                            sout = sout[:200] + '…'
                        scripts.append({'id': sid, 'output': sout})

                ports.append({
                    'port': pid,
                    'protocol': proto,
                    'state': pstate,
                    'service': service,
                    'version': version,
                    'scripts': scripts
                })

        # --- Detect Active Directory / Domain Controller ---
        is_dc = bool(open_port_ids & AD_PORTS)
        domain = ''
        if is_dc and hostname:
            # Extract domain from hostname e.g. dc01.manager.htb -> manager.htb
            parts = hostname.split('.')
            if len(parts) >= 2:
                domain = '.'.join(parts[1:])

        hosts.append({
            'ip': ip,
            'hostname': hostname,
            'state': state,
            'os': os_name,
            'ports': ports,
            'is_dc': is_dc,
            'domain': domain
        })
    return hosts


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target = data.get('target', '').strip()
    options = data.get('options', '-sV').strip()
    if not target:
        return jsonify({'error': 'Target vacío / Empty target'}), 400
    for ch in [';', '&&', '||', '`', '$', '|', '>', '<']:
        if ch in target or ch in options:
            return jsonify({'error': f'Carácter no permitido / Character not allowed: {ch}'}), 400
    cmd = ['nmap', '-oX', '-'] + options.split() + [target]
    t0 = datetime.datetime.now()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except FileNotFoundError:
        return jsonify({'error': 'Scan engine not found. Install: sudo apt install nmap'}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout >3min. Reduce port range.'}), 500
    duration = round((datetime.datetime.now() - t0).total_seconds(), 1)
    if proc.returncode not in (0, 1):
        return jsonify({'error': proc.stderr or 'Scan error'}), 500
    hosts = parse_xml(proc.stdout)
    return jsonify({'target': target, 'options': options, 'duration': duration, 'hosts': hosts})


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  PrettyScan — Visual Network Framework")
    print("  → http://localhost:5000")
    print("  → Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(debug=False, host='127.0.0.1', port=5000)
