document.getElementById("checkBtn").addEventListener("click", async () => {
  const input = document.getElementById("userInput").value;
  const resultEl = document.getElementById("result");

  if (!input) {
    resultEl.innerText = "Please enter a URL or text.";
    return;
  }

  const endpoint = input.startsWith("http")
    ? "http://127.0.0.1:5000/analyze/url"
    : "http://127.0.0.1:5000/analyze/text";

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input })
    });

    if (!res.ok) throw new Error("Backend error");

    const data = await res.json();
    resultEl.innerText = `Result: ${data.result}\nReasons: ${data.reasons.join(", ")}`;
  } catch (err) {
    resultEl.innerText = "❌ Could not connect to backend. Make sure it’s running!";
    console.error(err);
  }
});
