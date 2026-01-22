// Neon logo pulse
const logo = document.querySelector(".logo, .login-logo");
if (logo) {
  setInterval(() => {
    logo.classList.toggle("pulse");
  }, 2500);
}

// Button tap animation
document.querySelectorAll("button").forEach(btn => {
  btn.addEventListener("click", () => {
    btn.classList.add("tap");
    setTimeout(() => btn.classList.remove("tap"), 150);
  });
});
