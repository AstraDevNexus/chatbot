import { auth } from "./firebase.js";
import {
  GoogleAuthProvider,
  signInWithPopup,
  onAuthStateChanged,
  signOut
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const provider = new GoogleAuthProvider();

document.getElementById("google")?.addEventListener("click", () =>
  signInWithPopup(auth, provider)
);

onAuthStateChanged(auth, user => {
  if (user && location.pathname === "/") location.href = "/chat";
});

document.getElementById("logout")?.addEventListener("click", () => {
  signOut(auth).then(() => location.href = "/");
});
