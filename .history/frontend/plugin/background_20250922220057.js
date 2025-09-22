/**
 * Jarvis Guardian - Background Service Worker
 *
 * Final version. This script correctly sends the JSON key 'url' to the backend,
 * blocks malicious sites, and shows a working notification.
 */

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'loading' && changeInfo.url && changeInfo.url.startsWith('http')) {
    
    console.log(`Jarvis is checking URL: ${changeInfo.url}`);

    fetch("http://127.0.0.1:5000/analyze/url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // --- THIS IS THE FIX ---
      // The key is now "url" to match what the Python server expects.
      body: JSON.stringify({ url: changeInfo.url })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Backend returned an error. Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("Backend Analysis:", data);

      if (data.result === "malicious") {
        
        // ACTION 1: Show notification first
        chrome.notifications.create({
          type: "basic",
          title: "⚠️ Jarvis Guardian Alert",
          message: `Malicious site blocked! Redirecting you to safety.\nReason: ${data.reasons.join(", ")}`
        });
        
        // ACTION 2: Redirect the tab
        chrome.tabs.update(tabId, { url: data.redirect_url });
      }
    })
    .catch(err => {
      console.error("Jarvis Guardian Error:", err);
    });
  }
});

chrome.runtime.onInstalled.addListener(() => {
  console.log("Jarvis Guardian extension is active.");
});