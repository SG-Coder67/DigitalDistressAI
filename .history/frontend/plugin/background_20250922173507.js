chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (!changeInfo.url) return;

  fetch("http://127.0.0.1:5000/analyze/url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input: changeInfo.url })
  })
    .then(res => res.json())
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
