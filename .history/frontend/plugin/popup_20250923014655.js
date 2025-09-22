document.getElementById("checkBtn").addEventListener("click", async () => {
  const input = document.getElementById("userInput").value;
  const resultEl = document.getElementById("result");
  resultEl.innerText = "Analyzing..."; // Provide immediate feedback

  if (!input) {
    resultEl.innerText = "Please enter a URL or text.";
    return;
  }

  // Determine if the input is a URL or plain text
  const isUrl = input.startsWith("http");
  
  // Set the correct endpoint URL based on the input type
  const endpoint = isUrl
    ? "http://127.0.0.1:5000/analyze/url"
    : "http://127.0.0.1:5000/analyze/text";

  // Create the correct JSON body payload based on the input type
  // The backend expects {'url': '...'} for URLs and {'text': '...'} for text.
  const bodyPayload = isUrl ? { url: input } : { text: input };

  try {
    const response = await fetch(endpoint, {
      method: "POST", // <--- THIS IS THE CRITICAL FIX
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bodyPayload),
    });

    if (!response.ok) {
      // This will catch 404, 400, and 500 errors from the backend
      throw new Error(`Backend error! Status: ${response.status}`);
    }

    const data = await response.json();

    // Display the results (you can format this however you like)
    console.log("Analysis Result:", data);
    if (data.result === 'malicious') {
        resultEl.innerText = `Result: MALICIOUS  위험\nReason: ${data.reasons.join(", ")}`;
        resultEl.style.color = 'red';
    } else {
        resultEl.innerText = `Result: SAFE 안전\nType: ${data.type || 'N/A'}`;
        resultEl.style.color = 'green';
    }

  } catch (err) {
    console.error("Fetch error:", err);
    resultEl.innerText = `❌ Error: ${err.message}. Make sure the backend is running.`;
    resultEl.style.color = 'red';
  }
});