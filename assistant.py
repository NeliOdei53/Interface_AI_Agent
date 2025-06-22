class AIAssistant:
    def __init__(self):
        # Этот метод вызывается один раз при запуске программы
        print("AI Assistant: Инициализация...")
        self.initialized = True
        print("AI Assistant: Инициализация завершена.")

    def invoke(self, user_question: str) -> str:
        # Этот метод вызывается для обработки вопроса пользователя
        print(f"AI Assistant: Получен вопрос: '{user_question}'")
        processed_info = f"Вопрос '{user_question}' принят к обработке ассистентом."
        print(f"AI Assistant: {processed_info}")

        if "версию ядра" in user_question.lower():
            return "Чтобы проверить версию ядра в ALT Linux, используйте команду:\n<code>uname -r</code>\nЭто покажет вам текущую версию загруженного ядра."
        if "обновления" in user_question.lower():
            return "Для установки последних обновлений безопасности в ALT Linux, вы можете использовать следующие команды в терминале:\n1. Обновить список пакетов: <code>sudo apt-get update</code>\n2. Установить обновления: <code>sudo apt-get dist-upgrade</code>\n\nЭто рекомендуемый способ поддерживать вашу систему в актуальном состоянии."

        return "Ваш вопрос обрабатывается (ответ от заглушки assistant.py)"