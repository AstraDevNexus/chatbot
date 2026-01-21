const send = document.getElementById("send");
const input = document.getElementById("input");
const messages = document.getElementById("messages");

send.onclick = async () => {
  const text = input.value;
  if (!text) return;

  messages.innerHTML += `<div class="user">${text}</div>`;
  input.value = "";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: text})
  });

  const data = await res.json();
  typeText(data.reply);
};

function typeText(text) {
  let i = 0;
  const el = document.createElement("div");
  el.className = "bot";
  messages.appendChild(el);

  const interval = setInterval(() => {
    el.textContent += text[i++];
    if (i >= text.length) clearInterval(interval);
  }, window.innerWidth < 600 ? 15 : 8);
}
