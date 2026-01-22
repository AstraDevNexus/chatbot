import {
  getFirestore,
  collection,
  addDoc,
  getDocs,
  query,
  where,
  orderBy,
  serverTimestamp,
  doc,
  deleteDoc
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore.js";

import { auth } from "./firebase.js";

export const db = getFirestore();

/* ================================
   CREATE NEW CHAT
================================ */
export async function createChat() {
  const user = auth.currentUser;
  if (!user) return;

  const ref = await addDoc(collection(db, "chats"), {
    uid: user.uid,
    title: "New Chat",
    createdAt: serverTimestamp()
  });

  return ref.id;
}

/* ================================
   SAVE MESSAGE
================================ */
export async function saveMessage(chatId, role, content) {
  const user = auth.currentUser;
  if (!user || !chatId) return;

  await addDoc(collection(db, "messages"), {
    chatId,
    uid: user.uid,
    role,
    content,
    createdAt: serverTimestamp()
  });
}

/* ================================
   LOAD USER CHATS
================================ */
export async function loadChats() {
  const user = auth.currentUser;
  if (!user) return [];

  const q = query(
    collection(db, "chats"),
    where("uid", "==", user.uid),
    orderBy("createdAt", "desc")
  );

  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
}

/* ================================
   LOAD CHAT MESSAGES
================================ */
export async function loadMessages(chatId) {
  const q = query(
    collection(db, "messages"),
    where("chatId", "==", chatId),
    orderBy("createdAt")
  );

  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => doc.data());
}

/* ================================
   DELETE CHAT
================================ */
export async function deleteChat(chatId) {
  await deleteDoc(doc(db, "chats", chatId));
}
