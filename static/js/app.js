const messages = document.getElementById("messages");

function add(text, cls){
  const d = document.createElement("div");
  d.className = "message " + cls;
  d.innerText = text;
  messages.appendChild(d);
  messages.scrollTop = messages.scrollHeight;
}

async function send(){
  const input = document.getElementById("input");
  const text = input.value;
  if(!text) return;

  add(text, "user");
  input.value = "";

  const r = await fetch("/api/chat", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({message:text})
  });

  const data = await r.json();
  typeEffect(data.reply);
}

function typeEffect(text){
  let i = 0;
  const d = document.createElement("div");
  d.className="message bot";
  messages.appendChild(d);

  const interval = setInterval(()=>{
    d.innerText += text[i++];
    if(i>=text.length) clearInterval(interval);
    messages.scrollTop = messages.scrollHeight;
  }, 15);
}
