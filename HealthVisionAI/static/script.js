async function sendMessage() {
  const inputField = document.getElementById("user-input");
  const userInput = inputField.value.trim();
  const chatBox = document.getElementById("chat-box");

  if (!userInput) return;

  // Show user message
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.innerHTML = `<strong>You:</strong> ${userInput}`;
  chatBox.appendChild(userMsg);

  inputField.value = "";

  // Fetch response from backend
  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();

    // Show bot response
    const botMsg = document.createElement("div");
    botMsg.className = "message bot";
    botMsg.innerHTML = `<strong>HealthVisionAI:</strong> ${data.response}`;
    chatBox.appendChild(botMsg);

  } catch (error) {
    const errorMsg = document.createElement("div");
    errorMsg.className = "message bot";
    errorMsg.innerHTML = `<strong>HealthVisionAI:</strong> ⚠️ Something went wrong. Try again later.`;
    chatBox.appendChild(errorMsg);
  }

  // Auto-scroll to bottom
  chatBox.scrollTop = chatBox.scrollHeight;
}
const userInput = document.getElementById("user-input");

function startListening() {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Sorry, your browser doesn't support voice recognition.");
    return;
  }

  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.lang = 'en-US';
  recognition.interimResults = false;

  recognition.start();

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    userInput.value = transcript;
    sendMessage(); // auto send
  };

  recognition.onerror = function(event) {
    console.error("Speech recognition error", event.error);
  };
}
