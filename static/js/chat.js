import { auth, db } from "./firebase.js";
import {
  collection, addDoc, getDocs, deleteDoc, doc, updateDoc
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const messages = document.getElementById("messages");
const chatList = document.getElementById("chatList");
let currentChatId = null;

function bubble(text, cls) {
  const d = document.createElement("div");
  d.className = cls;
  d.textContent = text;
  messages.appendChild(d);
  messages.scrollTop = messages.scrollHeight;
  return d;
}

async function createChat(title="New Chat") {
  const ref = await addDoc(collection(db, "chats"), {
    title,
    created: Date.now()
  });
  loadChats();
  currentChatId = ref.id;
}

async function loadChats() {
  chatList.innerHTML = "";
  const snap = await getDocs(collection(db, "chats"));
  snap.forEach(d => {
    const item = document.createElement("div");
    item.textContent = d.data().title;
    item.onclick = () => currentChatId = d.id;

    item.oncontextmenu = e => {
      e.preventDefault();
      const name = prompt("Rename chat", d.data().title);
      if (name) updateDoc(doc(db,"chats",d.id),{title:name});
    };

    const del = document.createElement("span");
    del.textContent = " ✖";
    del.onclick = () => deleteDoc(doc(db,"chats",d.id));

    item.appendChild(del);
    chatList.appendChild(item);
  });
}

document.getElementById("newChat").onclick = () => createChat();

document.getElementById("send").onclick = async () => {
  const msg = msgInput.value;
  bubble(msg,"user");

  const res = await fetch("/stream", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({message:msg})
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let ai = bubble("","ai");

  while(true){
    const {value,done}=await reader.read();
    if(done) break;
    ai.textContent += decoder.decode(value);
  }
};

loadChats();
