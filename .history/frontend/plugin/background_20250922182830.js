// Optional whitelist of safe domains to ignore
const whitelist = ["google.com", "youtube.com", "github.com"];

chrome.webNavigation.onCommitted.addListener((details) => {
  if (details.frameId !== 0) return; // only main frame
  const url = details.url;

  if (!url) return;
  if (whitelist.some(domain => url.includes(domain))) return;

  // Send URL to backend for analysis
  fetch("http://127.0.0.1:5000/analyze/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input: url })
  })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => {
      if (data.result === "malicious") {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: "⚠️ Jarvis Guardian Alert",
          message: `Blocked malicious site!\nReason: ${data.reasons.join(", ")}`
        });
      }
    })
    .catch(err => console.error("Error connecting to backend:", err));
});
