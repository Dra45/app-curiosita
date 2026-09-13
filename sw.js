self.addEventListener('install', (e) => {
  console.log('Service Worker Installato');
});

self.addEventListener('fetch', (e) => {
  // Gestione offline di base
});