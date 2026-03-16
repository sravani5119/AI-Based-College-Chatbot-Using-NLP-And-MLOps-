function sendMessage() {

    const inputField = document.getElementById("user-input");
    const message = inputField.value.trim();

    if (!message) return;

    appendMessage("You", message, "user-message");

    inputField.value = "";

    // Create typing indicator
    const chatBox = document.getElementById("chat-box");

    const typingDiv = document.createElement("div");
    typingDiv.className = "bot-message";
    typingDiv.id = "typing-indicator";
    typingDiv.innerHTML = "Bot is typing...";

    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {

    setTimeout(() => {

        const typing = document.getElementById("typing-indicator");
        if (typing) typing.remove();

        appendMessage("Bot", data.response, "bot-message");

    }, 700);

})
    .catch(error => {
        console.error("Error:", error);
    });

}
function appendMessage(sender, message, className) {

    const chatBox = document.getElementById("chat-box");

    const messageDiv = document.createElement("div");
    messageDiv.className = className;

    // Format message
    const formattedMessage = message.replace(/\n/g, "<br>");

    messageDiv.innerHTML = formattedMessage;

    // Detect links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const urls = message.match(urlRegex);

    if (urls) {

        urls.forEach(url => {

            // Show PDF inside chat
            if (url.endsWith(".pdf")) {

                const iframe = document.createElement("iframe");

                iframe.src = url;
                iframe.width = "100%";
                iframe.height = "400px";
                iframe.style.border = "none";
                iframe.style.marginTop = "10px";

                messageDiv.appendChild(iframe);
            }

            // Show image inside chat
            if (
                url.endsWith(".jpg") ||
                url.endsWith(".jpeg") ||
                url.endsWith(".png")
            ) {

                const img = document.createElement("img");

                img.src = url;
                img.style.maxWidth = "100%";
                img.style.marginTop = "10px";
                img.style.borderRadius = "8px";

                messageDiv.appendChild(img);
            }

        });

    }

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}