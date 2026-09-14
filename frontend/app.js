const api='/api';
let lat=27.53, lon=68.76;
let latestWeather=null, latestDischarge=null, latestAdvisory=null, latestFlood=null, latestRecovery=null;
const $=s=>document.querySelector(s);
const $$=s=>[...document.querySelectorAll(s)];

const map=L.map('map',{zoomControl:true}).setView([lat,lon],8);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap contributors',maxZoom:19}).addTo(map);
const marker=L.circleMarker([lat,lon],{radius:7,color:'#fff',weight:2,fillColor:'#18d17c',fillOpacity:1}).addTo(map).bindPopup("Khairpur Mir's study point").openPopup();
map.on('click',e=>{lat=e.latlng.lat;lon=e.latlng.lng;marker.setLatLng(e.latlng); $('#mapDataNote').textContent=`Selected advisory coordinate: ${lat.toFixed(4)}, ${lon.toFixed(4)}`;});

function dateLabel(){
  const d=new Date(); $('#todayLabel').textContent=d.toLocaleDateString('en-GB',{weekday:'short',day:'2-digit',month:'short',year:'numeric'});
}
dateLabel();

async function j(url,opt){const r=await fetch(url,opt);let d={};try{d=await r.json()}catch{} if(!r.ok)throw new Error(d.detail||r.statusText||'Request failed');return d;}
function fmt(v,d=1){return Number.isFinite(Number(v))?Number(v).toFixed(d):'—'}
function weatherIcon(code){if(code===0)return'☀️';if([1,2].includes(code))return'🌤️';if(code===3)return'☁️';if([45,48].includes(code))return'🌫️';if([51,53,55,56,57,61,63,65,66,67,80,81,82].includes(code))return'🌧️';if([71,73,75,77,85,86].includes(code))return'🌨️';if([95,96,99].includes(code))return'⛈️';return'☁️'}
function weatherText(code){if(code===0)return'Clear sky';if([1,2].includes(code))return'Partly cloudy';if(code===3)return'Overcast';if([45,48].includes(code))return'Fog';if([51,53,55,56,57].includes(code))return'Drizzle';if([61,63,65,66,67,80,81,82].includes(code))return'Rain';if([71,73,75,77,85,86].includes(code))return'Snow';if([95,96,99].includes(code))return'Thunderstorm';return'Weather data'}

async function loadHealth(){
  try{const h=await j(api+'/health'); $('#geeStatus').textContent=h.gee_configured?'GEE configured':'GEE not configured'; $('#geeStatus').style.color=h.gee_configured?'#80efb0':'#eacb77';}
  catch{$('#geeStatus').textContent='API unavailable'}
}
loadHealth();

async function loadWeatherAndAdvisory(){
  $('#fetchBtn').disabled=true; $('#fetchBtn').textContent='Loading…';
  try{
    const [w,d]=await Promise.all([j(`${api}/weather?lat=${lat}&lon=${lon}`),j(`${api}/discharge?lat=${lat}&lon=${lon}`)]);
    latestWeather=w; latestDischarge=d;
    const req={latitude:lat,longitude:lon,rainfall_24h_mm:w.rainfall_24h_mm,rainfall_72h_mm:w.rainfall_72h_mm,discharge_m3s:d.river_discharge_m3s,discharge_baseline_m3s:null};
    const a=await j(api+'/advisory',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(req)}); latestAdvisory=a;
    renderWeather(w); renderAdvisory(a,d); renderKpis();
  }catch(e){$('#advisoryBox').textContent='Current providers unavailable: '+e.message; $('#qualityPill').textContent='Provider error';}
  finally{$('#fetchBtn').disabled=false; $('#fetchBtn').textContent='Refresh data';}
}
$('#fetchBtn').onclick=loadWeatherAndAdvisory; $('#weatherRefresh').onclick=loadWeatherAndAdvisory;

function renderWeather(w){
  const raw=w.raw||{}; const current=raw.current||{}; const daily=raw.daily||{};
  const code=Number(current.weather_code); const icon=weatherIcon(code); const desc=weatherText(code);
  $('#weatherBigIcon').textContent=icon; $('#weatherIcon').textContent=icon;
  $('#tempNow').textContent=current.temperature_2m!=null?`${Math.round(current.temperature_2m)}°C`:'—';
  $('#topTemp').textContent=current.temperature_2m!=null?`${Math.round(current.temperature_2m)}°C`:'—'; $('#topWeatherText').textContent=desc;
  $('#weatherDesc').textContent=desc; $('#humidityNow').textContent=current.relative_humidity_2m!=null?`${current.relative_humidity_2m}%`:'—';
  $('#windNow').textContent=current.wind_speed_10m!=null?`${fmt(current.wind_speed_10m,1)} km/h`:'—'; $('#rainNow').textContent=`${fmt(w.rainfall_24h_mm,1)} mm`;
  $('#kpiRain').textContent=fmt(w.rainfall_24h_mm,1);
  const days=(daily.time||[]).slice(0,5); let html='';
  days.forEach((date,i)=>{const dc=Number((daily.weather_code||[])[i]); const hi=(daily.temperature_2m_max||[])[i]; const lo=(daily.temperature_2m_min||[])[i]; const day=new Date(date+'T12:00:00').toLocaleDateString('en-GB',{weekday:'short'}); html+=`<div class="forecast-day"><strong>${day}</strong><span>${weatherIcon(dc)}</span><b>${hi==null?'—':Math.round(hi)+'°'}</b><small>${lo==null?'—':Math.round(lo)+'°'}</small></div>`});
  $('#forecastRow').innerHTML=html||'<div class="forecast-empty">Forecast fields unavailable from provider.</div>';
}

function renderAdvisory(a,d){
  const state=a.state||'Unknown/Insufficient Data'; $('#kpiRisk').textContent=state.replace('/Insufficient Data',''); $('#riskDonutValue').textContent=state==='Unknown/Insufficient Data'?'?':state;
  $('#kpiRiskNote').textContent=a.reasons?.[0]||'Experimental advisory'; $('#qualityPill').textContent=a.input_quality||'Unknown quality';
  const badge=$('#riskBadge'); badge.textContent=a.score==null?'—':`Score ${a.score}`; badge.className='kpi-badge '+(state==='High'?'bad':state==='Medium'?'warn':state==='Low'?'good':'neutral');
  const colors=state==='High'?['#ff4d4f','#5f3940']:state==='Medium'?['#ffb62e','#5b5633']:state==='Low'?['#2fd48b','#226454']:['#607d7e','#395153'];
  $('#riskDonut').style.background=`conic-gradient(${colors[0]} 0 ${a.score??35}%,${colors[1]} ${a.score??35}% 100%)`;
  $('#riskHigh').textContent=state==='High'?'Triggered':'Not triggered'; $('#riskMedium').textContent=state==='Medium'?'Triggered':'—'; $('#riskLow').textContent=state==='Low'?'Current state':'—';
  $('#dischargeValue').textContent=d.river_discharge_m3s==null?'—':`${fmt(d.river_discharge_m3s,1)} m³/s`;
  $('#advisoryBox').innerHTML=`<b>${state}</b><br>${(a.reasons||[]).map(x=>escapeHtml(x)).join('<br>')}<br><span style="color:#7ea29a">Experimental rule · not a calibrated flood probability.</span>`;
}

function renderKpis(){
  if(latestRecovery?.status==='ok'){$('#kpiNdvi').textContent=fmt(latestRecovery.recovery_ndvi,2); const delta=latestRecovery.ndvi_change; $('#ndviBadge').textContent=(delta>=0?'+':'')+fmt(delta,2); $('#ndviBadge').className='kpi-badge '+(delta>=0?'good':'warn');}
  if(latestFlood?.status==='ok'){$('#kpiCropExposure').textContent=fmt(latestFlood.potentially_affected_cropland_km2,1);}
}

async function loadAlerts(){
  try{const rows=await j(api+'/alerts'); const active=rows.filter(x=>x.active); $('#notifDot').style.display=active.length?'block':'none';
    $('#recentAlerts').innerHTML=active.length?active.slice(0,5).map(alertHtml).join(''):'<div class="empty-state">No active alerts yet.</div>'; return rows;
  }catch(e){$('#recentAlerts').innerHTML=`<div class="empty-state">Alerts unavailable: ${escapeHtml(e.message)}</div>`; return []}
}
function alertHtml(a){const cls=a.state.startsWith('Unknown')?'unknown':a.state.toLowerCase(); const icon=a.state==='High'?'!':a.state==='Medium'?'⚠':a.state==='Low'?'✓':'?'; return `<div class="alert-row"><div class="alert-icon">${icon}</div><div><strong>${escapeHtml(a.reason)}</strong><p>${escapeHtml(a.location)}</p><small>${escapeHtml(a.source_date)} · ${escapeHtml(a.quality)}${a.simulated?' · SIMULATED':''}</small></div><span class="state-chip ${cls}">${escapeHtml(a.state)}</span></div>`}
loadAlerts();

$('#runFlood').onclick=async()=>{
  const btn=$('#runFlood'); btn.disabled=true; btn.textContent='Running Sentinel-1…'; $('#scienceMessage').textContent='Processing Earth Engine request…';
  try{const d=await j(api+'/jobs/flood',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({district:'Khairpur',before_start:'2022-06-01',before_end:'2022-07-15',after_start:'2022-08-25',after_end:'2022-09-03',orbit_pass:'DESCENDING',polarization:'VH'})}); latestFlood=d; renderFlood(d); renderKpis();}
  catch(e){$('#scienceMessage').textContent=e.message;}
  finally{btn.disabled=false; btn.textContent='Run Sentinel-1 flood job';}
};
function renderFlood(d){if(d.status==='empty'){$('#scienceMessage').textContent=`No matching Sentinel-1 scenes. Before: ${d.before_scenes}, after: ${d.after_scenes}.`;return} $('#floodExtent').textContent=`${fmt(d.flood_km2,1)} km²`; $('#cropFloodExtent').textContent=`${fmt(d.potentially_affected_cropland_km2,1)} km²`; $('#sceneCount').textContent=`${d.before_scenes}+${d.after_scenes}`; $('#mapDataNote').textContent='Scientific flood summary loaded. Raster display requires Earth Engine map-tile integration.'; $('#scienceMessage').textContent=`Experimental result generated from Sentinel-1 change detection; permanent water and slope filters applied.`;}

$('#runRecovery').onclick=async()=>{
  const btn=$('#runRecovery'); btn.disabled=true; btn.textContent='Running…';
  try{const d=await j(api+'/jobs/recovery',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({district:'Khairpur',baseline_start:'2021-08-15',baseline_end:'2021-10-15',recovery_start:'2022-10-15',recovery_end:'2022-12-15',cloud_probability_max:40})}); latestRecovery=d; renderRecovery(d); renderKpis();}
  catch(e){$('#ndviChart').innerHTML=`<div class="chart-placeholder">${escapeHtml(e.message)}</div>`;}
  finally{btn.disabled=false; btn.textContent='Run GEE recovery →';}
};
function renderRecovery(d){if(d.status==='empty'){$('#ndviChart').innerHTML=`<div class="chart-placeholder">No matching Sentinel-2 scenes. Baseline: ${d.baseline_scenes}; recovery: ${d.recovery_scenes}.</div>`;return} $('#baselineNdvi').textContent=fmt(d.baseline_ndvi,3); $('#recoveryNdvi').textContent=fmt(d.recovery_ndvi,3); $('#ndviChange').textContent=(d.ndvi_change>=0?'+':'')+fmt(d.ndvi_change,3); const b=Number(d.baseline_ndvi),r=Number(d.recovery_ndvi); const y=v=>120-(Math.max(0,Math.min(1,v))*100); $('#ndviChart').innerHTML=`<svg class="ndvi-svg" viewBox="0 0 420 145" preserveAspectRatio="none"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#48e58e" stop-opacity=".42"/><stop offset="1" stop-color="#48e58e" stop-opacity="0"/></linearGradient></defs><g stroke="#234f50" stroke-width="1" opacity=".6"><line x1="35" y1="25" x2="405" y2="25"/><line x1="35" y1="72" x2="405" y2="72"/><line x1="35" y1="120" x2="405" y2="120"/></g><path d="M70 ${y(b)} C150 ${y((b+r)/2-.04)},270 ${y((b+r)/2+.03)},360 ${y(r)} L360 120 L70 120 Z" fill="url(#g)"/><path d="M70 ${y(b)} C150 ${y((b+r)/2-.04)},270 ${y((b+r)/2+.03)},360 ${y(r)}" fill="none" stroke="#7bf2a9" stroke-width="3"/><circle cx="70" cy="${y(b)}" r="5" fill="#fff" stroke="#41dc87" stroke-width="2"/><circle cx="360" cy="${y(r)}" r="5" fill="#fff" stroke="#41dc87" stroke-width="2"/><text x="48" y="140" font-size="10" fill="#83a69f">Baseline</text><text x="336" y="140" font-size="10" fill="#83a69f">Recovery</text></svg>`;}

$('#loadHistory').onclick=()=>navigateTo('history');
$('#backDashboard').onclick=()=>navigateTo('dashboard');
$$('[data-view-jump]').forEach(b=>b.onclick=()=>navigateTo(b.dataset.viewJump));
$$('.side-link').forEach(b=>b.onclick=()=>navigateTo(b.dataset.view));

function setDashboardVisible(visible){
  ['.hero-panel','.kpi-grid','.dashboard-grid'].forEach(sel=>{
    const el=$(sel); if(!el) return;
    el.classList.toggle('hidden',!visible);
    el.style.display=visible?'':'none';
  });
  const detail=$('#detailView');
  if(detail){detail.classList.toggle('hidden',visible);detail.style.display=visible?'none':'block';}
}

function navigateTo(view){
  const target=view||'dashboard';
  $$('.side-link').forEach(x=>x.classList.toggle('active',x.dataset.view===target));
  if(target==='dashboard'){
    showDashboard();
  }else{
    openDetail(target);
  }
  if(location.hash!==`#${target}`) history.replaceState(null,'',`#${target}`);
}

function showDashboard(){
  setDashboardVisible(true);
  window.scrollTo({top:0,behavior:'smooth'});
  setTimeout(()=>map.invalidateSize(),100);
}

function metric(label,value,note=''){
  return `<div class="detail-metric"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong>${note?`<small>${escapeHtml(note)}</small>`:''}</div>`;
}

async function openDetail(view){
  setDashboardVisible(false);
  window.scrollTo({top:0,behavior:'smooth'});
  const titleMap={flood:'Flood Risk Map',crop:'Crop Monitoring',weather:'Weather & Forecast',history:'Historical Data',reports:'Reports',alerts:'Advisories',settings:'Settings'};
  $('#detailTitle').textContent=titleMap[view]||'Details';
  const c=$('#detailContent');
  c.innerHTML='<div class="empty-state">Loading…</div>';
  try{
    if(view==='weather'){
      if(!latestWeather) await loadWeatherAndAdvisory();
      const raw=latestWeather?.raw||{}, cur=raw.current||{};
      c.innerHTML=`<div class="detail-grid">${metric('Temperature',cur.temperature_2m!=null?Math.round(cur.temperature_2m)+'°C':'—','Current Open-Meteo value')}${metric('Rainfall (24h)',latestWeather?fmt(latestWeather.rainfall_24h_mm,1)+' mm':'—')}${metric('Rainfall (72h)',latestWeather?fmt(latestWeather.rainfall_72h_mm,1)+' mm':'—')}${metric('Humidity',cur.relative_humidity_2m!=null?cur.relative_humidity_2m+'%':'—')}</div><div class="report-note">Weather data is sourced from Open-Meteo. It provides forecast/advisory context only and is not proof of future flooding.</div>`;
    }
    else if(view==='crop'){
      c.innerHTML=`<div class="detail-grid">${metric('Baseline NDVI',latestRecovery?.status==='ok'?fmt(latestRecovery.baseline_ndvi,3):'—')}${metric('Recovery NDVI',latestRecovery?.status==='ok'?fmt(latestRecovery.recovery_ndvi,3):'—')}${metric('NDVI change',latestRecovery?.status==='ok'?(latestRecovery.ndvi_change>=0?'+':'')+fmt(latestRecovery.ndvi_change,3):'—')}${metric('Data source','Sentinel-2','Cloud-screened observations')}</div><div class="report-note">Crop monitoring uses Sentinel-2 NDVI as a vegetation recovery indicator. Configure Google Earth Engine and run the recovery job to populate real results.</div>`;
    }
    else if(view==='flood'){
      c.innerHTML=`<div class="detail-grid">${metric('Flood extent',latestFlood?.status==='ok'?fmt(latestFlood.flood_km2,1)+' km²':'—')}${metric('Potential crop exposure',latestFlood?.status==='ok'?fmt(latestFlood.potentially_affected_cropland_km2,1)+' km²':'—')}${metric('Scenes used',latestFlood?.status==='ok'?`${latestFlood.before_scenes}+${latestFlood.after_scenes}`:'—')}${metric('Data source','Sentinel-1 SAR','Before/after change detection')}</div><div class="report-note">Flood mapping uses Sentinel-1 change detection with permanent-water and slope filtering. Configure Google Earth Engine and run the flood job to populate real scientific results.</div>`;
    }
    else if(view==='history'){
      const d=await j(api+'/historical-replay');
      c.innerHTML=`<div class="report-note"><b>${escapeHtml(d.event)}</b><br>${escapeHtml(d.selection_reason||'')}</div>${(d.observations||[]).map(o=>`<div class="history-item"><strong>${escapeHtml(o.date)}</strong><p>${escapeHtml(o.summary)}</p><small>${escapeHtml(o.sensor||'Reference')}</small></div>`).join('')}`;
    }
    else if(view==='alerts'){
      const rows=await loadAlerts();
      c.innerHTML=rows.length?rows.map(alertHtml).join(''):'<div class="empty-state">No alerts currently available.</div>';
    }
    else if(view==='reports'){
      const advisoryState=latestAdvisory?.state||'Unknown/Insufficient Data';
      c.innerHTML=`<div class="detail-grid">${metric('Current advisory',advisoryState)}${metric('Flood mapping',latestFlood?.status==='ok'?'Result available':'Not yet run')}${metric('Crop recovery',latestRecovery?.status==='ok'?'Result available':'Not yet run')}${metric('Validation','Pending','Precision / Recall / F1 / IoU after reference comparison')}</div><div class="report-note">Research reporting must keep software correctness separate from scientific accuracy. No scientific metric is shown until a suitable time-matched reference map is available.</div>`;
    }
    else if(view==='settings'){
      const h=await j(api+'/health');
      c.innerHTML=`<div class="settings-grid"><div><span>Backend</span><b>${escapeHtml(h.status)}</b></div><div><span>Google Earth Engine</span><b>${h.gee_configured?'Configured':'Not configured'}</b></div><div><span>Study area</span><b>Khairpur District, Sindh</b></div><div><span>System status</span><b>Academic prototype</b></div></div>`;
    }
  }catch(e){
    c.innerHTML=`<div class="empty-state">${escapeHtml(e.message)}</div>`;
  }
}

window.addEventListener('hashchange',()=>navigateTo(location.hash.slice(1)||'dashboard'));
const initialView=(location.hash||'#dashboard').slice(1);
navigateTo(['dashboard','flood','crop','weather','history','reports','alerts','settings'].includes(initialView)?initialView:'dashboard');
function escapeHtml(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

loadWeatherAndAdvisory();
