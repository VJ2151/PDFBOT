// static/js/app.js
const uploadForm = document.getElementById("uploadForm");
const questionForm = document.getElementById("questionForm");
const chatBox = document.getElementById("chatBox");
const uploadStatus = document.getElementById("uploadStatus");
const loading = document.getElementById("loading");

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(uploadForm);

  const res = await fetch("/upload/", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  uploadStatus.innerText = data.message || "PDF uploaded!";
  chatBox.innerHTML = ''; // clear chat
});

questionForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = questionForm.elements["question"];
  const question = input.value;

  if (!question.trim()) return;

  // Show user bubble
  appendBubble(question, "user");
  input.value = "";

  loading.style.display = "block";

  const res = await fetch("/ask/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await res.json();
  loading.style.display = "none";

  if (data.answer) {
    appendBubble(data.answer, "bot");
  } else {
    appendBubble("Error: " + (data.error || "Something went wrong"), "bot");
  }
});

function appendBubble(message, sender) {
  const bubble = document.createElement("div");
  bubble.classList.add("chat-bubble", sender);
  bubble.innerText = message;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}
