const firebaseConfig = {
  apiKey: "PUBLIC_KEY",
  authDomain: "PROJECT.firebaseapp.com",
  projectId: "PROJECT"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

function googleLogin(){
  auth.signInWithPopup(new firebase.auth.GoogleAuthProvider())
    .then(()=>location.href="/");
}

function emailLogin(){
  auth.signInWithEmailAndPassword(
    email.value, password.value
  ).then(()=>location.href="/");
}
