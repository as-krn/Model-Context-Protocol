const chatBox = document.getElementById("chat-box");
const inputField = document.getElementById("user-input");

async function sendMessage() {
  const text = inputField.value.trim();
  if (!text) return;

  // Kullanıcı mesajını ekrana koy
  appendMessage(text, "user");
  inputField.value = "";

  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();
    appendMessage(data.response, "bot");
  } catch (err) {
    appendMessage("Error: Could not reach backend.", "bot");
  }
}

function appendMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Enter'a basınca mesaj gönder
inputField.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
