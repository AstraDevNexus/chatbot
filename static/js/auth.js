import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDMgUlLMjrMDXCXJTdUpGdqRfB1U_kQpqU",
  authDomain: "ai-login-4a340.firebaseapp.com",
  projectId: "ai-login-4a340"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const isLogin = window.location.pathname === "/";

onAuthStateChanged(auth, user => {
  if (!user && !isLogin) window.location.href = "/";
  if (user && isLogin) window.location.href = "/chat";
});

window.loginGoogle = async () => {
  await signInWithPopup(auth, provider);
};

window.logout = async () => {
  await signOut(auth);
  window.location.href = "/";
};
