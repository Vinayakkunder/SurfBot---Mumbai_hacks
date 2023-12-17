// sw.js

// Register service worker
navigator.serviceWorker.register('sw.js').then(() => {
    console.log('Service worker registered!');
  }).catch((error) => {
    console.error('Error registering service worker:', error);
  });
  
  // Handle installation event
  self.addEventListener('install', (event) => {
    console.log('Service worker installed!');
    // Add logic for caching or pre-fetching resources
  });
  
  // Handle activation event
  self.addEventListener('activate', (event) => {
    console.log('Service worker activated!');
    // Add logic for activating new service worker and handling updates
  });
  