import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDMgUlLMjrMDXCXJTdUpGdqRfB1U_kQpqU",
  authDomain: "ai-login-4a340.firebaseapp.com",
  projectId: "ai-login-4a340",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

/* ---------- GOOGLE LOGIN ---------- */
window.googleLogin = async () => {
  try {
    await signInWithPopup(auth, provider);
    window.location.href = "/chat";
  } catch (err) {
    alert(err.message);
  }
};

/* ---------- EMAIL LOGIN ---------- */
window.emailLogin = async () => {
  const email = document.getElementById("email").value;
  const pass = document.getElementById("password").value;

  try {
    await signInWithEmailAndPassword(auth, email, pass);
    window.location.href = "/chat";
  } catch {
    await createUserWithEmailAndPassword(auth, email, pass);
    window.location.href = "/chat";
  }
};

/* ---------- AUTO REDIRECT ---------- */
onAuthStateChanged(auth, user => {
  if (user) window.location.href = "/chat";
});
