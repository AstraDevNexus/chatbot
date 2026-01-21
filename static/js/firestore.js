async function loadChats() {
  const list = document.getElementById("chatList");
  list.innerHTML = "";

  // Placeholder UI (backend hook later)
  ["New Chat", "Weather Help", "Code Session"].forEach(title => {
    const div = document.createElement("div");
    div.textContent = title;
    list.appendChild(div);
  });
}
