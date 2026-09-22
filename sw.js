/* RETRODECK service worker — cache do app shell para uso offline.
   Só trafega com a mesma origem; nada de terceiros. */
const CACHE = 'retrodeck-v1';
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './favicon.svg',
  './favicon.ico',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', e=>{
  e.waitUntil(
    caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())
  );
});

self.addEventListener('activate', e=>{
  e.waitUntil(
    caches.keys()
      .then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))
      .then(()=>self.clients.claim())
  );
});

self.addEventListener('fetch', e=>{
  const req = e.request;
  if(req.method !== 'GET') return;
  const url = new URL(req.url);
  if(url.origin !== self.location.origin) return;   /* nunca pega terceiros */

  e.respondWith((async ()=>{
    /* navegações: rede primeiro (conteúdo fresco), cache como fallback offline */
    if(req.mode === 'navigate'){
      try{
        const fresh = await fetch(req);
        if(fresh && fresh.ok){
          const cp = fresh.clone();
          caches.open(CACHE).then(c=>c.put('./index.html', cp)).catch(()=>{});
        }
        return fresh;
      }catch(err){
        const cached = await caches.match('./index.html');
        if(cached) return cached;
        throw err;
      }
    }
    /* estáticos: cache primeiro, rede atualiza o cache */
    const hit = await caches.match(req, {ignoreSearch:true});
    if(hit) return hit;
    try{
      const res = await fetch(req);
      if(res && res.ok && res.status===200 && res.type==='basic'){
        const cp = res.clone();
        caches.open(CACHE).then(c=>c.put(req, cp)).catch(()=>{});
      }
      return res;
    }catch(err){
      throw err;
    }
  })());
});
