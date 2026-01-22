// --------------------
// AUTH GUARD
// --------------------
auth.onAuthStateChanged(user => {
  const isLoginPage = window.location.pathname.includes("login");

  if (!user && !isLoginPage) {
    window.location.replace("/login");
  }

  if (user && isLoginPage) {
    window.location.replace("/");
  }
});

// --------------------
// EMAIL LOGIN
// --------------------
function emailLogin() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  auth.signInWithEmailAndPassword(email, password)
    .then(() => window.location.replace("/"))
    .catch(err => showAuthError(err.message));
}

// --------------------
// EMAIL SIGNUP
// --------------------
function emailSignup() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  auth.createUserWithEmailAndPassword(email, password)
    .then(() => window.location.replace("/"))
    .catch(err => showAuthError(err.message));
}

// --------------------
// GOOGLE LOGIN
// --------------------
function googleLogin() {
  const provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithPopup(provider)
    .then(() => window.location.replace("/"))
    .catch(err => showAuthError(err.message));
}

// --------------------
// LOGOUT
// --------------------
function logout() {
  auth.signOut().then(() => {
    window.location.replace("/login");
  });
}

// --------------------
// ERROR DISPLAY
// --------------------
function showAuthError(msg) {
  const el = document.getElementById("authError");
  if (!el) return;
  el.innerText = msg;
  el.style.opacity = 1;
}
