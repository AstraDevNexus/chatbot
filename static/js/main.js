import { initChat } from "./chat.js";
import { initParticles } from "./particles.js";

document.addEventListener("DOMContentLoaded", () => {
  initParticles();
  initChat();
});
