/* 분수의 나눗셈 실험실 — 오프라인 지원 서비스 워커
   교실 와이파이가 끊겨도 한 번 열어 본 기기에서는 앱이 계속 동작한다. */

const CACHE = 'fdlab-v2';
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon-180.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE)
      .then(function (c) { return c.addAll(SHELL); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(keys.filter(function (k) { return k !== CACHE; })
          .map(function (k) { return caches.delete(k); }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

function store(req, res) {
  if (!res) return;
  if (!res.ok && res.type !== 'opaque') return;
  const copy = res.clone();
  caches.open(CACHE).then(function (c) { c.put(req, copy); });
}

self.addEventListener('fetch', function (e) {
  const req = e.request;
  if (req.method !== 'GET') return;

  /* 페이지 요청 — 네트워크를 먼저 쓰고(항상 최신), 실패하면 캐시로 대체 */
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req)
        .then(function (res) { store('./index.html', res); return res; })
        .catch(function () { return caches.match('./index.html'); })
    );
    return;
  }

  /* 아이콘·구글 폰트 등 — 캐시를 먼저 쓰고, 없으면 받아서 저장 */
  e.respondWith(
    caches.match(req).then(function (hit) {
      if (hit) return hit;
      return fetch(req)
        .then(function (res) { store(req, res); return res; })
        .catch(function () { return new Response('', { status: 504, statusText: 'offline' }); });
    })
  );
});
