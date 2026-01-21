export function initChat() {
  const input = document.querySelector("#prompt");
  const sendBtn = document.querySelector("#sendBtn");
  const messages = document.querySelector("#messages");

  sendBtn.onclick = () => {
    const text = input.value.trim();
    if (!text) return;

    addMsg(text, "user");
    input.value = "";
    fakeAI("Thinking...");
  };

  function addMsg(text, role) {
    const div = document.createElement("div");
    div.className = `msg ${role}`;
    div.textContent = text;
    messages.appendChild(div);
  }

  async function fakeAI(text) {
    const div = document.createElement("div");
    div.className = "msg ai";
    messages.appendChild(div);

    for (const ch of text) {
      div.textContent += ch;
      await new Promise(r => setTimeout(r, 25));
    }
  }
}
