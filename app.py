from flask import Flask, render_template, request, jsonify
from assistant import AIAssistant # Импортируем наш класс ассистента
import yaml
import os
import markdown

# --- Configuration Loading Function ---
def load_app_configuration():
    config_file = 'config.yaml'
    default_ui_version = 'legacy'
    ui_version_to_use = default_ui_version # Start with default

    print(f"Flask App: Initializing configuration. Default UI version is '{default_ui_version}'.")

    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                loaded_config = yaml.safe_load(f)
                if loaded_config and isinstance(loaded_config, dict) and 'ui_version' in loaded_config:
                    potential_version = str(loaded_config['ui_version']).strip().lower()
                    if potential_version in ['new', 'legacy']:
                        ui_version_to_use = potential_version
                        print(f"Flask App: Loaded UI version '{ui_version_to_use}' from {config_file}.")
                    else:
                        print(f"Flask App: Warning: Invalid 'ui_version' value ('{potential_version}') in {config_file}. Using default '{default_ui_version}'.")
                        # ui_version_to_use remains default_ui_version
                elif not loaded_config or not isinstance(loaded_config, dict):
                    print(f"Flask App: Warning: {config_file} is empty, not valid YAML, or not a dictionary. Using default '{default_ui_version}'.")
                     # ui_version_to_use remains default_ui_version
                else: # 'ui_version' key not found
                    print(f"Flask App: Warning: 'ui_version' key not found in {config_file}. Using default '{default_ui_version}'.")
                     # ui_version_to_use remains default_ui_version
        except yaml.YAMLError as e:
            print(f"Flask App: Error loading {config_file}: {e}. Using default '{default_ui_version}'.")
            # ui_version_to_use remains default_ui_version
        except Exception as e:
            print(f"Flask App: An unexpected error occurred while loading {config_file}: {e}. Using default '{default_ui_version}'.")
            # ui_version_to_use remains default_ui_version
    else:
        print(f"Flask App: Warning: {config_file} not found. Using default '{default_ui_version}' UI.")
        # ui_version_to_use remains default_ui_version

    print(f"Flask App: Final UI version determined for this session: '{ui_version_to_use}'.")
    return {'ui_version': ui_version_to_use}
# --- End Configuration Loading Function ---

app = Flask(__name__)

# Загружаем конфигурацию один раз при старте приложения
APP_CONFIG = load_app_configuration()

# Инициализируем ассистента один раз при старте приложения
ai_assistant = AIAssistant()

last_user_question = None

@app.route('/')
def index():
    """Отдает главную HTML-страницу."""
    # Используем значение из загруженной конфигурации
    ui_version_for_template = APP_CONFIG.get('ui_version', 'legacy')
    print(f"Flask App: Rendering index.html with ui_version = '{ui_version_for_template}' (type: {type(ui_version_for_template)}) for template.")
    return render_template('index.html', ui_version=ui_version_for_template)

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

    assistant_response_internal = ai_assistant.invoke(user_question)
    print(f"Flask App: Внутренний ответ от ассистента (Markdown): '{assistant_response_internal}'") # для отладки
    
    response_to_user = markdown.markdown(assistant_response_internal, extensions=['fenced_code'])

    return jsonify({'answer': response_to_user, 'received_question': user_question})

if __name__ == '__main__':
    print("Flask App: Запуск веб-сервера...")
    app.run(debug=True)