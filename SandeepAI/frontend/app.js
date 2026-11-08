const $ = (id) => document.getElementById(id);
const messages = $('messages');
function addMessage(role, text) {
  const el = document.createElement('div'); el.className = `message ${role}`;
  const label = document.createElement('b'); label.textContent = role === 'user' ? 'You' : 'Sandeep AI';
  const p = document.createElement('p'); p.textContent = text;
  el.append(label, p); messages.append(el); messages.scrollTop = messages.scrollHeight;
}
async function api(url, options={}) {
  const response = await fetch(url, {headers:{'Content-Type':'application/json'}, ...options});
  const data = await response.json(); if (!response.ok) throw new Error(data.detail || 'Request failed'); return data;
}
async function sendMessage() {
  const input = $('prompt'), text = input.value.trim(); if (!text) return;
  input.value = ''; addMessage('user', text); $('send').disabled = true;
  try { const result = await api('/api/chat',{method:'POST',body:JSON.stringify({message:text})}); addMessage('assistant',result.reply); }
  catch(e){addMessage('assistant','Error: '+e.message)} finally {$('send').disabled=false;}
}
$('send').addEventListener('click',sendMessage);
$('prompt').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage();}});
async function refreshFiles(){const box=$('file-list');box.textContent='Loading…';try{const data=await api('/api/files');box.replaceChildren();if(!data.files.length){box.textContent='Workspace खाली है। अपनी project files workspace/projects में रखें।';return;}for(const f of data.files){const row=document.createElement('div');row.className='file-row';const name=document.createElement('span');name.textContent=`📄 ${f.path} · ${f.size} bytes`;const btn=document.createElement('button');btn.textContent='Read';btn.onclick=async()=>{try{const d=await api('/api/read-file',{method:'POST',body:JSON.stringify({path:f.path})});addMessage('assistant',`File: ${d.path}\n\n${d.content.slice(0,7000)}`);showPanel('chat');}catch(e){alert(e.message)}};row.append(name,btn);box.append(row);}}catch(e){box.textContent=e.message}}
$('refresh-files').onclick=refreshFiles;
function showPanel(name){$('chat-panel').classList.toggle('hidden',name!=='chat');$('files-panel').classList.toggle('hidden',name!=='files');$('page-title').textContent=name==='chat'?'AI Assistant':'Workspace Files';document.querySelectorAll('.nav').forEach(n=>n.classList.toggle('active',n.dataset.panel===name));if(name==='files')refreshFiles();}
document.querySelectorAll('.nav').forEach(n=>n.onclick=()=>showPanel(n.dataset.panel));
document.querySelectorAll('[data-action]').forEach(b=>b.onclick=async()=>{if(b.dataset.action==='files'){showPanel('files');return;}const url=prompt('कौन-सी website खोलनी है? (https://...)');if(!url)return;try{const r=await api('/api/open-site',{method:'POST',body:JSON.stringify({url})});addMessage('assistant',r.message)}catch(e){alert(e.message)}});
(async()=>{try{const s=await api('/api/status');$('connection').textContent=s.ai_connected?'Online AI key configured':'Local mode · API key not set';}catch{$('connection').textContent='Backend not connected'}})();
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if(SpeechRecognition){const rec=new SpeechRecognition();rec.lang='hi-IN';rec.interimResults=false;$('mic').onclick=()=>{rec.start();$('mic').textContent='Listening…'};rec.onresult=e=>{$('prompt').value=e.results[0][0].transcript;$('mic').textContent='🎙'};rec.onerror=()=>{$('mic').textContent='🎙'};rec.onend=()=>{$('mic').textContent='🎙'};}else{$('mic').disabled=true;$('mic').title='इस browser में voice recognition उपलब्ध नहीं है';}
