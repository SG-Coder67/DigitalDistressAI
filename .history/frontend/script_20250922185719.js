document.getElementById("checkBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value;
  const resultEl = document.getElementById("result");

  if (!url) {
    resultEl.innerText = "Please enter a URL.";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/analyze/url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await res.json();

    if (data.result === "malicious") {
      resultEl.innerHTML = `⚠️ Malicious URL detected!<br>Type: ${data.type}<br>Reasons: ${data.reasons.join(", ")}<br>Redirecting to a safe site...`;
      setTimeout(() => {
        window.location.href = data.redirect_url; // Redirect to safe site
      }, 3000); // 3-second delay
    } else {
      resultEl.innerHTML = "✅ URL is safe!";
    }
  } catch (err) {
    resultEl.innerText = "Error connecting to backend.";
    console.error(err);
  }
});
