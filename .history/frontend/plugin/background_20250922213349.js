/**
 * Jarvis Guardian - Background Service Worker
 *
 * This script runs in the background and acts as the central brain for the extension.
 * It listens for navigation events, communicates with the backend AI, and takes action.
 */

// 1. THE LISTENER: This function runs every time a tab is updated.
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // We only want to act when a new URL is loading in the main frame.
  // This prevents it from firing on sub-frames or for non-webpage URLs.
  if (changeInfo.status === 'loading' && changeInfo.url && changeInfo.url.startsWith('http')) {
    
    console.log(`Checking URL: ${changeInfo.url}`);

    // 2. THE API CALL: Send the detected URL to the Python backend for analysis.
    fetch("http://127.0.0.1:5000/analyze/url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: changeInfo.url })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("URL Analysis:", data); // Log the full analysis from the backend.

      // 3. THE ACTION: If the backend says the URL is malicious, take action.
      if (data.result === "malicious") {
        
        // ACTION 1: Block the site by redirecting the user's tab immediately.
        chrome.tabs.update(tabId, { url: data.redirect_url });

        // ACTION 2: Show a notification to inform the user what happened.
        // IMPORTANT: Make sure you have a folder named 'images' inside your 'plugin'
        // folder, and an icon named 'icon128.png' inside it.
        chrome.notifications.create({
          type: "basic",
          iconUrl: "images/icon128.png",
          title: "⚠️ Jarvis Guardian Alert",
          message: `Malicious site blocked! Redirecting you to safety.\nReason: ${data.reasons.join(", ")}`
        });
      }
    })
    .catch(err => {
      console.error("Jarvis Guardian Error: Could not connect to the backend server. Is it running?", err);
    });
  }
});

// A small listener to log when the extension is installed or updated.
chrome.runtime.onInstalled.addListener(() => {
  console.log("Jarvis Guardian extension installed successfully.");
});