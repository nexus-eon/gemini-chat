document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    // Configure marked options
    marked.setOptions({
        breaks: true,  // Enable line breaks
        gfm: true,     // Enable GitHub Flavored Markdown
        sanitize: true // Sanitize HTML input
    });

    // Handle enter key press
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Handle send button click
    sendButton.addEventListener('click', sendMessage);

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Disable input and button while processing
        messageInput.disabled = true;
        sendButton.disabled = true;

        // Add user message to chat
        addMessage(message, 'user-message');

        // Clear input
        messageInput.value = '';

        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
            .then(response => response.json().then(data => ({ status: response.status, data })))
            .then(({ status, data }) => {
                if (status === 429) {
                    // Rate limit error
                    addMessage('⚠️ ' + data.error, 'bot-message error');
                    // Disable input for 1 hour if rate limited
                    if (data.rate_limited) {
                        messageInput.disabled = true;
                        sendButton.disabled = true;
                        setTimeout(() => {
                            messageInput.disabled = false;
                            sendButton.disabled = false;
                            addMessage('You can now send messages again.', 'bot-message system');
                        }, 60 * 60 * 1000); // 1 hour
                    }
                } else if (status !== 200) {
                    // Other error
                    addMessage('⚠️ Sorry, something went wrong. Please try again.', 'bot-message error');
                } else {
                    // Success - render markdown response
                    addMessage(data.response, 'bot-message', true);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('⚠️ Sorry, something went wrong. Please try again.', 'bot-message error');
            })
            .finally(() => {
                // Re-enable input and button
                messageInput.disabled = false;
                sendButton.disabled = false;
                messageInput.focus();
            });
    }

    function addMessage(text, className, isMarkdown = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = className;
        
        // If it's a bot message and not an error, render as markdown
        if (isMarkdown && className === 'bot-message') {
            messageDiv.innerHTML = marked.parse(text);
        } else {
            messageDiv.textContent = text;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
