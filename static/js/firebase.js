const firebaseConfig = {
    apiKey: "AIzaSyDMgUlLMjrMDXCXJTdUpGdqRfB1U_kQpqU",
  authDomain: "ai-login-4a340.firebaseapp.com",
  projectId: "ai-login-4a340",
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

function googleLogin(){
  const provider = new firebase.auth.GoogleAuthProvider();
  auth.signInWithPopup(provider).then(()=>location="/chat");
}

function emailLogin(){
  const email = document.getElementById("email").value;
  const pass = document.getElementById("password").value;

  auth.signInWithEmailAndPassword(email, pass)
    .then(()=>location="/chat")
    .catch(()=>auth.createUserWithEmailAndPassword(email, pass)
      .then(()=>location="/chat"));
}
