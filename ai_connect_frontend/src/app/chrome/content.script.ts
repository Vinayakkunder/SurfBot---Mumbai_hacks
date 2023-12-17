// chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//     if (tabs.length > 0) {
//       const currentUrl = tabs[0].url;
//       console.log('Current URL:', currentUrl);
//       // Use `currentUrl` in your Angular app logic
//     } else {
//       console.error('No active tab found!');
//     }
//   });
  
// content.script.ts

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  if (tabs.length > 0) {
    const currentUrl = tabs[0].url;
    console.log('Current URL:', currentUrl);

    // Send message to Angular app
    chrome.runtime.sendMessage({ message: 'url', data: currentUrl });
  } else {
    console.error('No active tab found!');
  }
});
