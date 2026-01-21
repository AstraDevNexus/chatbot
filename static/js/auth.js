// static/js/auth.js
import { auth } from "./firebase.js";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup
} from "https://www.gstatic.com/firebasejs/9.23.0/firebase-auth.js";

export function initAuth() {
  const email = document.querySelector("#email");
  const password = document.querySelector("#password");

  document.querySelector("#loginBtn").onclick = () =>
    signInWithEmailAndPassword(auth, email.value, password.value);

  document.querySelector("#signupBtn").onclick = () =>
    createUserWithEmailAndPassword(auth, email.value, password.value);

  document.querySelector("#googleBtn").onclick = () =>
    signInWithPopup(auth, new GoogleAuthProvider());
}
