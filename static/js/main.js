// ===============================
// IMPORTS
// ===============================
import { auth } from "./firebase.js";
import {
  createChat,
  loadChats,
  loadMessages,
  saveMessage,
  deleteChat
} from "./firestore.js";

import "./particles.js";

// ===============================
// DOM ELEMENTS
// ===============================
const chatListEl = document.getElementById("chatList");
const newChatBtn = document.getElementById("newChatBtn");
const logoutBtn = document.getElementById("logoutBtn");
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");

// ===============================
// STATE
// ===============================
let currentChatId = null;

// ===============================
// AUTH GUARD
// ===============================
auth.onAuthStateChanged(async user => {
  if (!user) {
    window.location.replace("/login");
    return;
  }

  await renderChatList();
});

// ===============================
// CHAT LIST (SIDEBAR)
// ===============================
async function renderChatList() {
  chatListEl.innerHTML = "";

  const chats = await loadChats();

  chats.forEach(chat => {
    const div = document.createElement("div");
    div.className = "chat-title";
    div.textContent = chat.title;

    div.onclick = async () => {
      currentChatId = chat.id;
      await loadChatMessages(chat.id);
    };

    chatListEl.appendChild(div);
  });
}

// ===============================
// LOAD CHAT MESSAGES
// ===============================
async function loadChatMessages(chatId) {
  chatMessages.innerHTML = "";

  const messages = await loadMessages(chatId);

  messages.forEach(msg => {
    addMessage(msg.content, msg.role);
  });
}

// ===============================
// NEW CHAT
// ===============================
newChatBtn.addEventListener("click", async () => {
  currentChatId = await createChat();
  chatMessages.innerHTML = "";
});

// ===============================
// SEND MESSAGE
// ===============================
sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text || !currentChatId) return;

  chatInput.value = "";

  // User message
  addMessage(text, "user");
  await saveMessage(currentChatId, "user", text);

  // AI typing placeholder
  const aiBubble = addMessage("", "ai");

  // Fake streaming (replace later with backend API)
  const response = "I'm Astra Nexus. Streaming replies are active ✨";

  for (let char of response) {
    aiBubble.textContent += char;
    await new Promise(r => setTimeout(r, 18));
  }

  await saveMessage(currentChatId, "ai", response);
}

// ===============================
// MESSAGE UI
// ===============================
function addMessage(text, role) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return div;
}

// ===============================
// LOGOUT
// ===============================
logoutBtn.addEventListener("click", async () => {
  await auth.signOut();
  window.location.replace("/login");
});
