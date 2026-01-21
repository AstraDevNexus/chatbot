import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signOut
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const app = initializeApp({
  apiKey: "AIzaSyDMgUlLMjrMDXCXJTdUpGdqRfB1U_kQpqU",
  authDomain: "ai-login-4a340.firebaseapp.com",
  projectId: "ai-login-4a340"
});

const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const isLogin = location.pathname === "/";

onAuthStateChanged(auth, user => {
  if (!user && !isLogin) location.href = "/";
  if (user && isLogin) location.href = "/chat";
});

window.googleLogin = () => signInWithPopup(auth, provider);
window.emailLogin = async () => {
  const e = email.value, p = password.value;
  try {
    await signInWithEmailAndPassword(auth, e, p);
  } catch {
    await createUserWithEmailAndPassword(auth, e, p);
  }
};

window.logout = () => signOut(auth);
