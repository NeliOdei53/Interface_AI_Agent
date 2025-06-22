document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const showPredefinedBtn = document.getElementById('show-predefined-btn');
    const predefinedQuestionsPopup = document.getElementById('predefined-questions-popup');
    const predefinedQuestionsList = document.getElementById('predefined-questions-list');
    const closePopupBtn = document.getElementById('close-popup-btn');
    const themeToggleButton = document.querySelector('.chat-header .theme-icon');
    const chatContainer = document.querySelector('.chat-container');
    const bodyElement = document.body;

    // URL для аватарок
    const userAvatarUrl = "/static/images/photo_2025-06-21_15-42-36.jpg";
    const assistantAvatarUrl = "/static/images/photo_2025-06-21_15-31-50.jpg";
    
    const predefinedQuestions = [
        "Как установить последние обновления безопасности в ALT Linux?",
        "Есть ли поддержка Snap пакетов?",
        "Как проверить версию ядра?",
        "Где найти документацию по ALT Linux?",
        "Как настроить сеть?",
        "Можно ли установить Steam?",
        "Какие есть графические окружения?",
        "Как добавить нового пользователя?",
        "Команда для обновления списка пакетов?",
        "Как установить программу из репозитория?"
    ];

    function addMessage(text, sender) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message', sender);

        const avatarImg = document.createElement('img');
        avatarImg.classList.add('avatar');
        avatarImg.src = (sender === 'user') ? userAvatarUrl : assistantAvatarUrl;
        avatarImg.alt = sender;

        const messageContentDiv = document.createElement('div');
        messageContentDiv.classList.add('message-content');

        if (sender === 'assistant') {
            messageContentDiv.innerHTML = text; // Allows <code> tags
        } else {
            messageContentDiv.textContent = text;
        }

        if (sender === 'user') {
            messageWrapper.appendChild(messageContentDiv);
            messageWrapper.appendChild(avatarImg);
        } else {
            messageWrapper.appendChild(avatarImg);
            messageWrapper.appendChild(messageContentDiv);
        }
        
        chatMessages.appendChild(messageWrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendQuestion(questionText) {
        if (!questionText.trim()) return;

        addMessage(questionText, 'user');
        userInput.value = '';

        const processingMessageText = "Ваш вопрос обрабатывается...";
        addMessage(processingMessageText, 'assistant');
        const tempProcessingMessage = Array.from(chatMessages.querySelectorAll('.message.assistant .message-content'))
                                       .find(el => el.innerHTML === processingMessageText); // Use innerHTML to match

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: questionText }),
            });

            if (tempProcessingMessage && tempProcessingMessage.parentElement) {
                tempProcessingMessage.parentElement.remove();
            }

            if (!response.ok) {
                const errorData = await response.json();
                addMessage(`Ошибка: ${errorData.error || response.statusText}`, 'assistant');
                return;
            }

            const data = await response.json();
            addMessage(data.answer, 'assistant');
            console.log("Ответ от сервера:", data);
            // const lastAssistantMessage = chatMessages.querySelector('.message.assistant:last-child');
            // if (lastAssistantMessage && lastAssistantMessage.textContent.includes("обрабатывается")) {
            //    lastAssistantMessage.textContent = data.answer;
            // } else {
            //    addMessage(data.answer, 'assistant');
            // }

        } catch (error) {
            console.error('Ошибка при отправке вопроса:', error);
            if (tempProcessingMessage && tempProcessingMessage.parentElement) {
                 tempProcessingMessage.parentElement.remove();
            }
            addMessage("Не удалось связаться с сервером.", 'assistant');
        }
    }

    sendButton.addEventListener('click', () => sendQuestion(userInput.value));

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion(userInput.value);
        }
    });

    predefinedQuestions.forEach(qText => {
        const button = document.createElement('button');
        button.textContent = qText;
        button.addEventListener('click', () => {
            userInput.value = qText;
            predefinedQuestionsPopup.classList.add('hidden');
            userInput.focus(); 
        });
        predefinedQuestionsList.appendChild(button);
    });

    showPredefinedBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        predefinedQuestionsPopup.classList.toggle('hidden');
    });
    
    closePopupBtn.addEventListener('click', () => {
        predefinedQuestionsPopup.classList.add('hidden');
    });

    document.addEventListener('click', (event) => {
        if (!predefinedQuestionsPopup.classList.contains('hidden') && 
            !predefinedQuestionsPopup.contains(event.target) && 
            event.target !== showPredefinedBtn) {
            predefinedQuestionsPopup.classList.add('hidden');
        }
    });

    // Theme Toggling
    function applyTheme(theme) {
        if (theme === 'light') {
            chatContainer.classList.add('light-theme');
            bodyElement.classList.add('light-theme-active');
            themeToggleButton.textContent = '☀️';
            localStorage.setItem('chatTheme', 'light');
        } else {
            chatContainer.classList.remove('light-theme');
            bodyElement.classList.remove('light-theme-active');
            themeToggleButton.textContent = '🌙';
            localStorage.setItem('chatTheme', 'dark');
        }
    }

    themeToggleButton.addEventListener('click', () => {
        const currentTheme = chatContainer.classList.contains('light-theme') ? 'dark' : 'light';
        applyTheme(currentTheme);
    });

    const savedTheme = localStorage.getItem('chatTheme');
    applyTheme(savedTheme || 'dark'); // Default to dark if no theme is saved


    // Reasoning Toggle (only if new UI is active and elements exist)
    const reasoningToggle = document.getElementById('reasoningToggle');
    const reasoningToggleLabel = document.getElementById('reasoningToggleLabel');

    if (reasoningToggle && reasoningToggleLabel) {
        // Initialize label based on checkbox state (default to OFF as per HTML)
        reasoningToggleLabel.textContent = `Reasoning: ${reasoningToggle.checked ? 'ON' : 'OFF'}`;

        reasoningToggle.addEventListener('change', function() {
            const isEnabled = this.checked;
            reasoningToggleLabel.textContent = `Reasoning: ${isEnabled ? 'ON' : 'OFF'}`;
            console.log(`Reasoning mode: ${isEnabled ? 'ON' : 'OFF'}`);
            // Future: send this state to the backend or use it to modify requests
        });
    }

    // Optional: Initial greeting message
    // addMessage("Здравствуйте! Я ваш AI ассистент по ALT Linux. Чем могу помочь?", 'assistant');
});