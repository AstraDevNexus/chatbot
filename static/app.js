let messages = [];

function typeText(el, text){
  let i=0;
  let t=setInterval(()=>{
    el.innerHTML += text[i++];
    if(i>=text.length) clearInterval(t);
  },15);
}

function send(){
  let msg = input.value;
  input.value="";
  messages.push({role:"user",content:msg});

  let div=document.createElement("div");
  div.textContent=msg;
  messagesDiv.appendChild(div);

  fetch("/api/chat",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({messages})
  })
  .then(r=>r.json())
  .then(d=>{
    let a=document.createElement("div");
    messagesDiv.appendChild(a);
    typeText(a, d.reply);
    messages.push({role:"assistant",content:d.reply});
  });
}
