let currentChat = null;

function loadHistory() {
  fetch("/history")
    .then(r => r.json())
    .then(chats => {
      history.innerHTML = "";
      chats.forEach(c => {
        const div = document.createElement("div");
        div.textContent = c.title;
        div.onclick = () => currentChat = c.id;
        history.appendChild(div);
      });
    });
}

function newChat() {
  fetch("/new-chat", { method: "POST" })
    .then(r => r.json())
    .then(d => {
      currentChat = d.id;
      messages.innerHTML = "";
      loadHistory();
    });
}

function send() {
  if (!currentChat) return;
  const text = msg.value;
  messages.innerHTML += `<div class="msg">${text}</div>`;
  msg.value = "";

  fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ id: currentChat, message: text })
  })
  .then(r => r.json())
  .then(d => messages.innerHTML += `<div class="msg bot">${d.reply}</div>`);
}

function logout() {
  location.href = "/logout";
}

loadHistory();
