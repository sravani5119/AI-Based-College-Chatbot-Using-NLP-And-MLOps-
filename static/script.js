function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (!message) return;

    appendMessage("You", message, "user-message");

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("Bot", data.response, "bot-message");
    })
    .catch(error => {
        console.error("Error:", error);
    });

    inputField.value = "";
}

function appendMessage(sender, message, className) {
    const chatBox = document.getElementById("chat-box");

    const messageDiv = document.createElement("div");
    messageDiv.className = className;

    messageDiv.innerHTML = "<b>" + sender + ":</b><br>" + message.replace(/\n/g, "<br>");

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}