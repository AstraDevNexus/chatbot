async function sendMessage() {
  const input = document.getElementById("message");
  const text = input.value.trim();
  if (!text) return;

  addMessage("user", text);
  input.value = "";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  });

  const data = await res.json();
  addMessage("bot", data.reply);
}

function addMessage(role, text) {
  const chat = document.getElementById("chat");
  const div = document.createElement("div");
  div.className = role;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}
