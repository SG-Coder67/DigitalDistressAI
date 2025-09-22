/**
 * Jarvis Guardian - Background Service Worker
 *
 * This script runs in the background for the extension. It's responsible for
 * listening to browser events, communicating with the backend AI for analysis,
 * and taking protective actions like blocking sites and notifying the user.
 */

// 1. LISTENER: This function runs every time a tab is updated.
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // We only act when a new URL is fully loading in the main browser tab.
  // This prevents the code from running multiple times or on background frames.
  // It also ignores internal browser URLs like 'chrome://extensions'.
  if (changeInfo.status === 'loading' && changeInfo.url && changeInfo.url.startsWith('http')) {
    
    console.log(`Jarvis is checking URL: ${changeInfo.url}`);

    // 2. API CALL: Send the detected URL to the Python backend for analysis.
    fetch("http://127.0.0.1:5000/analyze/url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: changeInfo.url })
    })
    .then(response => {
      if (!response.ok) {
        // If the server returns an error (like 400 or 500), this will be triggered.
        throw new Error(`Backend returned an error. Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("Backend Analysis:", data);

      // 3. ACTION: If the backend confirms the URL is malicious, take action.
      if (data.result === "malicious") {
  
  // Create the notification
  chrome.notifications.create({
    type: "basic",
    iconUrl: "images/icon128.png",
    title: "⚠️ Jarvis Guardian Alert",
    message: `Malicious site blocked!\nReason: ${data.reasons.join(", ")}`
  });
  
  // TEMPORARILY DISABLED FOR TESTING
  // chrome.tabs.update(tabId, { url: data.redirect_url }); 
}
    })
    .catch(err => {
      // This will catch any network errors (like the server being down)
      // or errors from the .then() blocks.
      console.error("Jarvis Guardian Error:", err);
    });
  }
});

// A listener to confirm that the extension has been installed or updated.
chrome.runtime.onInstalled.addListener(() => {
  console.log("Jarvis Guardian extension is active.");
});