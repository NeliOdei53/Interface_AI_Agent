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

        # <-- ИЗМЕНЕНО: Ответы теперь используют синтаксис Markdown -->
        if "версию ядра" in user_question.lower():
            return "Чтобы проверить **версию ядра** в ALT Linux, используйте команду:\n```bash\nuname -r\n```\nЭто покажет вам текущую версию загруженного ядра."
        
        if "обновления" in user_question.lower():
            return """
Для установки **последних обновлений** безопасности в ALT Linux, вы можете использовать следующие команды в терминале:

1.  Обновить список пакетов:
    `sudo apt-get update`
2.  Установить обновления:
    `sudo apt-get dist-upgrade`

Это *рекомендуемый* способ поддерживать вашу систему в актуальном состоянии.
"""

        return "Ваш вопрос обрабатывается (ответ от заглушки assistant.py)"