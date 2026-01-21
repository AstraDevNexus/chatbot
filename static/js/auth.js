function login() {
  fetch("/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email: document.getElementById("email").value })
  }).then(() => location.href = "/");
}
