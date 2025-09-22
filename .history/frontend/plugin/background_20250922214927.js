/**
 * Jarvis Guardian - Background Service Worker
 *
 * Final version. This script listens for navigation, communicates with the
 * backend, and correctly blocks malicious sites while showing a notification.
 */

// 1. LISTENER: This function runs every time a tab is updated.
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // We only act when a new URL is fully loading in the main browser tab.
  // This ignores internal browser URLs and prevents the code from running multiple times.
  if (changeInfo.status === 'loading' && changeInfo.url && changeInfo.url.startsWith('http')) {
    
    console.log(`Jarvis is checking URL: ${changeInfo.url}`);

    // 2. API CALL: Send the detected URL to the Python backend for analysis.
    fetch("http://127.0.0.1:5000/analyze/url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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

      // 3. ACTION: If the backend confirms the URL is malicious, take action.
      if (data.result === "malicious") {
        
        // ACTION 1: SHOW THE NOTIFICATION FIRST
        // The custom icon is removed to prevent errors. The browser will use a default icon.
        // This guarantees the popup will appear.
        chrome.notifications.create({
          type: "basic",
          title: "⚠️ Jarvis Guardian Alert",
          message: `Malicious site blocked! Redirecting you to safety.\nReason: ${data.reasons.join(", ")}`
        });
        
        // ACTION 2: BLOCK THE SITE BY REDIRECTING
        // This happens immediately after the notification is created.
        chrome.tabs.update(tabId, { url: data.redirect_url });
      }
    })
    .catch(err => {
      // This will catch any network errors (like the server being down).
      console.error("Jarvis Guardian Error:", err);
    });
  }
});

// A listener to confirm that the extension has been installed or updated.
chrome.runtime.onInstalled.addListener(() => {
  console.log("Jarvis Guardian extension is active.");
});