from flask import Flask, render_template, request, jsonify
from assistant import AIAssistant # Импортируем наш класс ассистента
import yaml
import os

app = Flask(__name__)

# --- Configuration Loading ---
CONFIG_FILE = 'config.yaml'
config = {'ui_version': 'legacy'} # Default

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r') as f:
            loaded_config = yaml.safe_load(f)
            if loaded_config and 'ui_version' in loaded_config:
                config['ui_version'] = loaded_config['ui_version']
                print(f"Flask App: Loaded UI version '{config['ui_version']}' from {CONFIG_FILE}.")
            else:
                print(f"Flask App: Warning: 'ui_version' not found in {CONFIG_FILE}. Defaulting to 'legacy'.")
    except yaml.YAMLError as e:
        print(f"Flask App: Error loading {CONFIG_FILE}: {e}. Defaulting to 'legacy'.")
    except Exception as e:
        print(f"Flask App: An unexpected error occurred while loading {CONFIG_FILE}: {e}. Defaulting to 'legacy'.")
else:
    print(f"Flask App: Warning: {CONFIG_FILE} not found. Defaulting to 'legacy' UI.")
# --- End Configuration Loading ---


# Инициализируем ассистента один раз при старте приложения
ai_assistant = AIAssistant()

last_user_question = None

@app.route('/')
def index():
    """Отдает главную HTML-страницу."""
    return render_template('index.html', ui_version=config.get('ui_version', 'legacy'))

@app.route('/ask', methods=['POST'])
def ask_assistant():
    """Обрабатывает вопрос пользователя."""
    global last_user_question
    data = request.get_json()
    user_question = data.get('question')

    if not user_question:
        return jsonify({'error': 'Вопрос не может быть пустым'}), 400

    print(f"Flask App: Получен вопрос от пользователя: '{user_question}'")
    last_user_question = user_question # Сохраняем вопрос

    # Вызываем метод invoke нашего ассистента
    assistant_response_internal = ai_assistant.invoke(user_question)
    print(f"Flask App: Внутренний ответ от ассистента: '{assistant_response_internal}'") # для отладки
    
    response_to_user = "Ваш вопрос обрабатывается" 

    return jsonify({'answer': response_to_user, 'received_question': user_question})

if __name__ == '__main__':
    print("Flask App: Запуск веб-сервера...")
    app.run(debug=True) # debug=True для разработки