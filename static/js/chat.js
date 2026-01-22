const chatContainer = document.getElementById("chatMessages");
const input = document.getElementById("chatInput");

// --------------------
// SEND MESSAGE
// --------------------
function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      addMessage(data.reply, "ai");
    })
    .catch(() => {
      addMessage("⚠️ AI service unavailable.", "ai");
    });
}

// --------------------
// ADD MESSAGE
// --------------------
function addMessage(text, sender) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${sender}`;
  bubble.innerText = text;

  chatContainer.appendChild(bubble);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  bubble.animate(
    [{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "translateY(0)" }],
    { duration: 180, easing: "ease-out" }
  );
}

// --------------------
// NEW CHAT
// --------------------
function newChat() {
  chatContainer.innerHTML = "";
  addMessage("👋 Hello! Ask me anything.", "ai");
}

// --------------------
// ENTER TO SEND
// --------------------
input?.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
