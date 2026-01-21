import { initChat } from "./chat.js";
import { initParticles } from "./particles.js";
import "./firebase.js";

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("messages")) {
    initParticles();
    initChat();
  }
});
