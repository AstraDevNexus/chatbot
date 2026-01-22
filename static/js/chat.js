export function initChat() {
  const input = document.getElementById("prompt");
  const sendBtn = document.getElementById("sendBtn");
  const messages = document.getElementById("messages");
  const newChatBtn = document.getElementById("newChatBtn");
  const logoutBtn = document.getElementById("logoutBtn");

  if (!input || !sendBtn || !messages) {
    console.error("Chat elements missing");
    return;
  }

  // SEND MESSAGE
  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    addMsg(text, "user");
    input.value = "";

    fakeAIResponse();
  }

  // NEW CHAT
  newChatBtn?.addEventListener("click", () => {
    messages.innerHTML = "";
    addMsg("👋 New chat started. Ask me anything.", "ai");
  });

  // LOGOUT
  logoutBtn?.addEventListener("click", async () => {
    await auth.signOut();
    window.location.href = "/login";
  });

  function addMsg(text, role) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function fakeAIResponse() {
    const div = document.createElement("div");
    div.className = "msg ai";
    messages.appendChild(div);

    const text = "🤖 Astra AI is connected. API integration pending.";
    let i = 0;

    const interval = setInterval(() => {
      div.textContent += text[i++];
      if (i >= text.length) clearInterval(interval);
    }, 20);
  }

  // Welcome message
  addMsg("👋 Hello! Ask me anything — weather, code, ideas, or chat.", "ai");
}
