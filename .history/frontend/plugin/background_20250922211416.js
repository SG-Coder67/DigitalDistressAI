// Runs in the background for all tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (!changeInfo.url) return; // Only trigger on URL changes

  fetch("http://127.0.0.1:5000/analyze/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: changeInfo.url })
  })
    .then(res => res.json())
    .then(data => {
      console.log("URL Analysis:", data); // Logs result in console
      if (data.result === "malicious") {
        chrome.notifications.create({
          type: "basic",
          iconUrl: chrome.runtime.getURL("icon.png"), // Use extension icon if available
          title: "⚠️ Jarvis Guardian Alert",
          message: `Blocked malicious site!\nReason: ${data.reasons && data.reasons.length ? data.reasons.join(", ") : "Unknown"}`
        }, () => {
          // Fallback: If icon.png is missing, use Chrome's default icon
        });
      }
    })
    .catch(err => console.error("Error connecting to backend:", err));
});
